"""
========================================================================================
AeroFret: Kinetic — PRO AIR GUITAR SIMULATOR
"Strings of Light, Music of Motion"
----------------------------------------------------------------------------------------
Engineered & Developed by Mahmoud Labib

A unified, plug-and-play single-file launcher for touchless electric air guitar
performance and interactive rhythm gaming with AAA English UI/UX and 60 FPS performance.

Spatial Mechanics:
  - Left Hand  : Physically grips and aims the Fender Stratocaster neck in mid-air.
                 Number of extended fingers selects the active guitar chord/tone:
                 * 0 Fingers (Closed Fist) -> PALM MUTE
                 * 1 Finger (Index)        -> C MAJOR
                 * 2 Fingers               -> D MINOR
                 * 3 Fingers               -> E MINOR
                 * 4 Fingers               -> F MAJOR
                 * 5 Fingers (Open Palm)   -> G MAJOR
  - Right Hand : Index fingertip acts as the glowing laser Plectrum (Pick).
                 Sweeping across the pickups and neon strings triggers chords with
                 real-time velocity (dy/dt) gain control.
  - Visuals    : Photorealistic Fender Stratocaster guitar warped to player posture,
                 vibrating neon strings, mother-of-pearl fret markers, and sparks.

Controls:
  - [F]       : Toggle True Borderless Fullscreen
  - [C]       : Toggle Virtual Stage / Camera-Hide Mode
  - [M]       : Toggle Mode (Free-Play Air Guitar <-> Guitar Hero Rhythm Mode)
  - [R]       : Reset Score / Combo Streaks
  - [P]       : Cycle Amp Power Presets (50% / 75% / 100%)
  - [ [ / ] ] : Decrease / Increase Amp Power by 5%
  - [1-5 / 0] : Keyboard Chord Overrides (1=C, 2=Dm, 3=Em, 4=F, 5=G, 0=Mute)
  - [SPACE]   : Manual Test Strum
  - [Q / ESC] : Quit Application
========================================================================================
"""

import math
import os
import random
import sys
import time
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

# Ensure clean UTF-8 output on Windows terminals
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from core.terminal_banner import print_cyberpunk_banner
from core.audio_synth import AudioEngine
from core.hand_tracker import HandTracker
from core.gesture_engine import GestureEngine
from core.rhythm_manager import RhythmManager
from ui.visualizer import Visualizer
from ui.hud import HUD


