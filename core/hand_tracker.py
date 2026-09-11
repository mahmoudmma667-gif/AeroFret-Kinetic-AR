"""
AeroFret: Kinetic - Hand Tracker Module
High-precision dual-hand tracking using MediaPipe Hands.
Optimized for 45-60 FPS performance via scaled inference buffers,
CLAHE brightness normalization for dark environments,
adaptive EMA smoothing, and spatial disambiguation.
"""

from typing import Dict, List, Optional, Tuple
import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """
    Optimized Dual-Hand Tracker for Air-Guitar spatial interaction.
    Features:
      - CLAHE brightness normalization for tracking in dark/dim rooms
      - Adaptive velocity-aware EMA smoothing (less jitter at rest, faster response on movement)
      - 448x252 inference buffer for improved accuracy
      - Spatial X-partition disambiguation for fret vs strum hand
    """

    WRIST = 0
    THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP = 1, 2, 3, 4
    INDEX_MCP, INDEX_PIP, INDEX_DIP, INDEX_TIP = 5, 6, 7, 8
    MIDDLE_MCP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_TIP = 9, 10, 11, 12
    RING_MCP, RING_PIP, RING_DIP, RING_TIP = 13, 14, 15, 16
    PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP = 17, 18, 19, 20

    FINGER_TIPS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    FINGER_PIPS = [THUMB_IP, INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP]

    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.50,
        min_tracking_confidence: float = 0.50,
        smoothing_alpha: float = 0.72
    ):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=0,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.smoothing_alpha = smoothing_alpha
        self.prev_strum_tip: Optional[Tuple[int, int]] = None
        self.prev_fret_wrist: Optional[Tuple[int, int]] = None
        self.prev_fret_pts: Optional[List[Tuple[int, int, float]]] = None
        self.prev_strum_pts: Optional[List[Tuple[int, int, float]]] = None

        # CLAHE for dark environment brightness normalization
        self._clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

    def process_frame(self, frame_bgr: np.ndarray) -> Dict[str, Optional[dict]]:
        """
        Process frame with ultra-fast scaled inference, adaptive CLAHE normalization,
        and kinematic 21-joint temporal stabilization for fluid 60 FPS motion.
        """
        h, w, _ = frame_bgr.shape

        # Scale down for fast MediaPipe inference (448x252 for crisp detection)
        infer_w, infer_h = 448, 252
        small = cv2.resize(frame_bgr, (infer_w, infer_h))

        # Fast-path luminance check: subsampled green channel (<0.04ms)
        # Avoids expensive unconditional BGR->LAB->BGR conversions every frame
        mean_lum = float(np.mean(small[::4, ::4, 1]))
        if mean_lum < 85.0:
            lab = cv2.cvtColor(small, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = self._clahe.apply(lab[:, :, 0])
            small = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        small_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        small_rgb.flags.writeable = False
        results = self.hands.process(small_rgb)
        small_rgb.flags.writeable = True

        hands_data = {'fret_hand': None, 'strum_hand': None}

        if not results.multi_hand_landmarks:
            self.prev_strum_tip = None
            self.prev_fret_pts = None
            self.prev_strum_pts = None
            return hands_data

        detected_hands = []

        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label

            pts_px = []
            for lm in hand_landmarks.landmark:
                # Map normalized [0, 1] directly to native canvas dimensions
                px_x = int(lm.x * w)
                px_y = int(lm.y * h)
                pts_px.append((px_x, px_y, lm.z))

            xs = [p[0] for p in pts_px]
            ys = [p[1] for p in pts_px]
            center_x = sum(xs) // len(xs)
            center_y = sum(ys) // len(ys)

            extended = self._detect_extended_fingers(pts_px)
            finger_count = sum(extended)

            detected_hands.append({
                'label': handedness,
                'landmarks_px': pts_px,
                'center': (center_x, center_y),
                'wrist': pts_px[self.WRIST][:2],
                'index_tip': pts_px[self.INDEX_TIP][:2],
                'thumb_tip': pts_px[self.THUMB_TIP][:2],
                'extended': extended,
                'finger_count': finger_count,
                'raw_landmarks': hand_landmarks
            })

        # Disambiguate: In mirrored camera selfie view,
        # Player's Left Hand (Fret / Neck) is on the left half (X < 0.48 * W)
        # Player's Right Hand (Strum / Pick) is on the right half (X >= 0.48 * W)
        if len(detected_hands) == 1:
            h_info = detected_hands[0]
            if h_info['center'][0] < w * 0.48:
                hands_data['fret_hand'] = self._apply_fret_smoothing(h_info)
            else:
                hands_data['strum_hand'] = self._apply_strum_smoothing(h_info)
        elif len(detected_hands) >= 2:
            sorted_by_x = sorted(detected_hands, key=lambda d: d['center'][0])
            hands_data['fret_hand'] = self._apply_fret_smoothing(sorted_by_x[0])
            hands_data['strum_hand'] = self._apply_strum_smoothing(sorted_by_x[-1])

        return hands_data

    def _apply_strum_smoothing(self, strum_info: dict) -> dict:
        """
        Acceleration-Aware 21-Joint Kinematic Filter for Strumming Hand.
        Smooths all hand joints to eliminate visual jitter while maintaining 1:1 instantaneous response.
        """
        curr_pts = strum_info['landmarks_px']
        if self.prev_strum_pts is None or len(self.prev_strum_pts) != len(curr_pts):
            self.prev_strum_pts = curr_pts
            self.prev_strum_tip = strum_info['index_tip']
            return strum_info

        smoothed_pts = []
        for i, (cx, cy, cz) in enumerate(curr_pts):
            px, py, _ = self.prev_strum_pts[i]
            d = float(np.hypot(cx - px, cy - py))
            if d > 20.0:
                alpha = 1.0
            elif d > 4.0:
                alpha = 0.65 + (d - 4.0) / 16.0 * 0.35
            else:
                alpha = 0.60
            sx = int(alpha * cx + (1.0 - alpha) * px)
            sy = int(alpha * cy + (1.0 - alpha) * py)
            smoothed_pts.append((sx, sy, cz))

        self.prev_strum_pts = smoothed_pts
        strum_info['landmarks_px'] = smoothed_pts
        strum_info['index_tip'] = smoothed_pts[self.INDEX_TIP][:2]
        strum_info['wrist'] = smoothed_pts[self.WRIST][:2]
        strum_info['thumb_tip'] = smoothed_pts[self.THUMB_TIP][:2]
        self.prev_strum_tip = strum_info['index_tip']
        return strum_info

    def _apply_fret_smoothing(self, fret_info: dict) -> dict:
        """
        Carpal Kinematic Stabilizer for Fret Grip.
        Stabilizes all 21 fret hand joints for rock-solid chord stability and silky smooth positioning.
        """
        curr_pts = fret_info['landmarks_px']
        if self.prev_fret_pts is None or len(self.prev_fret_pts) != len(curr_pts):
            self.prev_fret_pts = curr_pts
            self.prev_fret_wrist = fret_info['wrist']
            return fret_info

        smoothed_pts = []
        for i, (cx, cy, cz) in enumerate(curr_pts):
            px, py, _ = self.prev_fret_pts[i]
            d = float(np.hypot(cx - px, cy - py))
            if d > 22.0:
                alpha = 1.0
            elif d > 4.0:
                alpha = 0.60 + (d - 4.0) / 18.0 * 0.40
            else:
                alpha = 0.55
            sx = int(alpha * cx + (1.0 - alpha) * px)
            sy = int(alpha * cy + (1.0 - alpha) * py)
            smoothed_pts.append((sx, sy, cz))

        self.prev_fret_pts = smoothed_pts
        fret_info['landmarks_px'] = smoothed_pts
        fret_info['wrist'] = smoothed_pts[self.WRIST][:2]
        fret_info['index_tip'] = smoothed_pts[self.INDEX_TIP][:2]
        fret_info['thumb_tip'] = smoothed_pts[self.THUMB_TIP][:2]
        self.prev_fret_wrist = fret_info['wrist']
        return fret_info

    def _detect_extended_fingers(self, pts: List[Tuple[int, int, float]]) -> List[bool]:
        """Detect which fingers are extended using relative joint distances."""
        extended = [False, False, False, False, False]
        wrist = pts[self.WRIST]

        pinky_mcp = pts[self.PINKY_MCP]
        d_tip = np.hypot(pts[self.THUMB_TIP][0] - pinky_mcp[0], pts[self.THUMB_TIP][1] - pinky_mcp[1])
        d_ip = np.hypot(pts[self.THUMB_IP][0] - pinky_mcp[0], pts[self.THUMB_IP][1] - pinky_mcp[1])
        extended[0] = d_tip > d_ip * 1.15

        for i, (tip_idx, pip_idx) in enumerate(zip(self.FINGER_TIPS[1:], self.FINGER_PIPS[1:]), start=1):
            tip_y = pts[tip_idx][1]
            pip_y = pts[pip_idx][1]
            dist_tip = np.hypot(pts[tip_idx][0] - wrist[0], pts[tip_idx][1] - wrist[1])
            dist_pip = np.hypot(pts[pip_idx][0] - wrist[0], pts[pip_idx][1] - wrist[1])
            extended[i] = (tip_y < pip_y) and (dist_tip > dist_pip * 1.06)

        return extended

    def draw_skeleton(self, frame: np.ndarray, hands_data: Dict[str, Optional[dict]]):
        """Draw streamlined cyberpunk hand landmarks."""
        for role, h_data in hands_data.items():
            if h_data is None:
                continue
            color = (0, 240, 255) if role == 'fret_hand' else (255, 0, 180)
            self.mp_draw.draw_landmarks(
                frame,
                h_data['raw_landmarks'],
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=2),
                self.mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=1)
            )

    def release(self):
        """Release MediaPipe resources."""
        self.hands.close()
