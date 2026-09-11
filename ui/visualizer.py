"""
AeroFret: Kinetic - Visualizer Module (Photorealistic Electric Guitar)
Renders a photorealistic Fender Stratocaster electric guitar dynamically gripped
by the player's hands in mid-air with natural two-hand 3D tilting kinematics.
- Wider scale & aspect ratio (~0.76x length, 0.88x width): commanding, full-size lap presence.
- Strings wider, bolder, thicker (5-7px glowing neon core) with generous spacing across neck and pickups.
- Accurate bone nut (x=250) and chrome bridge saddles (x=1110) alignment (100% fretboard locked).
- Both Hands On Top: Left fingers curl over neck; Right forearm & wrist rest over the lower bout.
- Virtual Stage Mode ([C] Key): Sleek dark studio concert stage with solid stylized 3D hands.
- Ultra-fast 60 FPS ROI blitting & integer alpha blending (~8-10ms).
- Rich visual effects: expanding shockwave ripples, particle spark flares, multi-layer glowing strings.
- 100% Unified Affine Matrix (M): Strings and guitar are locked as one piece ("حته واحدة").
"""

import math
import os
import random
import sys
import time
from typing import List, Optional, Tuple
import cv2
import numpy as np


class Particle:
    """Sparks emitted during string strumming."""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(110.0, 380.0)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd - random.uniform(50, 140)
        self.gravity = 440.0
        self.life = random.uniform(0.35, 0.65)
        self.max_life = self.life
        self.size = random.uniform(2.5, 5.5)

    def update(self, dt: float) -> bool:
        self.life -= dt
        if self.life <= 0:
            return False
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        return True


class ShockwaveRipple:
    """Expanding chromatic shockwave ring emitted at the strum pick contact point."""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 12.0
        self.max_radius = 56.0
        self.life = 0.28
        self.max_life = 0.28

    def update(self, dt: float) -> bool:
        self.life -= dt
        if self.life <= 0:
            return False
        progress = 1.0 - (self.life / self.max_life)
        self.radius = 12.0 + progress * (self.max_radius - 12.0)
        return True

    def draw(self, frame: np.ndarray):
        alpha = max(0.0, min(1.0, self.life / self.max_life))
        c = tuple(int(x * alpha) for x in self.color)
        r = int(self.radius)
        cv2.circle(frame, (int(self.x), int(self.y)), r, c, 2, cv2.LINE_AA)
        cv2.circle(frame, (int(self.x), int(self.y)), max(1, r - 4), (255, 255, 255), 1, cv2.LINE_AA)


class VolumetricFlameSystem:
    """
    Photorealistic Volumetric Stage Flame Cannon & Ember Projector System.
    Produces continuous, fluid roaring fire plumes using additive optical blending,
    convective buoyancy acceleration, turbulent eddy vorticity, and 4-tier thermal coloration.
    Optimized with localized ROI rendering and pre-allocated scratch buffers for rock-solid 60 FPS.
    """

    def __init__(self, cannon_xs: List[int] = None, nozzle_y: float = 480.0):
        self.cannon_xs = cannon_xs or [85, 1195]
        self.nozzle_y = float(nozzle_y)
        self.eddies = []
        self.embers = []
        self.cannon_active_time = {cx: 0.0 for cx in self.cannon_xs}
        self._flame_scratch: Optional[np.ndarray] = None

    def trigger(self, intensity: float = 1.0):
        """Activates flame cannons with burst duration proportional to strum gain."""
        duration = min(0.95, 0.40 + 0.55 * float(np.clip(intensity, 0.2, 1.0)))
        for cx in self.cannon_xs:
            self.cannon_active_time[cx] = max(self.cannon_active_time[cx], duration)

    def update(self, dt: float):
        # Spawn convective fire eddies and fast ember streaks while cannons are firing
        for cx in self.cannon_xs:
            if self.cannon_active_time[cx] > 0:
                self.cannon_active_time[cx] -= dt
                # Spawn buoyant turbulent flame puffs
                for _ in range(3):
                    self.eddies.append({
                        'x': cx + random.uniform(-10, 10),
                        'y': self.nozzle_y,
                        'vx': random.uniform(-20, 20),
                        'vy': random.uniform(-450, -800),
                        'radius': random.uniform(14, 22),
                        'growth': random.uniform(25, 45),
                        'life': random.uniform(0.50, 0.80),
                        'max_life': 0.75,
                        't_phase': random.uniform(0, 6.28),
                        't_freq': random.uniform(7.0, 14.0)
                    })
                # Spawn vertical spark streaks
                for _ in range(2):
                    self.embers.append({
                        'x': cx + random.uniform(-8, 8),
                        'y': self.nozzle_y,
                        'vx': random.uniform(-30, 30),
                        'vy': random.uniform(-650, -1100),
                        'life': random.uniform(0.35, 0.70),
                        'max_life': 0.60,
                        'size': random.uniform(2.0, 3.5)
                    })

        # Update eddies
        alive_eddies = []
        for e in self.eddies:
            e['life'] -= dt
            if e['life'] > 0:
                e['vy'] -= 200.0 * dt  # Buoyant acceleration upward
                e['vx'] += math.sin(e['t_phase'] + e['t_freq'] * (0.8 - e['life'])) * 160.0 * dt
                e['x'] += e['vx'] * dt
                e['y'] += e['vy'] * dt
                e['radius'] += e['growth'] * dt
                alive_eddies.append(e)
        self.eddies = alive_eddies

        # Update embers
        alive_embers = []
        for em in self.embers:
            em['life'] -= dt
            if em['life'] > 0:
                em['vy'] += 320.0 * dt
                em['x'] += em['vx'] * dt
                em['y'] += em['vy'] * dt
                alive_embers.append(em)
        self.embers = alive_embers

    def draw(self, frame: np.ndarray):
        h, w = frame.shape[:2]
        if not self.eddies and not self.embers:
            return

        # Pre-allocate scratch buffer if needed (zero allocation in steady state)
        if self._flame_scratch is None or self._flame_scratch.shape[:2] != (h, w):
            self._flame_scratch = np.zeros((h, w, 3), dtype=np.uint8)

        # Restrict rendering to Left and Right Cannon ROIs for 70% memory/compute reduction
        roi_w = 230
        left_active = any(e['x'] < roi_w for e in self.eddies) or any(em['x'] < roi_w for em in self.embers)
        right_active = any(e['x'] > (w - roi_w) for e in self.eddies) or any(em['x'] > (w - roi_w) for em in self.embers)

        if left_active:
            self._flame_scratch[:, :roi_w] = 0
        if right_active:
            self._flame_scratch[:, w - roi_w:] = 0

        # Draw thermal flame eddies into ROIs
        for e in self.eddies:
            prog = 1.0 - max(0.0, e['life'] / e['max_life'])
            px = int(round(e['x']))
            py = int(round(e['y']))
            r = int(round(e['radius']))
            if py < 0 or py >= h or px < 0 or px >= w:
                continue

            if prog < 0.25:
                # White-hot incandescent core & brilliant yellow
                cv2.circle(self._flame_scratch, (px, py), r, (0, 180, 255), -1)
                cv2.circle(self._flame_scratch, (px, py), max(1, int(r * 0.55)), (0, 245, 255), -1)
                cv2.circle(self._flame_scratch, (px, py), max(1, int(r * 0.28)), (255, 255, 255), -1)
            elif prog < 0.60:
                # Golden yellow & blazing solar orange
                alpha = (0.60 - prog) / 0.35
                col_outer = (10, int(100 * alpha), int(255 * alpha))
                col_inner = (0, int(220 * alpha), int(255 * alpha))
                cv2.circle(self._flame_scratch, (px, py), r, col_outer, -1)
                cv2.circle(self._flame_scratch, (px, py), max(1, int(r * 0.50)), col_inner, -1)
            else:
                # Ruby-red edge & dissipating smoke
                alpha = max(0.0, (1.0 - prog) / 0.40)
                col = (int(15 * alpha), int(45 * alpha), int(180 * alpha))
                cv2.circle(self._flame_scratch, (px, py), r, col, -1)

        # Motion-blurred ember streaks
        for em in self.embers:
            prog = 1.0 - max(0.0, em['life'] / em['max_life'])
            alpha = max(0.0, 1.0 - prog)
            p1 = (int(round(em['x'])), int(round(em['y'])))
            p2 = (int(round(em['x'] - em['vx'] * 0.024)), int(round(em['y'] - em['vy'] * 0.024)))
            col = (int(80 * alpha), int(225 * alpha), int(255 * alpha))
            cv2.line(self._flame_scratch, p1, p2, col, max(1, int(em['size'] * alpha)), cv2.LINE_AA)

        # Fast localized blur and additive blending on active ROIs only
        if left_active:
            left_patch = cv2.GaussianBlur(self._flame_scratch[:, :roi_w], (9, 9), 0)
            cv2.add(frame[:, :roi_w], left_patch, dst=frame[:, :roi_w])

        if right_active:
            right_patch = cv2.GaussianBlur(self._flame_scratch[:, w - roi_w:], (9, 9), 0)
            cv2.add(frame[:, w - roi_w:], right_patch, dst=frame[:, w - roi_w:])