# ======================================================================================
# MASTER GAME APPLICATION LOOP
# ======================================================================================
class AeroFretApp:
    """
    Master orchestrator for AeroFret: Kinetic.
    Coordinates camera capture, hand tracking, gesture recognition, audio synthesis,
    visual rendering, and rhythm gameplay in a tight 60 FPS real-time loop.
    """

    WINDOW_NAME = "AeroFret: Kinetic"
    WINDOW_NAME_DEMO = "AeroFret: Kinetic (Demo Mode)"

    def __init__(
        self,
        camera_index: int = 0,
        bpm: float = 105.0,
        num_strings: int = 4,
        power_level: float = 0.85,
        start_fullscreen: bool = True,
        virtual_stage: bool = False,
        debounce_ms: float = 120.0,
        confidence: float = 0.65,
        initial_mode: str = "free",
        tone_preset: str = "overdrive",
        enable_pyro: bool = True,
        enable_floating_notes: bool = True,
        enable_vibrato: bool = False,
        play_style: str = "hybrid"
    ):
        print_cyberpunk_banner("Performance Session Active")

        self.camera_index = camera_index
        self.start_fullscreen = start_fullscreen
        self.cap = None

        # Core engine instances (single source of truth from core/ package)
        self.audio = AudioEngine(preset=tone_preset, enable_vibrato=enable_vibrato)
        self.tracker = HandTracker(min_detection_confidence=confidence, min_tracking_confidence=confidence)
        self.gesture = GestureEngine(num_strings=num_strings, debounce_ms=debounce_ms, play_style=play_style)
        self.rhythm = RhythmManager(bpm=bpm)
        if initial_mode == "rhythm":
            self.rhythm.is_active = True
        self.visualizer = Visualizer(
            num_strings=num_strings,
            enable_pyro=enable_pyro,
            enable_floating_notes=enable_floating_notes,
            enable_vibrato=enable_vibrato
        )
        if virtual_stage:
            self.visualizer.virtual_stage_mode = True
        self.hud = HUD()

        self.is_running = False
        self.is_fullscreen = False
        self.power_level = float(power_level)
        self.last_gain = float(power_level)

        # Track the active window name for fullscreen toggle
        self._active_window_name = self.WINDOW_NAME

    def _on_mouse(self, event, x, y, flags, param):
        """Interactive mouse callback for Rotary Power Dial, +/- buttons, and Mode Badge."""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.hud.handle_mode_click(x, y):
                self.rhythm.toggle()
                return

            new_p = self.hud.handle_click(x, y, self.power_level)
            if new_p is not None:
                self.power_level = new_p
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            new_p = self.hud.handle_click(x, y, self.power_level)
            if new_p is not None:
                self.power_level = new_p
        elif event == cv2.EVENT_MOUSEWHEEL:
            direction = 1 if flags > 0 else -1
            self.power_level = self.hud.handle_scroll(direction, self.power_level)

    def _apply_window_icon_win32(self):
        """Sets custom cyberpunk electric guitar icon on the window titlebar & taskbar."""
        if sys.platform != 'win32':
            return
        try:
            import ctypes
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'app_icon.ico')
            if not os.path.exists(icon_path):
                return
            user32 = ctypes.windll.user32
            hwnd = user32.FindWindowW(None, self._active_window_name)
            if not hwnd:
                hwnd = user32.GetActiveWindow()
            if hwnd:
                h_icon_sm = user32.LoadImageW(None, icon_path, 1, 16, 16, 0x0010)
                h_icon_lg = user32.LoadImageW(None, icon_path, 1, 32, 32, 0x0010)
                if h_icon_sm:
                    user32.SendMessageW(hwnd, 0x0080, 0, h_icon_sm)  # WM_SETICON, ICON_SMALL
                if h_icon_lg:
                    user32.SendMessageW(hwnd, 0x0080, 1, h_icon_lg)  # WM_SETICON, ICON_BIG
        except Exception:
            pass

    def _apply_borderless_win32(self):
        """Forces the window to borderless popup mode on Windows OS to eliminate title bar."""
        if sys.platform != 'win32':
            return
        try:
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = user32.FindWindowW(None, self._active_window_name)
            if not hwnd:
                hwnd = user32.GetActiveWindow()
            if hwnd:
                style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
                # Strip title bar, borders, sizing frame, sysmenu
                style &= ~(0x00C00000 | 0x00040000 | 0x00080000 | 0x00010000)
                style |= 0x80000000  # WS_POPUP
                user32.SetWindowLongW(hwnd, -16, style)
                sw = user32.GetSystemMetrics(0)
                sh = user32.GetSystemMetrics(1)
                user32.SetWindowPos(hwnd, 0, 0, 0, sw, sh, 0x0020 | 0x0040)
        except Exception:
            pass

    def toggle_fullscreen(self):
        """Toggles true borderless fullscreen (hides titlebar & taskbar completely)."""
        self.is_fullscreen = not self.is_fullscreen
        win_name = self._active_window_name
        if self.is_fullscreen:
            cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self._apply_borderless_win32()
        else:
            cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            if sys.platform == 'win32':
                try:
                    import ctypes
                    user32 = ctypes.windll.user32
                    hwnd = user32.FindWindowW(None, win_name)
                    if not hwnd:
                        hwnd = user32.GetActiveWindow()
                    if hwnd:
                        style = user32.GetWindowLongW(hwnd, -16)
                        style |= (0x00C00000 | 0x00040000 | 0x00080000)
                        style &= ~0x80000000
                        user32.SetWindowLongW(hwnd, -16, style)
                        sw = user32.GetSystemMetrics(0)
                        sh = user32.GetSystemMetrics(1)
                        user32.SetWindowPos(hwnd, 0, (sw - 1280) // 2, (sh - 720) // 2, 1280, 720, 0x0020 | 0x0040)
                except Exception:
                    pass
            cv2.resizeWindow(win_name, 1280, 720)

    def start_camera(self) -> bool:
        """Initialize webcam capture with MJPG codec forcing for 60 FPS on Windows USB."""
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW if sys.platform == 'win32' else cv2.CAP_ANY)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("[AeroFretApp] Error: No webcam detected!")
            return False

        # Force MJPG codec to bypass Windows USB uncompressed YUY2 12 FPS throttle
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        # Perf 4: Pre-flush stale USB buffer (discard first 2 frames)
        for _ in range(2):
            self.cap.read()

        return True

    def run(self):
        """Main game loop: camera capture → hand tracking → guitar rendering → HUD → display."""
        if not self.start_camera():
            self._run_fallback_loop()
            return

        self.is_running = True
        self._active_window_name = self.WINDOW_NAME
        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.WINDOW_NAME, 1280, 720)
        cv2.setMouseCallback(self.WINDOW_NAME, self._on_mouse)

        # Auto-start in borderless fullscreen (hide white title bar from frame 1)
        if self.start_fullscreen:
            self.toggle_fullscreen()

        fps_smooth = 60.0
        frame_count = 0

        print("[AeroFretApp] System online! Ready to rock:")
        print("  Left Hand  : Grip the guitar neck in air (1-5 fingers for chords)")
        print("  Right Hand : Index Finger acts as the Plectrum across strings")
        print("  Power Knob : Click/Drag Dial, Scroll Wheel, or keys [ [ / ] ] / P")
        print("  Display    : Press [F] for Fullscreen Borderless, [C] for Virtual Stage")

        while self.is_running:
            t_start = time.time()
            ret, frame = self.cap.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            # 1. High-speed 60 FPS Spatial Hand Tracking
            hands = self.tracker.process_frame(frame)

            # 2. Update Dynamic Fender Stratocaster Anchors
            string_segments = self.visualizer.update_oud_anchors(hands['fret_hand'], hands['strum_hand'], w, h)

            # 3. Chord Classification from Left Hand
            chord_code, chord_display = self.gesture.update_chord(hands['fret_hand'])

            # 4. Detect Crossing of Dynamic Strings by Right Index Finger
            strums = self.gesture.detect_strums(hands['strum_hand'], string_segments, chord_code)

            # Sync nearest string highlight for visual UX feedback
            self.visualizer.nearest_string_idx = self.gesture.nearest_string_idx

            # 5. Play Audio & Trigger Visual Reactions modulated by Power Level & Physical Velocity
            if len(strums) == 1:
                strum = strums[0]
                effective_gain = float(np.clip(self.power_level * strum.get('gain', 1.0), 0.1, 1.0))
                self.last_gain = effective_gain
                self.audio.play_single_string(strum['chord'], strum['string_index'], velocity=effective_gain)
                self.visualizer.trigger_pluck(strum['string_index'], strum['strum_x'], effective_gain, chord_name=strum['chord'])
                self.rhythm.check_hit(strum)
            elif len(strums) > 1:
                direction = strums[0].get('direction', 1)
                avg_gain = float(np.mean([s.get('gain', 1.0) for s in strums]))
                effective_gain = float(np.clip(self.power_level * avg_gain, 0.1, 1.0))
                self.last_gain = effective_gain
                self.audio.play_chord(strums[0]['chord'], velocity=effective_gain, direction=direction)

                # Harmonious stage event: 1 unified shockwave & controlled power flame check at centroid
                mid_strum = strums[len(strums) // 2]
                self.visualizer.trigger_chord_burst(mid_strum['strum_x'], mid_strum['string_index'], effective_gain, chord_name=strums[0]['chord'])

                for strum in strums:
                    s_gain = float(np.clip(self.power_level * strum.get('gain', 1.0), 0.1, 1.0))
                    self.visualizer.trigger_pluck(strum['string_index'], strum['strum_x'], s_gain, chord_name=strum['chord'], is_chord_sweep=True)
                    self.rhythm.check_hit(strum)

            # 6. Update Rhythm Game Notes (Perf 3: cache time once per frame)
            now = time.time()
            self.rhythm.update(now, string_segments)

            # 7. Render Realistic Guitar and Graphics (with 3D hand layering)
            frame = self.visualizer.render(frame, hands['fret_hand'], hands['strum_hand'], self.rhythm, chord_code)

            # Bug 5: Skeleton only drawn in camera mode; guard against missing raw_landmarks
            if not self.visualizer.virtual_stage_mode:
                safe_hands = {}
                for role in ('fret_hand', 'strum_hand'):
                    h_data = hands.get(role)
                    if h_data is not None and 'raw_landmarks' in h_data:
                        safe_hands[role] = h_data
                    else:
                        safe_hands[role] = None
                self.tracker.draw_skeleton(frame, safe_hands)

            frame = self.hud.render(
                frame,
                hands['fret_hand'],
                hands['strum_hand'],
                chord_code,
                chord_display,
                fps_smooth,
                self.rhythm,
                self.last_gain,
                power_level=self.power_level
            )

            dt = now - t_start
            if dt > 0:
                fps_smooth = 0.90 * fps_smooth + 0.10 * (1.0 / dt)

            cv2.imshow(self.WINDOW_NAME, frame)
            if frame_count == 0:
                self._apply_window_icon_win32()
                if self.is_fullscreen:
                    self._apply_borderless_win32()
            frame_count += 1

            key = cv2.waitKey(1) & 0xFF
            self._handle_key(key, w)

        self.cleanup()

    def _run_fallback_loop(self):
        """Demo mode: renders the full UI without a webcam for testing and exploration."""
        w, h = 1280, 720
        self._active_window_name = self.WINDOW_NAME_DEMO
        cv2.namedWindow(self.WINDOW_NAME_DEMO, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.WINDOW_NAME_DEMO, w, h)
        # Bug 3: Register mouse callback so power dial and mode pill are interactive
        cv2.setMouseCallback(self.WINDOW_NAME_DEMO, self._on_mouse)

        if self.start_fullscreen:
            self.toggle_fullscreen()

        fps_smooth = 60.0
        frame_count = 0
        self.is_running = True

        while self.is_running:
            t_start = time.time()
            canvas = np.zeros((h, w, 3), dtype=np.uint8)
            cv2.rectangle(canvas, (0, 0), (w, h), (18, 18, 28), -1)

            string_segments = self.visualizer.update_oud_anchors(None, None, w, h)
            now = time.time()
            self.rhythm.update(now, string_segments)

            canvas = self.visualizer.render(canvas, None, None, self.rhythm)
            # Bug 2: Pass power_level to HUD render in demo mode
            canvas = self.hud.render(
                canvas, None, None,
                self.gesture.current_chord,
                self.gesture.CHORD_NAMES.get(self.gesture.current_chord, 'C MAJOR'),
                fps_smooth, self.rhythm,
                self.last_gain,
                power_level=self.power_level
            )

            cv2.putText(canvas, "[DEMO MODE: NO WEBCAM DETECTED]", (w // 2 - 200, h // 2),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(canvas, "Press [SPACE] to Strum, [1-5] for Chords, [F] Fullscreen, [C] Stage, [Q] to Quit",
                        (w // 2 - 380, h // 2 + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 255, 255), 1)

            dt = now - t_start
            if dt > 0:
                fps_smooth = 0.90 * fps_smooth + 0.10 * (1.0 / dt)

            cv2.imshow(self.WINDOW_NAME_DEMO, canvas)
            if frame_count == 0:
                self._apply_window_icon_win32()
                if self.is_fullscreen:
                    self._apply_borderless_win32()
            frame_count += 1

            key = cv2.waitKey(16) & 0xFF
            self._handle_key(key, w)

        self.cleanup()

    def _handle_key(self, key: int, frame_width: int):
        """Unified keyboard handler shared by both camera and demo modes."""
        if key in (ord('q'), ord('Q'), 27):
            self.is_running = False
        elif key in (ord('f'), ord('F')):
            self.toggle_fullscreen()
        elif key in (ord('c'), ord('C')):
            self.visualizer.virtual_stage_mode = not self.visualizer.virtual_stage_mode
        elif key in (ord('m'), ord('M')):
            self.rhythm.toggle()
        elif key in (ord('r'), ord('R')):
            self.rhythm.reset()
        elif key in (ord('['), ord('{')):
            self.power_level = max(0.10, self.power_level - 0.05)
        elif key in (ord(']'), ord('}')):
            self.power_level = min(1.0, self.power_level + 0.05)
        elif key in (ord('p'), ord('P')):
            presets = [0.50, 0.75, 1.0]
            curr_idx = min(range(len(presets)), key=lambda i: abs(presets[i] - self.power_level))
            self.power_level = presets[(curr_idx + 1) % len(presets)]
        elif key == ord(' '):
            self.audio.play_chord(self.gesture.current_chord, velocity=self.power_level)
            self.visualizer.trigger_pluck(1, int(frame_width * 0.65), self.power_level)
        elif key in (ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5')):
            idx = int(chr(key))
            self.gesture.current_chord = self.gesture.CHORD_MAP.get(idx, 'C')

    def cleanup(self):
        """Release all resources gracefully."""
        print("[AeroFretApp] Cleaning up and releasing resources...")
        if hasattr(self, 'audio') and self.audio:
            try:
                self.audio.stop_all()
            except Exception:
                pass
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
        if hasattr(self, 'tracker') and self.tracker:
            try:
                self.tracker.release()
            except Exception:
                pass
        cv2.destroyAllWindows()
        print("[AeroFretApp] Keep rocking!")


# ======================================================================================
# ENTRY POINT
# ======================================================================================
if __name__ == '__main__':
    app = AeroFretApp(camera_index=0)
    app.run()
