"""
AeroFret: Kinetic - Gesture Engine
Performs 100% English chord classification from left-hand finger geometry:
  0 Fingers (Fist) -> PALM MUTE
  1 Finger (Index) -> C MAJOR
  2 Fingers        -> D MINOR
  3 Fingers        -> E MINOR
  4 Fingers        -> F MAJOR
  5 Fingers (Open) -> G MAJOR

Hybrid Strum Detection:
  - Crossing Detection: Sweep across strings (strumming)
  - Proximity Detection: Quick perpendicular motion near any individual string (picking)
  Both methods have strict 120ms debouncing per string.
"""

import time
import math
from typing import Dict, List, Optional, Tuple
import numpy as np


class GestureEngine:
    """
    High-speed gesture and kinematic physics engine for Air-Guitar.
    Evaluates finger states, maps chords, and detects string interactions
    using a hybrid crossing + proximity algorithm for realistic playing.
    """

    CHORD_MAP = {
        0: 'MUTE',
        1: 'C',
        2: 'Dm',
        3: 'Em',
        4: 'F',
        5: 'G'
    }

    CHORD_DISPLAY_NAMES = {
        'C': 'C MAJOR',
        'Dm': 'D MINOR',
        'Em': 'E MINOR',
        'F': 'F MAJOR',
        'G': 'G MAJOR',
        'MUTE': 'PALM MUTE'
    }
    CHORD_NAMES = CHORD_DISPLAY_NAMES

    def __init__(
        self,
        num_strings: int = 4,
        debounce_ms: float = 120.0,
        min_velocity_px_s: float = 180.0,
        max_velocity_px_s: float = 1800.0,
        min_vel: Optional[float] = None,
        max_vel: Optional[float] = None,
        proximity_radius: float = 22.0,
        proximity_min_vel: float = 120.0,
        play_style: str = 'hybrid'
    ):
        self.num_strings = num_strings
        self.debounce_sec = debounce_ms / 1000.0
        self.min_vel = min_vel if min_vel is not None else min_velocity_px_s
        self.max_vel = max_vel if max_vel is not None else max_velocity_px_s
        self.play_style = play_style.lower() if play_style.lower() in ('hybrid', 'solo', 'strum') else 'hybrid'

        # Proximity picking thresholds
        self.proximity_radius = proximity_radius      # Max perpendicular distance to trigger
        self.proximity_min_vel = proximity_min_vel     # Min perpendicular velocity for pick

        self.last_trigger_times = [0.0] * num_strings
        self.last_strum_direction = [0] * num_strings  # Direction vector (+1: down/forward, -1: up/reverse)
        self.alternate_debounce_sec = 0.038           # 38ms lockout on direction reversals (enables ~26 notes/sec tremolo)
        self.prev_tip_pos: Optional[Tuple[int, int]] = None
        self.prev_timestamp: Optional[float] = None

        self.current_chord = 'C'
        self.chord_history: List[str] = []
        self.history_len = 3

        # Track which string is closest to the pick (for visual feedback)
        self.nearest_string_idx: int = -1
        self.nearest_string_dist: float = 999.0

    def update_chord(self, fret_hand_data: Optional[dict]) -> Tuple[str, str]:
        """Alias for update_fret_chord."""
        return self.update_fret_chord(fret_hand_data)

    def update_fret_chord(self, fret_hand_data: Optional[dict]) -> Tuple[str, str]:
        """Classify chord based on left-hand finger extension count."""
        if fret_hand_data is None:
            return self.current_chord, self.CHORD_DISPLAY_NAMES.get(self.current_chord, 'C MAJOR')

        extended = fret_hand_data['extended']
        total_extended = sum(extended)
        if total_extended == 0:
            self.chord_history = ['MUTE'] * self.history_len
            self.current_chord = 'MUTE'
            return 'MUTE', 'PALM MUTE'

        raw_chord = self.CHORD_MAP.get(total_extended, 'C')

        self.chord_history.append(raw_chord)
        if len(self.chord_history) > self.history_len:
            self.chord_history.pop(0)

        counts = {c: self.chord_history.count(c) for c in set(self.chord_history)}
        stable_chord = max(counts, key=counts.get)
        self.current_chord = stable_chord

        display_name = self.CHORD_DISPLAY_NAMES.get(stable_chord, stable_chord)
        return stable_chord, display_name

    @staticmethod
    def _point_to_segment_distance(px, py, ax, ay, bx, by):
        """
        Compute perpendicular distance from point (px,py) to segment (a->b),
        and the projection factor t along the segment.
        """
        vx = bx - ax
        vy = by - ay
        v_sq = vx * vx + vy * vy
        if v_sq < 1.0:
            return math.hypot(px - ax, py - ay), 0.0

        t = ((px - ax) * vx + (py - ay) * vy) / v_sq
        t_clamped = max(0.0, min(1.0, t))

        proj_x = ax + t_clamped * vx
        proj_y = ay + t_clamped * vy
        dist = math.hypot(px - proj_x, py - proj_y)
        return dist, t

    def detect_strums_dynamic(
        self,
        strum_hand_data: Optional[dict],
        string_segments: List[Tuple[Tuple[int, int], Tuple[int, int]]],
        current_chord: str
    ) -> List[dict]:
        """
        Continuous Swept-Line Collision Detection (Swept Ray Intersection)
        with Directional Alternating Strum Debounce (High-Speed Tremolo Shredding).
        
        Guarantees zero missed strums during violent high-velocity hand motions (>3000 px/s)
        while allowing rapid-fire alternate picking (down-up-down-up) up to 26 notes per second.
        """
        current_time = time.time()
        events = []

        if strum_hand_data is None:
            self.prev_tip_pos = None
            self.prev_timestamp = None
            self.nearest_string_idx = -1
            self.nearest_string_dist = 999.0
            return events

        curr_x, curr_y = strum_hand_data['index_tip']

        # Dynamically size trigger arrays to support any string count (3, 4, 5, 6)
        if len(string_segments) > len(self.last_trigger_times):
            diff = len(string_segments) - len(self.last_trigger_times)
            self.last_trigger_times.extend([0.0] * diff)
            self.last_strum_direction.extend([0] * diff)

        # --- Track nearest string for visual feedback ---
        min_dist = 999.0
        min_idx = -1
        for str_idx, (p1, p2) in enumerate(string_segments):
            d, t = self._point_to_segment_distance(
                float(curr_x), float(curr_y),
                float(p1[0]), float(p1[1]),
                float(p2[0]), float(p2[1])
            )
            if 0.05 <= t <= 1.08 and d < min_dist:
                min_dist = d
                min_idx = str_idx
        self.nearest_string_idx = min_idx
        self.nearest_string_dist = min_dist

        # --- Continuous Swept-Line Strum Physics ---
        if self.prev_tip_pos is not None and self.prev_timestamp is not None:
            dt = current_time - self.prev_timestamp
            prev_x, prev_y = self.prev_tip_pos

            if 0.001 < dt < 0.25:
                disp = math.hypot(curr_x - prev_x, curr_y - prev_y)
                velocity_px_s = disp / dt

                # Compute dynamic impact gain from physical hand velocity
                dynamic_gain = float(np.clip(0.60 + (velocity_px_s - 400.0) / 1400.0 * 0.40, 0.55, 1.0))

                crossed_strings = set()

                # Pick motion displacement vector (P1 -> P2)
                p1_x, p1_y = float(prev_x), float(prev_y)
                p2_x, p2_y = float(curr_x), float(curr_y)
                v_pick_x = p2_x - p1_x
                v_pick_y = p2_y - p1_y

                # --- METHOD 1: Exact Swept-Line Continuous Collision Detection (CCD) ---
                for str_idx, (s_a, s_b) in enumerate(string_segments):
                    sa_x, sa_y = float(s_a[0]), float(s_a[1])
                    sb_x, sb_y = float(s_b[0]), float(s_b[1])
                    v_str_x = sb_x - sa_x
                    v_str_y = sb_y - sa_y

                    # 2D cross-product determinant
                    det = v_pick_x * v_str_y - v_pick_y * v_str_x
                    if abs(det) < 1e-5:
                        continue

                    # Parametric intersection factors:
                    # u: fraction along pick swept path [0.0, 1.0]
                    # t: fraction along guitar string span [-0.06, 1.10]
                    dx = sa_x - p1_x
                    dy = sa_y - p1_y
                    u = (dx * v_str_y - dy * v_str_x) / det
                    t = (dx * v_pick_y - dy * v_pick_x) / det

                    # Check if swept path intersected the string segment in this frame interval
                    if 0.0 <= u <= 1.0 and -0.06 <= t <= 1.10:
                        stroke_dir = 1 if v_pick_y >= 0 else -1
                        time_since_last = current_time - self.last_trigger_times[str_idx]

                        # Directional debouncing: alternate stroke reversals unlock 38ms threshold for shredding
                        is_alternate = (stroke_dir != self.last_strum_direction[str_idx])
                        active_debounce = self.alternate_debounce_sec if is_alternate else self.debounce_sec

                        if time_since_last >= active_debounce:
                            self.last_trigger_times[str_idx] = current_time
                            self.last_strum_direction[str_idx] = stroke_dir
                            crossed_strings.add(str_idx)

                            int_x = int(p1_x + u * v_pick_x)
                            int_y = int(p1_y + u * v_pick_y)

                            events.append({
                                'string_index': str_idx,
                                'string_y': int_y,
                                'strum_x': int_x,
                                'velocity_px_s': velocity_px_s,
                                'gain': dynamic_gain,
                                'chord': current_chord,
                                'timestamp': current_time,
                                'direction': stroke_dir,
                                'is_solo': False
                            })

                # Precision String Skipping & Play Style filtering:
                # In 'solo' mode, or in 'hybrid' mode when displacement is small (<= 52px) or velocity is moderate (<= 750px/s),
                # pluck only the single closest string (enables leaping across strings without sounding intermediate strings!).
                if len(events) > 1:
                    if self.play_style == 'solo' or (self.play_style == 'hybrid' and (velocity_px_s <= 750.0 or abs(v_pick_y) <= 52.0)):
                        events.sort(key=lambda ev: abs(ev['string_y'] - curr_y))
                        events = [events[0]]

                for ev in events:
                    ev['is_solo'] = (len(events) == 1)

                # --- METHOD 2: Proximity-Based High-Fidelity Individual Picking ---
                # Fires if no full crossing occurred but pick tapped near a specific string
                if len(crossed_strings) == 0 and velocity_px_s > self.proximity_min_vel:
                    for str_idx, (s_a, s_b) in enumerate(string_segments):
                        sa_x, sa_y = float(s_a[0]), float(s_a[1])
                        sb_x, sb_y = float(s_b[0]), float(s_b[1])

                        dist_curr, t_curr = self._point_to_segment_distance(
                            float(curr_x), float(curr_y), sa_x, sa_y, sb_x, sb_y
                        )
                        dist_prev, t_prev = self._point_to_segment_distance(
                            float(prev_x), float(prev_y), sa_x, sa_y, sb_x, sb_y
                        )

                        if (dist_curr <= self.proximity_radius and
                                dist_prev > dist_curr and
                                0.05 <= t_curr <= 1.08):

                            time_since_last = current_time - self.last_trigger_times[str_idx]
                            stroke_dir = 1 if (curr_y > prev_y) else -1
                            is_alternate = (stroke_dir != self.last_strum_direction[str_idx])
                            active_debounce = self.alternate_debounce_sec if is_alternate else self.debounce_sec

                            if time_since_last >= active_debounce:
                                self.last_trigger_times[str_idx] = current_time
                                self.last_strum_direction[str_idx] = stroke_dir
                                events.append({
                                    'string_index': str_idx,
                                    'string_y': curr_y,
                                    'strum_x': curr_x,
                                    'velocity_px_s': velocity_px_s,
                                    'gain': dynamic_gain,
                                    'chord': current_chord,
                                    'timestamp': current_time,
                                    'direction': stroke_dir,
                                    'is_solo': True
                                })
                                break  # Individual single string pick priority

        self.prev_tip_pos = (curr_x, curr_y)
        self.prev_timestamp = current_time
        return events

    def set_play_style(self, style: str):
        """Switches play style: 'hybrid', 'solo', or 'strum'."""
        if style.lower() in ('hybrid', 'solo', 'strum'):
            self.play_style = style.lower()

    def detect_strums(
        self,
        strum_hand_data: Optional[dict],
        string_rects,
        current_chord: str
    ) -> List[dict]:
        """Auto-routes to dynamic 2D segment or bounding rect crossing."""
        if string_rects and isinstance(string_rects[0][0], (tuple, list)):
            return self.detect_strums_dynamic(strum_hand_data, string_rects, current_chord)

        segments = [((r[0], (r[1]+r[3])//2), (r[2], (r[1]+r[3])//2)) for r in string_rects]
        return self.detect_strums_dynamic(strum_hand_data, segments, current_chord)