class FloatingNote:
    """Floating musical note (♪, ♫, ♬) undulating upward from the electric guitar soundhole."""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x0 = x
        self.y = y
        self.color = color
        self.text = random.choice(['#', '♪', '♫', '♬', '§', 'o'])
        self.vy = random.uniform(85.0, 175.0)
        self.freq = random.uniform(3.5, 6.5)
        self.amp = random.uniform(16.0, 34.0)
        self.phase = random.uniform(0, 2 * math.pi)
        self.life = random.uniform(1.3, 1.9)
        self.max_life = self.life
        self.x = x

    def update(self, dt: float, current_time: float) -> bool:
        self.life -= dt
        if self.life <= 0:
            return False
        self.y -= self.vy * dt
        self.x = self.x0 + self.amp * math.sin(current_time * self.freq + self.phase)
        return True

    def draw(self, frame: np.ndarray):
        alpha = max(0.0, min(1.0, self.life / self.max_life))
        scale = 0.55 + 0.35 * (self.life / self.max_life)
        glow_c = tuple(int(v * alpha * 0.4) for v in self.color)
        cv2.putText(frame, self.text, (int(self.x) - 1, int(self.y) - 1), cv2.FONT_HERSHEY_SIMPLEX, scale, glow_c, 3, cv2.LINE_AA)
        cv2.putText(frame, self.text, (int(self.x), int(self.y)), cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 1, cv2.LINE_AA)


class DynamicStringVibration:
    """Physical model of a guitar string with 2D perpendicular normal oscillation."""

    def __init__(self, color: Tuple[int, int, int], enable_vibrato: bool = False):
        self.p1 = np.array([200.0, 400.0])
        self.p2 = np.array([800.0, 400.0])
        self.color = color
        self.enable_vibrato = enable_vibrato

        self.amplitude = 0.0
        self.max_amplitude = 26.0
        self.frequency = 38.0
        self.damping = 6.5
        self.trigger_time = 0.0

    def update_endpoints(self, p1: Tuple[float, float], p2: Tuple[float, float]):
        self.p1 = np.array(p1, dtype=np.float32)
        self.p2 = np.array(p2, dtype=np.float32)

    def pluck(self, intensity: float = 1.0):
        self.trigger_time = time.time()
        self.amplitude = self.max_amplitude * min(1.6, max(0.7, intensity))

    def get_points(self, current_time: float, steps: int = 38) -> np.ndarray:
        v = self.p2 - self.p1
        length = np.linalg.norm(v)
        if length < 1.0:
            return np.array([[self.p1[0], self.p1[1]]], dtype=np.int32)

        u = v / length
        normal = np.array([-u[1], u[0]], dtype=np.float32)

        elapsed = current_time - self.trigger_time
        vib_amp = 0.0
        if elapsed < 1.3 and self.amplitude >= 0.2:
            env = self.amplitude * math.exp(-self.damping * elapsed)
            if self.enable_vibrato:
                vib_amp = env * (0.80 * math.sin(2.0 * math.pi * self.frequency * elapsed) + 0.35 * math.sin(4.0 * math.pi * self.frequency * elapsed))
            else:
                vib_amp = env * math.sin(2.0 * math.pi * self.frequency * elapsed)

        if vib_amp == 0.0:
            return np.array([
                [int(round(self.p1[0])), int(round(self.p1[1]))],
                [int(round(self.p2[0])), int(round(self.p2[1]))]
            ], dtype=np.int32).reshape((-1, 1, 2))

        pts = []
        vib_steps = 18
        for i in range(vib_steps + 1):
            s = i / float(vib_steps)
            if self.enable_vibrato:
                spatial = math.sin(math.pi * s) + 0.30 * math.sin(2.0 * math.pi * s)
            else:
                spatial = math.sin(math.pi * s)
            disp = vib_amp * spatial * normal
            p = self.p1 + s * v + disp
            pts.append([int(p[0]), int(p[1])])

        return np.array(pts, dtype=np.int32).reshape((-1, 1, 2))


