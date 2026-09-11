"""
AeroFret: Kinetic - HUD (Heads Up Display)
100% Fullscreen Camera UI with Zero Full-Width Bars.
100% English AAA Game Studio Holographic AR Badges:
- Transparent floating header pill (Top-Right) with Dancing Audio VU Spectrum
- Dynamic fretboard chord badge tracked at Top-Left (Clear of guitar & hands)
- Plectrum velocity gauge tracked to Right Index
- Floating Rhythm Game scoreboard card (Top-Right)
- Compact Rotary Power & Gain Dial (Bottom-Right, 162x70px)
- Minimalist floating bottom control pill
"""

import os
import math
import time
from typing import Dict, Optional, Tuple
import cv2
import numpy as np


class HUD:
    """
    Professional AAA Cyberpunk Holographic HUD for AeroFret Air Guitar.
    Zero full-width blocking bars: 100% fullscreen camera visibility.
    """

    COLOR_CYAN = (255, 230, 0)
    COLOR_MAGENTA = (230, 0, 255)
    COLOR_GOLD = (0, 215, 255)
    COLOR_BG_DARK = (15, 18, 28)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREEN = (0, 255, 140)

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_DUPLEX
        self.font_small = cv2.FONT_HERSHEY_SIMPLEX
        self.start_time = time.time()

        # Load high-definition cyberpunk guitar logo badge
        self.logo_badge = None
        badge_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'logo_badge.png')
        if os.path.exists(badge_path):
            try:
                data = np.fromfile(badge_path, dtype=np.uint8)
                b_img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
                if b_img is not None:
                    # High-fidelity area downsampling preserves subpixel edge clarity
                    self.logo_badge = cv2.resize(b_img, (36, 36), interpolation=cv2.INTER_AREA)
            except Exception:
                pass

    def render(
        self,
        frame: np.ndarray,
        fret_hand_data: Optional[dict],
        strum_hand_data: Optional[dict],
        chord_code: str,
        chord_display: str,
        fps: float,
        rhythm_manager=None,
        last_gain: float = 0.8,
        power_level: float = 0.85
    ) -> np.ndarray:
        h, w, _ = frame.shape

        # 1. Minimalist Top-Right Floating Telemetry Pill with Audio VU Meter
        self._render_floating_header(frame, w, fps, rhythm_manager, power_level)

        # 2. Dynamic Fret Badge (Top-Left, clear of neck & hands)
        self._render_fret_badge(frame, fret_hand_data, chord_code, chord_display)

        # 3. Dynamic Plectrum Velocity Gauge near Right Hand
        if strum_hand_data is not None:
            self._render_strum_gauge(frame, strum_hand_data, last_gain)

        # 4. Compact Interactive Rotary Power & Gain Dial (Bottom-Right, 145x62px)
        self._render_power_dial(frame, w, h, power_level)

        # 5. Rhythm Game Telemetry (when active)
        if rhythm_manager and rhythm_manager.is_active:
            self._render_rhythm_telemetry(frame, w, h, rhythm_manager)

        # 6. Compact Frosted Glass Mode Switcher Badge (Bottom-Left)
        self._render_mode_pill(frame, w, h, rhythm_manager)

        return frame

    def _draw_glass_box(
        self,
        frame: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        bg_color: Tuple[int, int, int] = (15, 18, 28),
        border_color: Optional[Tuple[int, int, int]] = (65, 75, 100),
        alpha: float = 0.75
    ):
        """Renders an anti-aliased, alpha-blended glassmorphic panel."""
        h_f, w_f = frame.shape[:2]
        x1 = max(0, min(w_f - 1, x))
        y1 = max(0, min(h_f - 1, y))
        x2 = max(0, min(w_f - 1, x + w))
        y2 = max(0, min(h_f - 1, y + h))

        if x2 <= x1 or y2 <= y1:
            return

        sub = frame[y1:y2, x1:x2]
        colored_rect = np.full(sub.shape, bg_color, dtype=np.uint8)
        blended = cv2.addWeighted(colored_rect, alpha, sub, 1.0 - alpha, 0)
        frame[y1:y2, x1:x2] = blended

        if border_color is not None:
            cv2.rectangle(frame, (x1, y1), (x2, y2), border_color, 1, cv2.LINE_AA)

    def _render_floating_header(self, frame: np.ndarray, width: int, fps: float, rhythm_manager, power_level: float):
        """Top-Right compact floating glass pill with high-def anti-aliased logo badge, kinetic branding, and dancing audio spectrum."""
        is_rhythm = rhythm_manager and rhythm_manager.is_active
        mode_text = "HERO" if is_rhythm else "PLAY"
        mode_color = self.COLOR_MAGENTA if is_rhythm else self.COLOR_GREEN

        pill_w = 415
        pill_h = 42
        pill_x = width - pill_w - 18
        pill_y = 14

        self._draw_glass_box(frame, pill_x, pill_y, pill_w, pill_h, self.COLOR_BG_DARK, (75, 88, 120), alpha=0.86)

        t = time.time() - self.start_time

        # --- High-Definition Vector / Badge Emblem (No pixelation!) ---
        icon_cx = pill_x + 24
        icon_cy = pill_y + 21

        if self.logo_badge is not None:
            bx = pill_x + 6
            by = pill_y + 3
            bw, bh = self.logo_badge.shape[1], self.logo_badge.shape[0]
            roi = frame[by:by + bh, bx:bx + bw]
            if roi.shape[0] == bh and roi.shape[1] == bw and self.logo_badge.shape[2] == 4:
                # Soft neon ambient backglow behind the hex
                glow_pulse = 0.4 + 0.3 * math.sin(t * 4.0)
                sub_glow = cv2.circle(roi.copy(), (18, 18), 16, (int(255 * glow_pulse), int(180 * glow_pulse), 0), -1)
                roi = cv2.addWeighted(sub_glow, 0.35, roi, 0.65, 0)

                alpha = self.logo_badge[:, :, 3:4].astype(np.float32) / 255.0
                rgb = self.logo_badge[:, :, :3].astype(np.float32)
                blended = (rgb * alpha + roi.astype(np.float32) * (1.0 - alpha)).astype(np.uint8)
                frame[by:by + bh, bx:bx + bw] = blended
        else:
            # High-definition crisp circular badge fallback
            cv2.circle(frame, (icon_cx, icon_cy), 14, (28, 32, 48), -1, cv2.LINE_AA)
            cv2.circle(frame, (icon_cx, icon_cy), 14, (0, 229, 255), 1, cv2.LINE_AA)
            cv2.circle(frame, (icon_cx, icon_cy), 3, (255, 255, 255), -1)

        # --- Brand Typography (Crisp Anti-Aliased) ---
        cv2.putText(frame, "AEROFRET", (pill_x + 48, pill_y + 21), self.font, 0.48, self.COLOR_CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, "KINETIC", (pill_x + 49, pill_y + 34), self.font_small, 0.30, (190, 215, 255), 1, cv2.LINE_AA)

        # Accent gradient separator line
        cv2.line(frame, (pill_x + 134, pill_y + 10), (pill_x + 134, pill_y + 32), (60, 72, 95), 1, cv2.LINE_AA)

        # --- Mode Badge ---
        badge_x = pill_x + 144
        badge_y = pill_y + 11
        badge_w = 48
        badge_h = 20
        cv2.rectangle(frame, (badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h), (25, 30, 45), -1)
        cv2.rectangle(frame, (badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h), mode_color, 1, cv2.LINE_AA)
        cv2.putText(frame, mode_text, (badge_x + 6, badge_y + 14), self.font_small, 0.36, mode_color, 1, cv2.LINE_AA)

        # --- Dancing Audio VU Spectrum (6 gradient bars) ---
        vu_x = pill_x + 204
        vu_base_y = pill_y + 30
        for b_i in range(6):
            bar_h = int((5 + 14 * power_level) * (0.45 + 0.55 * math.sin(t * (6.5 + b_i * 2.1) + b_i * 1.2)))
            bx = vu_x + b_i * 7
            bar_col = (255, 230, 0) if b_i < 3 else ((0, 200, 255) if b_i < 5 else (230, 0, 255))
            cv2.line(frame, (bx, vu_base_y), (bx, vu_base_y - bar_h), bar_col, 3, cv2.LINE_AA)

        # --- FPS & Latency Telemetry ---
        dot_col = self.COLOR_GREEN if fps >= 45 else ((0, 215, 255) if fps >= 30 else (0, 100, 255))
        cv2.circle(frame, (pill_x + 264, pill_y + 21), 3, dot_col, -1)

        fps_text = f"{int(fps)} FPS"
        cv2.putText(frame, fps_text, (pill_x + 274, pill_y + 26), self.font_small, 0.42, self.COLOR_WHITE, 1, cv2.LINE_AA)
        cv2.putText(frame, "<8ms", (pill_x + 350, pill_y + 26), self.font_small, 0.36, (160, 175, 205), 1, cv2.LINE_AA)

    def _render_fret_badge(
        self,
        frame: np.ndarray,
        fret_hand: Optional[dict],
        chord_code: str,
        chord_display: str
    ):
        """Compact, sleek glassmorphic chord card (148 x 40 px) with micro LED indicators."""
        bw, bh = 148, 40
        bx = 18
        by = 14
        finger_count = fret_hand['finger_count'] if fret_hand is not None else 0

        if chord_code == 'MUTE' or finger_count == 0:
            chord_title = "PALM MUTE"
            border_color = (0, 140, 255)
            glow_color = (0, 140, 255)
        else:
            CHORD_MAP_INFO = {
                'C': "C MAJOR",
                'Dm': "D MINOR",
                'Em': "E MINOR",
                'F': "F MAJOR",
                'G': "G MAJOR"
            }
            chord_title = CHORD_MAP_INFO.get(chord_code, chord_display)
            border_color = (0, 240, 255)
            glow_color = (0, 255, 200)

        # Compact frosted glass panel
        self._draw_glass_box(frame, bx, by, bw, bh, self.COLOR_BG_DARK, border_color, alpha=0.88)

        # Glowing left accent strip
        cv2.rectangle(frame, (bx, by), (bx + 3, by + bh), glow_color, -1)

        # Header label
        cv2.putText(frame, "ACTIVE CHORD", (bx + 10, by + 13), self.font_small, 0.28, (150, 165, 185), 1, cv2.LINE_AA)

        # Main chord title (Clean, unpixelated)
        cv2.putText(frame, chord_title, (bx + 10, by + 30), self.font, 0.46, self.COLOR_WHITE, 1, cv2.LINE_AA)

        # 5 Modern Micro LED indicator dots for fingers (Right side)
        for d_i in range(5):
            dx = bx + 95 + d_i * 9
            dy = by + 26
            is_lit = (d_i < finger_count)
            dot_c = glow_color if is_lit else (45, 50, 65)
            cv2.circle(frame, (dx, dy), 2, dot_c, -1, cv2.LINE_AA)
            if is_lit:
                cv2.circle(frame, (dx, dy), 4, tuple(int(c * 0.45) for c in dot_c), 1, cv2.LINE_AA)

    def _render_strum_gauge(self, frame: np.ndarray, strum_hand: dict, gain: float):
        """Small cyber velocity meter floating beside the right index pick."""
        tip_x, tip_y = strum_hand['index_tip']
        gx = max(20, min(frame.shape[1] - 115, tip_x + 25))
        gy = max(20, min(frame.shape[0] - 70, tip_y - 36))

        bar_w = 75
        bar_h = 8

        self._draw_glass_box(frame, gx - 4, gy - 16, bar_w + 8, bar_h + 22, self.COLOR_BG_DARK, (65, 75, 95), alpha=0.75)

        fill_w = int(bar_w * gain)
        bar_color = (0, 255, 140) if gain < 0.75 else (0, 180, 255)
        cv2.rectangle(frame, (gx, gy), (gx + fill_w, gy + bar_h), bar_color, -1)
        cv2.rectangle(frame, (gx, gy), (gx + bar_w, gy + bar_h), (100, 105, 120), 1)

        cv2.putText(frame, f"PICK {int(gain*100)}%", (gx, gy - 4), self.font_small, 0.34, (220, 230, 255), 1, cv2.LINE_AA)

    def _render_rhythm_telemetry(self, frame: np.ndarray, width: int, height: int, rm):
        """Floating scoreboard card for Guitar Hero rhythm mode."""
        panel_w = 200
        panel_h = 120
        panel_x = width - panel_w - 18
        panel_y = 60

        self._draw_glass_box(frame, panel_x, panel_y, panel_w, panel_h, self.COLOR_BG_DARK, self.COLOR_MAGENTA, alpha=0.85)

        cv2.putText(frame, "SCORE", (panel_x + 12, panel_y + 18), self.font_small, 0.42, (170, 175, 190), 1, cv2.LINE_AA)
        cv2.putText(frame, f"{rm.score:,}", (panel_x + 12, panel_y + 46), self.font, 0.85, self.COLOR_GOLD, 2, cv2.LINE_AA)
        cv2.putText(frame, f"COMBO: {rm.combo}", (panel_x + 12, panel_y + 72), self.font, 0.54, self.COLOR_WHITE, 2, cv2.LINE_AA)
        cv2.putText(frame, f"{rm.multiplier}X", (panel_x + panel_w - 46, panel_y + 72), self.font, 0.74, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"P:{rm.perfect_count}  G:{rm.good_count}  M:{rm.miss_count}", (panel_x + 12, panel_y + 102), self.font_small, 0.42, (160, 255, 160), 1, cv2.LINE_AA)

    def _render_mode_pill(self, frame: np.ndarray, width: int, height: int, rhythm_manager):
        """Compact frosted glass pill switcher pinned cleanly at Bottom-Left (200 x 30 px)."""
        is_rhythm = rhythm_manager and rhythm_manager.is_active
        pill_w = 200
        pill_h = 30
        pill_x = 20
        pill_y = height - pill_h - 16

        self.mode_pill_rect = (pill_x, pill_y, pill_w, pill_h)

        border_c = (230, 0, 255) if is_rhythm else (0, 255, 140)
        self._draw_glass_box(frame, pill_x, pill_y, pill_w, pill_h, self.COLOR_BG_DARK, border_c, alpha=0.88)

        if is_rhythm:
            text = "HERO RHYTHM"
            col = (230, 0, 255)
        else:
            text = "FREE PLAY"
            col = (0, 255, 140)

        # Left glowing status dot
        cv2.circle(frame, (pill_x + 14, pill_y + pill_h // 2), 4, col, -1, cv2.LINE_AA)
        cv2.circle(frame, (pill_x + 14, pill_y + pill_h // 2), 6, tuple(int(c * 0.4) for c in col), 1, cv2.LINE_AA)

        # Mode label
        cv2.putText(frame, text, (pill_x + 26, pill_y + 20), self.font_small, 0.38, (240, 245, 255), 1, cv2.LINE_AA)

        # Shortcut hint [M]
        cv2.putText(frame, "[M]", (pill_x + pill_w - 32, pill_y + 20), self.font_small, 0.34, col, 1, cv2.LINE_AA)

    def _render_power_dial(self, frame: np.ndarray, width: int, height: int, power_level: float):
        """
        Image 3: Compact Studio Rotary Power Dial (145 x 62 px) tucked into bottom-right corner.
        """
        pw, ph = 145, 62
        px = width - pw - 10
        py = height - ph - 10

        border_c = (0, 215, 255) if power_level >= 0.85 else ((0, 240, 255) if power_level >= 0.60 else (70, 80, 110))
        self._draw_glass_box(frame, px, py, pw, ph, self.COLOR_BG_DARK, border_c, alpha=0.86)

        # Header title
        cv2.putText(frame, "AMP POWER", (px + 8, py + 13), self.font_small, 0.32, (160, 175, 200), 1, cv2.LINE_AA)

        # Rotary Knob Center
        cx = px + 24
        cy = py + 36
        radius = 16
        self.dial_center = (cx, cy)
        self.dial_radius = radius

        # Dark dial body
        cv2.circle(frame, (cx, cy), radius, (28, 30, 42), -1)
        cv2.circle(frame, (cx, cy), radius, (70, 80, 105), 1, cv2.LINE_AA)

        # Neon power arc
        arc_end_deg = 135.0 + 270.0 * float(power_level)
        cv2.ellipse(frame, (cx, cy), (radius - 2, radius - 2), 0, 135, int(arc_end_deg), border_c, 2, cv2.LINE_AA)

        # Rotating needle pointer
        rad_needle = math.radians(arc_end_deg)
        nx = int(cx + (radius - 4) * math.cos(rad_needle))
        ny = int(cy + (radius - 4) * math.sin(rad_needle))
        cv2.line(frame, (cx, cy), (nx, ny), (255, 255, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, (nx, ny), 2, (0, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 3, (40, 45, 60), -1)

        # Digital readout & tone character
        pct = int(power_level * 100)
        cv2.putText(frame, f"{pct}%", (px + 46, py + 31), self.font, 0.52, self.COLOR_WHITE, 2, cv2.LINE_AA)

        mode_str = "OD" if power_level >= 0.85 else ("CRUNCH" if power_level >= 0.60 else "CLEAN")
        mode_col = self.COLOR_GOLD if power_level >= 0.85 else ((0, 255, 255) if power_level >= 0.60 else self.COLOR_CYAN)
        cv2.putText(frame, mode_str, (px + 46, py + 45), self.font_small, 0.30, mode_col, 1, cv2.LINE_AA)

        # Compact Clickable [-] and [+] Buttons (20 x 20 px)
        btn_y = py + 19
        btn_w, btn_h = 20, 20
        bx_minus = px + 94
        bx_plus = px + 118

        self.btn_minus_rect = (bx_minus, btn_y, btn_w, btn_h)
        self.btn_plus_rect = (bx_plus, btn_y, btn_w, btn_h)

        self._draw_glass_box(frame, bx_minus, btn_y, btn_w, btn_h, (25, 28, 40), (80, 95, 125), alpha=0.9)
        cv2.putText(frame, "-", (bx_minus + 6, btn_y + 14), self.font, 0.50, (220, 230, 255), 2, cv2.LINE_AA)

        self._draw_glass_box(frame, bx_plus, btn_y, btn_w, btn_h, (25, 28, 40), (80, 95, 125), alpha=0.9)
        cv2.putText(frame, "+", (bx_plus + 4, btn_y + 14), self.font, 0.50, (220, 230, 255), 2, cv2.LINE_AA)

        cv2.putText(frame, "Wheel / [ [ / ] ]", (px + 46, py + 56), self.font_small, 0.25, (130, 140, 160), 1, cv2.LINE_AA)

    def handle_mode_click(self, x: int, y: int) -> bool:
        """Returns True if the bottom mode pill was clicked."""
        if hasattr(self, 'mode_pill_rect'):
            px, py, pw, ph = self.mode_pill_rect
            return px <= x <= px + pw and py <= y <= py + ph
        return False

    def handle_click(self, x: int, y: int, current_power: float) -> Optional[float]:
        """Handles mouse click events on the dial or buttons."""
        if hasattr(self, 'btn_minus_rect'):
            bx, by, bw, bh = self.btn_minus_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                return float(np.clip(current_power - 0.05, 0.10, 1.0))

        if hasattr(self, 'btn_plus_rect'):
            bx, by, bw, bh = self.btn_plus_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                return float(np.clip(current_power + 0.05, 0.10, 1.0))

        if hasattr(self, 'dial_center'):
            cx, cy = self.dial_center
            dist = np.hypot(x - cx, y - cy)
            if dist <= self.dial_radius + 10:
                ang = math.degrees(math.atan2(y - cy, x - cx))
                if ang < 0:
                    ang += 360.0
                if 135.0 <= ang <= 360.0:
                    norm = (ang - 135.0) / 270.0
                elif 0.0 <= ang <= 45.0:
                    norm = (ang + 360.0 - 135.0) / 270.0
                else:
                    norm = current_power
                return float(np.clip(norm, 0.10, 1.0))

        return None

    def handle_scroll(self, direction: int, current_power: float) -> float:
        """Handles mouse wheel scrolling to adjust power smoothly."""
        return float(np.clip(current_power + 0.05 * direction, 0.10, 1.0))