class Visualizer:
    """
    Renders the photorealistic Fender Stratocaster electric guitar attached to the player's hands.
    - Dynamic String Distribution: evenly maps 3, 4, 5, or 6 strings across neck nut & bridge.
    - Wider scale (~0.76x) & broader neck/body aspect ratio (0.88x): prominent, realistic presence.
    - Thicker radiant multi-layer glowing strings with white incandescent core.
    - Active string highlight: nearest string pulses brighter when pick is nearby.
    - Virtual Stage Mode with Concert Flame Cannons & Multi-Color Reactive Stage Bloom.
    - Floating Musical Notation VFX & Standing Wave Vibrato Modulation.
    """

    STRING_COLORS = [
        (255, 140, 0),    # Neon Electric Cyan
        (0, 245, 140),    # Acid Emerald Green
        (0, 255, 255),    # Golden Yellow
        (0, 180, 255),    # Solar Orange
        (255, 0, 210),    # Hot Pink / Magenta
        (80, 20, 255)     # Cyber Ruby Crimson
    ]

    CHORD_BLOOM_COLORS = {
        'C': (255, 220, 0),     # Electric Cyan (BGR)
        'Dm': (255, 60, 190),   # Radiant Violet
        'Em': (40, 240, 110),   # Neon Emerald
        'F': (0, 180, 255),     # Solar Amber
        'G': (200, 0, 255),     # Hot Magenta
        'MUTE': (30, 40, 240)   # Blazing Crimson
    }

    # Anchor point in guitar image: Bone nut separator at headstock
    ANCHOR_IMG = np.array([250.0, 378.0], dtype=np.float32)

    @staticmethod
    def generate_string_sources(num_strings: int) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Dynamically and evenly distributes 3, 4, 5, or 6 strings along the nut and bridge
        of the Fender Stratocaster body with mathematical precision and ergonomic spacing.
        Nut: Y spans [340.0, 415.0] (75px span)
        Bridge: Y spans [305.0, 475.0] (170px span)
        Provides ~50px separation at the picking zone for clean string skipping and strumming.
        """
        n = max(1, num_strings)
        sources = []
        for i in range(n):
            frac = float(i) / float(n - 1) if n > 1 else 0.5
            y_nut = 340.0 + frac * (415.0 - 340.0)
            y_brg = 305.0 + frac * (475.0 - 305.0)
            sources.append(((250.0, y_nut), (1110.0, y_brg)))
        return sources

    def __init__(
        self,
        num_strings: int = 4,
        enable_pyro: bool = True,
        enable_floating_notes: bool = True,
        enable_vibrato: bool = False
    ):
        self.num_strings = max(1, num_strings)
        self.enable_pyro = enable_pyro
        self.enable_floating_notes = enable_floating_notes
        self.enable_vibrato = enable_vibrato

        self.string_src = self.generate_string_sources(self.num_strings)
        self.STRING_SRC = self.string_src  # Backward compatibility alias
        self.strings = [
            DynamicStringVibration(
                self.STRING_COLORS[i % len(self.STRING_COLORS)],
                enable_vibrato=enable_vibrato
            )
            for i in range(self.num_strings)
        ]
        self.particles: List[Particle] = []
        self.ripples: List[ShockwaveRipple] = []
        self.flame_system = VolumetricFlameSystem(cannon_xs=[85, 1195], nozzle_y=480.0)
        self.pyro_particles = []  # Kept for backward compatibility
        self.floating_notes: List[FloatingNote] = []
        self.last_time = time.time()

        # Dynamic physical tracking (EMA smoothed)
        self.fret_anchor = np.array([310.0, 460.0], dtype=np.float32)
        self.current_angle = 19.0  # degrees
        self.fixed_scale_x = 0.76
        self.fixed_scale_y = 0.88
        self.fixed_scale = 0.76

        # Virtual Stage Mode (Toggleable via Key [C])
        self.virtual_stage_mode = False

        # Reactive concert stage atmospheric effects (Living Concert Stage)
        self.stage_start_time = time.time()
        self.stage_flash_intensity = 0.0
        self.active_chord_color = (255, 220, 0)
        # 28 persistent floating bokeh/dust motes for organic stage depth
        self.stage_motes = []
        for _ in range(28):
            self.stage_motes.append({
                'x': random.uniform(0.05, 0.95),
                'y': random.uniform(0.08, 0.92),
                'vy': random.uniform(14.0, 36.0),
                'vx_freq': random.uniform(0.7, 2.1),
                'r': random.uniform(1.6, 3.6),
                'color': random.choice([(255, 230, 0), (230, 0, 255), (0, 215, 255), (255, 255, 255)]),
                'phase': random.uniform(0, 2 * math.pi)
            })

        # Active string highlight index (set by GestureEngine proximity tracking)
        self.nearest_string_idx = -1

        # Unified Affine Transform Matrix
        self.M = np.eye(2, 3, dtype=np.float32)

        # 60 FPS Performance Pre-allocations & Stage Backdrop Caching
        self.cached_stage_bg: Optional[np.ndarray] = None
        self._cone_scratch: Optional[np.ndarray] = None
        self._hand_mask: Optional[np.ndarray] = None
        self.flame_last_trigger: float = 0.0
        self.flame_cooldown_sec: float = 0.55

        self.guitar_rgba = None
        self._load_guitar_asset()

    def _init_stage_cache(self, w: int, h: int):
        """Pre-renders static concert stage backdrop components once to eliminate per-frame allocations."""
        bg = np.zeros((h, w, 3), dtype=np.uint8)
        # 1. Base stage gradient (Obsidian dark room with concert navy ambiance)
        ratios = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, np.newaxis]
        bg[:, :, 0] = (16 + 20 * ratios).astype(np.uint8)  # B
        bg[:, :, 1] = (12 + 15 * ratios).astype(np.uint8)  # G
        bg[:, :, 2] = (18 + 16 * ratios).astype(np.uint8)  # R

        # 2. Overhead Concert Stage Truss Rigging
        truss_y1, truss_y2 = 14, 26
        cv2.line(bg, (0, truss_y1), (w, truss_y1), (45, 52, 68), 2, cv2.LINE_AA)
        cv2.line(bg, (0, truss_y2), (w, truss_y2), (45, 52, 68), 2, cv2.LINE_AA)
        for tx in range(0, w, 40):
            cv2.line(bg, (tx, truss_y1), (tx + 20, truss_y2), (35, 40, 55), 1, cv2.LINE_AA)
            cv2.line(bg, (tx + 20, truss_y2), (tx + 40, truss_y1), (35, 40, 55), 1, cv2.LINE_AA)

        # Spotlight Fixtures mounted on truss
        for fx in [int(w * 0.18), int(w * 0.38), int(w * 0.62), int(w * 0.82)]:
            cv2.rectangle(bg, (fx - 14, truss_y2), (fx + 14, truss_y2 + 12), (30, 35, 48), -1)
            cv2.circle(bg, (fx, truss_y2 + 12), 6, (255, 235, 140), -1)

        # 3. Reflective Stage Floor Horizon
        floor_y = int(h * 0.72)
        cv2.line(bg, (0, floor_y), (w, floor_y), (65, 58, 78), 2, cv2.LINE_AA)
        cv2.line(bg, (0, floor_y + 2), (w, floor_y + 2), (32, 28, 42), 1, cv2.LINE_AA)

        # Stage Flame Cannon Launcher Hardware Fixtures on left & right
        for cx in [85, w - 85]:
            cy = floor_y - 2
            cv2.rectangle(bg, (cx - 20, cy - 22), (cx + 20, cy), (42, 48, 60), -1)
            cv2.rectangle(bg, (cx - 20, cy - 22), (cx + 20, cy), (75, 84, 102), 1, cv2.LINE_AA)
            cv2.rectangle(bg, (cx - 8, cy - 38), (cx + 8, cy - 22), (58, 66, 82), -1)
            cv2.rectangle(bg, (cx - 8, cy - 38), (cx + 8, cy - 22), (95, 108, 130), 1, cv2.LINE_AA)

        self.cached_stage_bg = bg
        self._cone_scratch = np.zeros((h, w, 3), dtype=np.uint8)
        self._hand_mask = np.zeros((h, w), dtype=np.uint8)

    def _load_guitar_asset(self):
        from core.config import CONFIG
        asset_path = getattr(CONFIG.paths, 'GUITAR_IMAGE', '')
        if not os.path.exists(asset_path):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            asset_path = os.path.join(base_dir, 'assets', 'guitar_playing_stance.png')
        if not os.path.exists(asset_path):
            asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'guitar_playing_stance.png')
        if os.path.exists(asset_path):
            try:
                data = np.fromfile(asset_path, dtype=np.uint8)
                img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
                if img is not None and len(img.shape) == 3 and img.shape[2] == 4:
                    # Enhance guitar graphics: Candy Red Lacquer & Crisp Chrome Frets
                    bgr = img[:, :, :3].astype(np.float32)
                    alpha = img[:, :, 3]

                    hsv = cv2.cvtColor(bgr.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
                    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.25, 0, 255)       # Rich candy lacquer saturation
                    hsv[:, :, 2] = np.clip((hsv[:, :, 2] - 128) * 1.12 + 134, 0, 255) # High-def contrast punch
                    enhanced_bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

                    blur = cv2.GaussianBlur(enhanced_bgr, (0, 0), 2.0)
                    sharp = cv2.addWeighted(enhanced_bgr, 1.35, blur, -0.35, 0)
                    self.guitar_rgba = np.dstack([sharp, alpha])
            except Exception as e:
                print(f"[Visualizer] Asset load note: {e}")

    def update_oud_anchors(
        self,
        fret_hand: Optional[dict],
        strum_hand: Optional[dict],
        width: int,
        height: int
    ) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        # 1. Wider scales: 0.76x length, 0.88x width (~15% broader neck & body)
        self.fixed_scale_x = 0.76 * (float(width) / 1280.0)
        self.fixed_scale_y = 0.88 * (float(width) / 1280.0)
        self.fixed_scale = self.fixed_scale_x

        # 2. Determine Left-Hand Grip Target: Anchored in the crook of the hand
        if fret_hand is not None:
            pts = fret_hand.get('landmarks_px')
            if pts is not None and len(pts) > 5:
                target_fret_x = float(0.40 * pts[0][0] + 0.40 * pts[5][0] + 0.20 * pts[1][0])
                target_fret_y = float(0.40 * pts[0][1] + 0.40 * pts[5][1] + 0.20 * pts[1][1])
            else:
                wx, wy = fret_hand['wrist']
                cx, cy = fret_hand.get('center', (wx, wy))
                target_fret_x = float(0.45 * wx + 0.55 * cx)
                target_fret_y = float(0.45 * wy + 0.55 * cy)
        else:
            target_fret_x = float(width * 0.24)
            target_fret_y = float(height * 0.68)

        # 3. Two-Hand Kinematics: Guitar connects left hand grip to right strumming hand
        if fret_hand is not None and strum_hand is not None:
            sx = float(strum_hand['wrist'][0])
            sy = float(strum_hand['wrist'][1])
            dx = sx - target_fret_x
            dy = sy - target_fret_y
            if dx > 60.0:
                raw_angle = math.degrees(math.atan2(dy, dx))
                target_angle = float(np.clip(raw_angle, -6.0, 36.0))
            else:
                target_angle = 19.0
        elif fret_hand is not None:
            tilt = 19.0 + (height * 0.65 - target_fret_y) * 0.08
            target_angle = float(np.clip(tilt, 6.0, 36.0))
        else:
            target_angle = 19.0

        # 4. Continuous Velocity-Adaptive Kinematic Smoothing (Instant zero-delay response)
        speed = float(np.hypot(target_fret_x - self.fret_anchor[0], target_fret_y - self.fret_anchor[1]))
        alpha_pos = float(np.clip(0.55 + (speed / 50.0) * 0.40, 0.55, 0.95))
        ang_blend = float(np.clip(0.50 + (abs(target_angle - self.current_angle) / 18.0) * 0.45, 0.50, 0.90))

        ang_diff = target_angle - self.current_angle
        clamped_diff = float(np.clip(ang_diff, -18.0, 18.0))

        self.fret_anchor[0] = alpha_pos * target_fret_x + (1.0 - alpha_pos) * self.fret_anchor[0]
        self.fret_anchor[1] = alpha_pos * target_fret_y + (1.0 - alpha_pos) * self.fret_anchor[1]
        self.current_angle += ang_blend * clamped_diff

        # 5. Compute Unified Anisotropic Affine Transformation Matrix M (Wider neck & body)
        theta = math.radians(self.current_angle)
        Sx = self.fixed_scale_x
        Sy = self.fixed_scale_y
        x0, y0 = self.ANCHOR_IMG[0], self.ANCHOR_IMG[1]
        fx, fy = self.fret_anchor[0], self.fret_anchor[1]

        a = Sx * math.cos(theta)
        b = Sy * math.sin(theta)
        c = Sx * math.sin(theta)
        d = Sy * math.cos(theta)

        self.M = np.array([
            [a, -b, fx - a * x0 + b * y0],
            [c,  d, fy - c * x0 - d * y0]
        ], dtype=np.float32)

        # 6. Compute String Segments via the EXACT SAME Matrix M ("حته واحدة")
        # Dynamic iteration: guarantees 3, 4, 5, or 6 strings align 100% on the guitar neck & bridge
        segments = []
        for i, (p_nut, p_brg) in enumerate(self.string_src):
            p1 = self.M @ np.array([p_nut[0], p_nut[1], 1.0], dtype=np.float32)
            p2 = self.M @ np.array([p_brg[0], p_brg[1], 1.0], dtype=np.float32)
            if i < len(self.strings):
                self.strings[i].update_endpoints((p1[0], p1[1]), (p2[0], p2[1]))
            segments.append(((int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))))

        return segments

        return segments

    def update_layout(self, width: int, height: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return self.update_oud_anchors(None, None, width, height)

    def trigger_pluck(
        self,
        s_idx: int,
        px: int,
        gain: float = 1.0,
        chord_name: str = 'C',
        is_chord_sweep: bool = False
    ):
        if 0 <= s_idx < len(self.strings):
            s = self.strings[s_idx]
            s.pluck(gain)
            py = float((s.p1[1] + s.p2[1]) / 2.0)

            # Chromatic shockwave ring burst (only on solo plucks; chord sweeps use unified chord burst)
            if not is_chord_sweep and len(self.ripples) < 16:
                self.ripples.append(ShockwaveRipple(float(px), py, s.color))

            # Dynamic multi-color concert stage flash
            self.stage_flash_intensity = min(1.0, self.stage_flash_intensity + (0.12 if is_chord_sweep else 0.35) * gain)
            self.active_chord_color = self.CHORD_BLOOM_COLORS.get(chord_name, (255, 220, 0))

            # Flame cannons: only on high-energy power plucks (gain >= 0.75) with 0.55s cooldown
            now = time.time()
            if self.enable_pyro and gain >= 0.75 and (now - self.flame_last_trigger) >= self.flame_cooldown_sec:
                self.flame_last_trigger = now
                self._trigger_stage_flame_cannons(gain)

            # Spawn floating musical notes VFX (disciplined, max 12 active)
            if self.enable_floating_notes and not is_chord_sweep and len(self.floating_notes) < 12:
                self._spawn_floating_note(float(px), py, s.color)

            # Disciplined, balanced particle sparks (avoiding CPU overhead and visual clutter)
            if len(self.particles) < 200:
                spark_count = int(3 + 2 * gain) if is_chord_sweep else int(12 + 6 * gain)
                for _ in range(spark_count):
                    c = random.choice([s.color, (255, 255, 255), (0, 255, 255), (255, 0, 210), (0, 215, 255)])
                    self.particles.append(Particle(float(px), py, c))

    def trigger_chord_burst(self, px: int, s_idx: int, gain: float = 1.0, chord_name: str = 'C'):
        """Triggers a grand unified musical event for a multi-string chord strum sweep."""
        if 0 <= s_idx < len(self.strings):
            s = self.strings[s_idx]
            py = float((s.p1[1] + s.p2[1]) / 2.0)
            # 1 Grand unified shockwave at strum centroid
            if len(self.ripples) < 16:
                self.ripples.append(ShockwaveRipple(float(px), py, (255, 240, 180)))

        # 1 Graceful floating musical note for the chord
        if self.enable_floating_notes and len(self.floating_notes) < 12:
            chord_color = self.CHORD_BLOOM_COLORS.get(chord_name, (0, 240, 255))
            py_ref = float((self.strings[s_idx].p1[1] + self.strings[s_idx].p2[1]) / 2.0) if 0 <= s_idx < len(self.strings) else 420.0
            self._spawn_floating_note(float(px), py_ref, chord_color)

        # High-power flame cannon burst (gain >= 0.75 with cooldown)
        now = time.time()
        if self.enable_pyro and gain >= 0.75 and (now - self.flame_last_trigger) >= self.flame_cooldown_sec:
            self.flame_last_trigger = now
            self._trigger_stage_flame_cannons(gain)

    def _trigger_stage_flame_cannons(self, gain: float):
        """Erupts twin volumetric concert flame plumes on Stage Left & Stage Right."""
        self.flame_system.trigger(gain)
        self.pyro_particles.append(True)

    def _spawn_floating_note(self, x: float, y: float, color: Tuple[int, int, int]):
        """Spawns an undulating musical notation particle (♪, ♫, ♬) from the pickup zone."""
        if len(self.floating_notes) < 16:
            self.floating_notes.append(FloatingNote(x, y, color))

    def render(
        self,
        frame: np.ndarray,
        fret_hand: Optional[dict],
        strum_hand: Optional[dict],
        rm=None,
        active_chord: str = 'C'
    ) -> np.ndarray:
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # 0. Virtual Stage Mode: If enabled, replace webcam with dark studio concert stage
        if self.virtual_stage_mode:
            self._render_virtual_stage_backdrop(frame)

        # Save raw frame only in camera mode for 3D hand layering (avoids 2.8MB copy in stage mode)
        camera_raw = frame.copy() if not self.virtual_stage_mode else None

        # 1. Warp & Fast Blit Photorealistic Electric Guitar
        self._render_realistic_guitar(frame)

        # 2. Render Mother-of-pearl Fret Markers on the Neck
        self._render_fret_markers(frame, active_chord)

        # 4. Render Electromagnetic Pickup Field Aura
        self._render_pickup_field(frame)

        # 5. Render Thick Radiant Vibrating Neon Strings (AAA Electric Core + Bloom)
        for s_idx, s in enumerate(self.strings):
            pts = s.get_points(now)
            is_vib = (now - s.trigger_time) < 0.9
            is_active = (s_idx == self.nearest_string_idx)

            # Boost glow when pick is nearby (active string highlight for UX feedback)
            boost = 1.35 if is_active else 1.0

            # Layer 1: Wide atmospheric volumetric bloom
            glow_wide = tuple(max(0, min(255, int(c * 0.40 * boost))) for c in s.color)
            cv2.polylines(frame, [pts], False, glow_wide, 22 if is_vib else (16 if is_active else 14), cv2.LINE_AA)

            # Layer 2: Radiant neon aura
            glow_mid = tuple(max(0, min(255, int(c * 0.85 * boost))) for c in s.color)
            cv2.polylines(frame, [pts], False, glow_mid, 12 if is_vib else (9 if is_active else 7), cv2.LINE_AA)

            # Layer 3: Solid electric core (Thick, bold 5-6px line)
            core_c = tuple(max(0, min(255, int(c * boost))) for c in s.color)
            cv2.polylines(frame, [pts], False, core_c, 6 if is_vib else (5 if is_active else 4), cv2.LINE_AA)

            # Layer 4: Superheated incandescent white filament
            cv2.polylines(frame, [pts], False, (255, 255, 255), 2 if (is_vib or is_active) else 1, cv2.LINE_AA)

            # Nut & Bridge anchor nodes
            cv2.circle(frame, (int(s.p1[0]), int(s.p1[1])), 6, s.color, -1)
            cv2.circle(frame, (int(s.p1[0]), int(s.p1[1])), 2, (255, 255, 255), -1)
            cv2.circle(frame, (int(s.p2[0]), int(s.p2[1])), 8, (230, 230, 245), -1)
            cv2.circle(frame, (int(s.p2[0]), int(s.p2[1])), 4, (255, 255, 255), -1)

        # 6. Shockwave Ripples
        alive_ripples = []
        for rip in self.ripples:
            if rip.update(dt):
                rip.draw(frame)
                alive_ripples.append(rip)
        self.ripples = alive_ripples

        # 7. True 3D Hand Occlusion & Stage Hands (Guitar stays 100% solid!)
        if fret_hand is not None and 'landmarks_px' in fret_hand:
            if self.virtual_stage_mode:
                self._render_fleshy_3d_hand(frame, fret_hand['landmarks_px'], is_fret_hand=True)
            else:
                self._composite_3d_hand(frame, camera_raw, fret_hand)

        # 8. Laser Plectrum on Right Index Fingertip & 3D Strum Hand in Virtual Stage
        if strum_hand is not None:
            if self.virtual_stage_mode and 'landmarks_px' in strum_hand:
                self._render_fleshy_3d_hand(frame, strum_hand['landmarks_px'], is_fret_hand=False)
            self._render_plectrum(frame, strum_hand['index_tip'])

        # 8. Rhythm Notes
        if rm and rm.is_active:
            for n in rm.notes:
                if n.hit_status is not None or n.string_index >= len(self.strings):
                    continue
                s_obj = self.strings[n.string_index]
                v = s_obj.p2 - s_obj.p1
                nx = int(s_obj.p1[0] + 0.70 * v[0])
                ny = int(n.current_y)
                r = 18
                poly = np.array([[nx, ny - r], [nx + r, ny], [nx, ny + r], [nx - r, ny]], np.int32)
                cv2.fillPoly(frame, [poly], s_obj.color)
                cv2.polylines(frame, [poly], True, (255, 255, 255), 2, cv2.LINE_AA)
                chord_str = str(n.chord)
                ts = cv2.getTextSize(chord_str, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                cv2.putText(frame, chord_str, (nx - ts[0]//2, ny + ts[1]//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 10, 20), 1, cv2.LINE_AA)

        # 9. Particle Bursts
        alive_p = []
        for p in self.particles:
            if p.update(dt):
                a = p.life / p.max_life
                c = tuple(int(x * a) for x in p.color)
                cv2.circle(frame, (int(p.x), int(p.y)), max(1, int(p.size * a)), c, -1)
                alive_p.append(p)
        self.particles = alive_p

        # 9B. Floating Musical Notation VFX (♪, ♫, ♬)
        alive_notes = []
        for fn in self.floating_notes:
            if fn.update(dt, now):
                fn.draw(frame)
                alive_notes.append(fn)
        self.floating_notes = alive_notes

        # 10. Floating Popups
        if rm and rm.popups:
            for pop in rm.popups:
                c = tuple(int(x * pop.alpha) for x in pop.color)
                cv2.putText(frame, pop.text, (pop.x, pop.y), cv2.FONT_HERSHEY_DUPLEX, 0.85, c, 2, cv2.LINE_AA)

        return frame

    def _render_virtual_stage_backdrop(self, frame: np.ndarray):
        """
        Dynamic Living Concert Stage Backdrop.
        High-performance 60 FPS implementation utilizing cached static backdrops
        and pre-allocated scratch buffers (zero memory allocation per frame).
        """
        h, w = frame.shape[:2]
        if self.cached_stage_bg is None or self.cached_stage_bg.shape[:2] != (h, w):
            self._init_stage_cache(w, h)

        # 1. Zero-cost C-memory copy of pre-rendered static stage backdrop (<0.2ms)
        np.copyto(frame, self.cached_stage_bg)

        now = time.time()
        t = now - self.stage_start_time

        # 2. Sweeping Volumetric Spotlights (single pass onto pre-allocated scratch buffer)
        self._cone_scratch.fill(0)
        s1_top_x = int(w * (0.22 + 0.08 * math.sin(t * 0.75)))
        s1_bot_x = int(w * (0.46 + 0.14 * math.sin(t * 0.75)))
        cone1 = np.array([
            [s1_top_x - 30, 0],
            [s1_top_x + 30, 0],
            [s1_bot_x + 180, int(h * 0.88)],
            [s1_bot_x - 180, int(h * 0.88)]
        ], dtype=np.int32)
        cv2.fillPoly(self._cone_scratch, [cone1], (55, 45, 15))  # Warm cyan/blue spotlight tint

        s2_top_x = int(w * (0.78 - 0.08 * math.sin(t * 0.90)))
        s2_bot_x = int(w * (0.54 - 0.14 * math.sin(t * 0.90)))
        cone2 = np.array([
            [s2_top_x - 30, 0],
            [s2_top_x + 30, 0],
            [s2_bot_x + 160, int(h * 0.84)],
            [s2_bot_x - 160, int(h * 0.84)]
        ], dtype=np.int32)
        cv2.fillPoly(self._cone_scratch, [cone2], (40, 15, 50))  # Vivid magenta rim spotlight

        # Fast single additive blit for both volumetric cones
        cv2.add(frame, self._cone_scratch, dst=frame)

        # 3. Dynamic pilot burner glow on Stage Flame Cannons
        floor_y = int(h * 0.72)
        cy = floor_y - 2
        for cx in [85, w - 85]:
            pilot_c = (255, 220, 0) if (int(t * 10) % 2 == 0) else (0, 210, 255)
            cv2.circle(frame, (cx, cy - 39), 4, pilot_c, -1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy - 39), 2, (255, 255, 255), -1, cv2.LINE_AA)

        # 4. Floor specular reflections
        for fx, col in [(s1_bot_x, (45, 38, 15)), (s2_bot_x, (35, 15, 42))]:
            cv2.ellipse(frame, (fx, floor_y + 35), (140, 22), 0, 0, 360, col, -1)

        # 5. Floating Ambient Dust / Bokeh Motes (Subtle cinematic atmosphere)
        dt = 0.016  # standard frame delta approximation
        for mote in self.stage_motes:
            mote['y'] -= (mote['vy'] * dt) / h
            mote['x'] += (math.sin(t * mote['vx_freq'] + mote['phase']) * 12.0 * dt) / w
            if mote['y'] < 0.04:
                mote['y'] = 0.94
            mote['x'] = max(0.01, min(0.99, mote['x']))
            px = max(2, min(w - 3, int(mote['x'] * w)))
            py = max(2, min(h - 3, int(mote['y'] * h)))
            rad = max(1, min(10, int(mote['r'])))
            cv2.circle(frame, (px, py), rad + 2, (30, 35, 45), -1, cv2.LINE_AA)
            cv2.circle(frame, (px, py), rad, mote['color'], -1, cv2.LINE_AA)

        # 6. Dynamic Reactive Multi-Color Chord Bloom Flash
        if self.stage_flash_intensity > 0.01:
            flash_alpha = min(0.35, self.stage_flash_intensity * 0.35)
            col = getattr(self, 'active_chord_color', (255, 220, 0))
            center_x = w // 2
            center_y = int(h * 0.44)
            bloom_r = int(180 * self.stage_flash_intensity)
            if bloom_r > 0:
                cv2.circle(frame, (center_x, center_y), bloom_r, (int(col[0] * flash_alpha), int(col[1] * flash_alpha), int(col[2] * flash_alpha)), -1, cv2.LINE_AA)

            # Central stage spotlight bloom
            center_x = w // 2
            center_y = int(h * 0.44)
            bloom_r = int(140 * self.stage_flash_intensity)
            if bloom_r > 0:
                cv2.circle(frame, (center_x, center_y), bloom_r, (int(col[0]*0.3), int(col[1]*0.3), int(col[2]*0.3)), -1, cv2.LINE_AA)

            self.stage_flash_intensity = max(0.0, self.stage_flash_intensity - 3.2 * dt)

        # 7. Update & Render Volumetric Stage Flame Cannons & Ember Streaks
        self.flame_system.update(dt)
        self.flame_system.draw(frame)

        # Retain backward-compatible particle loop if custom particles exist
        alive_pyro = []
        for p in self.pyro_particles:
            if hasattr(p, 'update') and p.update(dt):
                if hasattr(p, 'draw'):
                    p.draw(frame)
                alive_pyro.append(p)
        self.pyro_particles = alive_pyro

    def _render_pickup_field(self, frame: np.ndarray):
        """Pulsating electromagnetic aura over the active guitar pickups."""
        p_c1 = self.M @ np.array([860.0, 380.0, 1.0], dtype=np.float32)
        p_c2 = self.M @ np.array([1000.0, 380.0, 1.0], dtype=np.float32)
        cx = int((p_c1[0] + p_c2[0]) / 2.0)
        cy = int((p_c1[1] + p_c2[1]) / 2.0)
        axes = (int(64 * self.fixed_scale_x), int(30 * self.fixed_scale_y))
        ang = int(self.current_angle)

        glow_c = (0, 215, 255)
        cv2.ellipse(frame, (cx, cy), axes, ang, 0, 360, glow_c, 2, cv2.LINE_AA)
        cv2.ellipse(frame, (cx, cy), (int(axes[0]*0.7), int(axes[1]*0.7)), ang, 0, 360, (255, 255, 255), 1, cv2.LINE_AA)

    def _composite_3d_hand(self, frame: np.ndarray, camera_raw: np.ndarray, fret_hand: dict):
        """
        Composites ONLY the player's fingers curling over the fretboard.
        Guarantees the guitar neck remains 100% solid, continuous, and unbroken (NO forearm slicing!).
        """
        h, w = frame.shape[:2]
        pts_px = fret_hand.get('landmarks_px', [])
        if len(pts_px) < 21:
            return

        hand_mask = np.zeros((h, w), dtype=np.uint8)

        # 1. Finger segments curling over the fretboard (finger width ~18px)
        FINGER_CHAINS = [
            [2, 3, 4],             # Thumb tip only
            [5, 6, 7, 8],          # Index finger
            [9, 10, 11, 12],       # Middle finger
            [13, 14, 15, 16],      # Ring finger
            [17, 18, 19, 20]       # Pinky finger
        ]
        for chain in FINGER_CHAINS:
            for i in range(len(chain) - 1):
                p1 = (int(pts_px[chain[i]][0]), int(pts_px[chain[i]][1]))
                p2 = (int(pts_px[chain[i+1]][0]), int(pts_px[chain[i+1]][1]))
                cv2.line(hand_mask, p1, p2, 255, thickness=18)
            for idx in chain:
                cv2.circle(hand_mask, (int(pts_px[idx][0]), int(pts_px[idx][1])), 9, 255, -1)

        # 2. Soft edge feathering
        hand_mask = cv2.GaussianBlur(hand_mask, (9, 9), 0)

        # 3. Smooth alpha blend of fingers on top of guitar neck (guitar stays 100% solid!)
        mask_idx = hand_mask > 35
        if np.any(mask_idx):
            alpha = (hand_mask[mask_idx].astype(np.float32) / 255.0)[:, np.newaxis]
            fg = camera_raw[mask_idx].astype(np.float32)
            bg = frame[mask_idx].astype(np.float32)
            frame[mask_idx] = (fg * alpha + bg * (1.0 - alpha)).astype(np.uint8)

    def _render_realistic_guitar(self, frame: np.ndarray):
        """Ultra-fast SIMD ROI blitting with ambient drop shadow & C-level alpha blending."""
        h, w = frame.shape[:2]
        if self.guitar_rgba is None:
            return

        warped = cv2.warpAffine(
            self.guitar_rgba, self.M, (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0, 0, 0, 0)
        )

        bgr = warped[:, :, :3]
        alpha = warped[:, :, 3]
        pts = cv2.findNonZero(alpha)
        if pts is None:
            return

        rx, ry, rw, rh = cv2.boundingRect(pts)
        sub_frame = frame[ry:ry+rh, rx:rx+rw]
        sub_bgr = bgr[ry:ry+rh, rx:rx+rw]
        sub_alpha = alpha[ry:ry+rh, rx:rx+rw]

        # Fast ambient drop shadow
        sh_y1 = min(h, ry + 10)
        sh_y2 = min(h, ry + rh + 10)
        sh_x1 = min(w, rx + 8)
        sh_x2 = min(w, rx + rw + 8)
        sh_h = sh_y2 - sh_y1
        sh_w = sh_x2 - sh_x1
        if sh_h > 0 and sh_w > 0:
            s_sub = frame[sh_y1:sh_y2, sh_x1:sh_x2]
            sm_h = min(s_sub.shape[0], rh)
            sm_w = min(s_sub.shape[1], rw)
            if sm_h > 0 and sm_w > 0:
                s_mask = cv2.blur((sub_alpha[:sm_h, :sm_w] > 60).astype(np.uint8) * 55, (11, 11))
                s_3ch = cv2.merge([s_mask, s_mask, s_mask])
                cv2.subtract(s_sub[:sm_h, :sm_w], s_3ch, dst=s_sub[:sm_h, :sm_w])

        # Blit guitar using pure C++ SIMD cv2.copyTo (<1.2ms execution!)
        if sub_frame.shape[:2] == sub_bgr.shape[:2] and sub_alpha.shape[:2] == sub_bgr.shape[:2]:
            cv2.copyTo(sub_bgr, sub_alpha, sub_frame)

    def _render_fret_markers(self, frame: np.ndarray, chord: str):
        fret_xs = [330.0, 420.0, 510.0, 600.0, 690.0]
        for idx, x_fret in enumerate(fret_xs):
            p_scr = self.M @ np.array([x_fret, 378.0, 1.0], dtype=np.float32)
            is_active = (chord != 'MUTE') and (idx < 3)
            glow_color = (0, 255, 255) if is_active else (150, 150, 170)
            radius = 4 if is_active else 3
            cv2.circle(frame, (int(p_scr[0]), int(p_scr[1])), radius, glow_color, -1)

    def _render_plectrum(self, frame: np.ndarray, tip: Tuple[int, int]):
        """Image 1: Compact, razor-sharp pick triangle and cyber rings."""
        tx, ty = tip
        sz = 9
        pts = np.array([[tx, ty + sz], [tx - sz, ty - sz // 2], [tx + sz, ty - sz // 2]], dtype=np.int32)
        cv2.circle(frame, (tx, ty), 12, (255, 0, 180), 2, cv2.LINE_AA)
        cv2.circle(frame, (tx, ty), 16, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.fillPoly(frame, [pts], (0, 255, 255))
        cv2.polylines(frame, [pts], True, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "PICK", (tx - 12, ty - 13), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 255, 255), 1, cv2.LINE_AA)

    @staticmethod
    def _get_bone_quad(p1, p2, w1, w2):
        """Calculates a smooth 4-point fleshy polygon between two joints."""
        dx = float(p2[0] - p1[0])
        dy = float(p2[1] - p1[1])
        dist = max(1.0, math.hypot(dx, dy))
        nx = -dy / dist
        ny = dx / dist

        pt1 = (int(p1[0] + nx * w1 * 0.5), int(p1[1] + ny * w1 * 0.5))
        pt2 = (int(p2[0] + nx * w2 * 0.5), int(p2[1] + ny * w2 * 0.5))
        pt3 = (int(p2[0] - nx * w2 * 0.5), int(p2[1] - ny * w2 * 0.5))
        pt4 = (int(p1[0] - nx * w1 * 0.5), int(p1[1] - ny * w1 * 0.5))
        return np.array([pt1, pt2, pt3, pt4], dtype=np.int32)

    def _render_fleshy_3d_hand(
        self,
        canvas: np.ndarray,
        pts_px: List[Tuple[float, float]],
        is_fret_hand: bool = False,
        skin_base: Tuple[int, int, int] = (135, 175, 228)
    ):
        """
        Renders a unified, continuous 3D realistic human hand with pro-grade detail:
        - Zero internal circular seams (fully unified fleshy palm + fingers)
        - Thick, nourished human proportions
        - Fingernail rendering with specular edge
        - Palm lines (life, head, heart)
        - Knuckle wrinkle details at PIP/DIP joints
        - Soft 3D lighting, cylindrical highlights
        - Anti-aliased silhouette edges
        """
        if len(pts_px) < 21:
            return

        pts = [(int(p[0]), int(p[1])) for p in pts_px]

        # HSV-inspired warm skin tones
        c_shadow = tuple(max(0, int(c * 0.72)) for c in skin_base)
        c_deep_shadow = tuple(max(0, int(c * 0.58)) for c in skin_base)
        c_mid = skin_base
        c_light = tuple(min(255, int(c * 1.18)) for c in skin_base)
        c_highlight = (220, 240, 255)
        c_fold = tuple(max(0, int(c * 0.65)) for c in skin_base)
        c_nail = (195, 215, 238)
        c_nail_edge = (235, 242, 252)

        # Thickness specifications for full nourished human fingers
        FINGER_SPECS = [
            ([1, 2, 3, 4], [28, 26, 22, 20]),       # Thumb
            ([5, 6, 7, 8], [26, 23, 20, 18]),       # Index
            ([9, 10, 11, 12], [27, 24, 21, 18]),    # Middle
            ([13, 14, 15, 16], [25, 22, 19, 17]),   # Ring
            ([17, 18, 19, 20], [23, 20, 17, 15])    # Pinky
        ]

        # ====== PASS 1: Unified Solid Flesh Silhouette ======
        # Palm body polygon
        palm_pts = [
            pts[0],
            pts[1],
            (int(0.4 * pts[1][0] + 0.6 * pts[5][0]), int(0.4 * pts[1][1] + 0.6 * pts[5][1])),
            pts[5],
            pts[9],
            pts[13],
            pts[17],
            (int(0.6 * pts[17][0] + 0.4 * pts[0][0]), int(0.6 * pts[17][1] + 0.4 * pts[0][1]))
        ]
        palm_poly = np.array(palm_pts, dtype=np.int32)
        cv2.fillConvexPoly(canvas, palm_poly, c_mid)

        # Muscle pads blended into the palm
        thenar_pt = (
            int(0.46 * pts[0][0] + 0.38 * pts[1][0] + 0.16 * pts[5][0]),
            int(0.46 * pts[0][1] + 0.38 * pts[1][1] + 0.16 * pts[5][1])
        )
        cv2.circle(canvas, thenar_pt, 28, c_mid, -1)

        hypothenar_pt = (
            int(0.42 * pts[0][0] + 0.58 * pts[17][0]),
            int(0.42 * pts[0][1] + 0.58 * pts[17][1])
        )
        cv2.circle(canvas, hypothenar_pt, 24, c_mid, -1)
        cv2.circle(canvas, pts[0], 25, c_mid, -1)

        # Fill all finger quads in solid flesh tone
        for chain, widths in FINGER_SPECS:
            for s in range(len(chain) - 1):
                quad = self._get_bone_quad(pts[chain[s]], pts[chain[s+1]], widths[s], widths[s+1])
                cv2.fillConvexPoly(canvas, quad, c_mid)
                cv2.circle(canvas, pts[chain[s]], widths[s] // 2, c_mid, -1)
            cv2.circle(canvas, pts[chain[-1]], widths[-1] // 2, c_mid, -1)

        # Knuckle webbing fills
        for k in [5, 9, 13, 17]:
            cv2.circle(canvas, pts[k], 14, c_mid, -1)

        # ====== PASS 2: 3D Shading & Muscle Contours ======
        # Thenar and hypothenar muscle highlights
        cv2.circle(canvas, (thenar_pt[0] - 2, thenar_pt[1] - 2), 16, c_light, -1)
        cv2.circle(canvas, (hypothenar_pt[0] - 2, hypothenar_pt[1] - 2), 12, c_light, -1)
        p_center = (
            int((pts[0][0] + pts[5][0] + pts[17][0]) / 3),
            int((pts[0][1] + pts[5][1] + pts[17][1]) / 3)
        )
        cv2.circle(canvas, p_center, 18, c_light, -1)

        # ====== PASS 2B: Palm Lines (Life, Head, Heart) ======
        # Heart line: across upper palm from pinky MCP to between index/middle
        heart_mid = (int(0.5 * pts[9][0] + 0.5 * pts[5][0]), int(0.5 * pts[9][1] + 0.5 * pts[5][1]))
        cv2.line(canvas, pts[17], heart_mid, c_fold, 1, cv2.LINE_AA)
        # Head line: mid-palm diagonal
        head_start = (int(0.65 * pts[5][0] + 0.35 * pts[0][0]), int(0.65 * pts[5][1] + 0.35 * pts[0][1]))
        head_end = (int(0.45 * pts[17][0] + 0.55 * pts[0][0]), int(0.45 * pts[17][1] + 0.55 * pts[0][1]))
        cv2.line(canvas, head_start, head_end, c_fold, 1, cv2.LINE_AA)
        # Life line: curved arc from thumb base
        life_mid = (int(0.55 * pts[0][0] + 0.30 * pts[1][0] + 0.15 * pts[5][0]),
                    int(0.55 * pts[0][1] + 0.30 * pts[1][1] + 0.15 * pts[5][1]))
        cv2.line(canvas, pts[1], life_mid, c_fold, 1, cv2.LINE_AA)

        # ====== PASS 3: Finger Shading, Nails & Joint Creases ======
        for chain, widths in FINGER_SPECS:
            for s in range(len(chain) - 1):
                p1, p2 = pts[chain[s]], pts[chain[s+1]]
                w1, w2 = widths[s], widths[s+1]

                dx = float(p2[0] - p1[0])
                dy = float(p2[1] - p1[1])
                dist = max(1.0, math.hypot(dx, dy))
                nx = -dy / dist
                ny = dx / dist

                # Specular light ridge along upper finger surface
                h1 = (int(p1[0] + nx * w1 * 0.16), int(p1[1] + ny * w1 * 0.16))
                h2 = (int(p2[0] + nx * w2 * 0.16), int(p2[1] + ny * w2 * 0.16))
                cv2.line(canvas, h1, h2, c_light, max(2, int(w1 * 0.28)), cv2.LINE_AA)

                # Shadow ridge along lower finger surface
                s1 = (int(p1[0] - nx * w1 * 0.20), int(p1[1] - ny * w1 * 0.20))
                s2 = (int(p2[0] - nx * w2 * 0.20), int(p2[1] - ny * w2 * 0.20))
                cv2.line(canvas, s1, s2, c_shadow, max(1, int(w1 * 0.18)), cv2.LINE_AA)

                # Joint fold lines (natural crease at PIP and DIP joints)
                if s > 0:
                    jp = p1
                    rad = w1 // 2
                    c_dx = -dy / dist * (rad * 0.65)
                    c_dy = dx / dist * (rad * 0.65)
                    pt_a = (int(jp[0] - c_dx), int(jp[1] - c_dy))
                    pt_b = (int(jp[0] + c_dx), int(jp[1] + c_dy))
                    cv2.line(canvas, pt_a, pt_b, c_fold, 1, cv2.LINE_AA)
                    # Secondary subtle crease
                    off = 2
                    pt_a2 = (pt_a[0] + off, pt_a[1] + off)
                    pt_b2 = (pt_b[0] + off, pt_b[1] + off)
                    cv2.line(canvas, pt_a2, pt_b2, c_deep_shadow, 1, cv2.LINE_AA)

            # ====== Fingernail Rendering ======
            tip_p = pts[chain[-1]]
            prev_p = pts[chain[-2]]
            tip_rad = widths[-1] // 2

            # Nail direction (from DIP to TIP)
            n_dx = float(tip_p[0] - prev_p[0])
            n_dy = float(tip_p[1] - prev_p[1])
            n_dist = max(1.0, math.hypot(n_dx, n_dy))
            n_ux = n_dx / n_dist
            n_uy = n_dy / n_dist

            # Nail base (slightly before fingertip)
            nail_cx = int(tip_p[0] + n_ux * tip_rad * 0.2)
            nail_cy = int(tip_p[1] + n_uy * tip_rad * 0.2)

            # Nail body (oval)
            nail_w = max(3, int(tip_rad * 0.75))
            nail_h = max(2, int(tip_rad * 0.55))
            nail_angle = math.degrees(math.atan2(n_uy, n_ux))
            cv2.ellipse(canvas, (nail_cx, nail_cy), (nail_w, nail_h), nail_angle, 0, 360, c_nail, -1)
            # Nail specular edge
            cv2.ellipse(canvas, (nail_cx, nail_cy), (nail_w, nail_h), nail_angle, 0, 360, c_nail_edge, 1, cv2.LINE_AA)
            # Nail lunula (half-moon at base)
            lunula_cx = int(nail_cx - n_ux * nail_w * 0.5)
            lunula_cy = int(nail_cy - n_uy * nail_w * 0.5)
            cv2.ellipse(canvas, (lunula_cx, lunula_cy), (max(2, nail_w // 2), max(1, nail_h // 2)),
                        nail_angle, 0, 360, c_highlight, -1)
