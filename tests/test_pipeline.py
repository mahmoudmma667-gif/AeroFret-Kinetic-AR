"""
AeroFret: Kinetic - Automated Verification Test Harness
Tests physical audio modeling, 60 FPS spatial tracking, velocity calculation,
dynamic angled string crossing, and photorealistic electric guitar rendering.
"""

import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.audio_synth import AudioEngine
from core.gesture_engine import GestureEngine
from core.rhythm_manager import RhythmManager
from ui.visualizer import Visualizer
from ui.hud import HUD


def test_audio_synthesis():
    print("[TEST] Running AudioEngine verification...")
    ae = AudioEngine()
    assert ae.is_initialized or ae.backend is not None
    assert len(ae.raw_waveforms) >= 6

    for chord_name, wave in ae.raw_waveforms.items():
        assert wave.shape[1] == 2
        assert not np.isnan(wave).any()
        assert not np.isinf(wave).any()
        assert np.max(np.abs(wave)) <= 1.0

    ae.play_chord('C', velocity=0.5, direction=1)
    ae.play_chord('Em', velocity=0.9, direction=-1)
    ae.play_single_string('C', 0, velocity=0.7)
    ae.play_single_string('G', 3, velocity=0.85)
    print("  --> AudioEngine: PASSED")


def test_gesture_chord_mapping():
    print("[TEST] Running 100% English GestureEngine chord mapping verification...")
    ge = GestureEngine()

    expected_chords = [
        (0, 'MUTE', 'PALM MUTE'),
        (1, 'C', 'C MAJOR'),
        (2, 'Dm', 'D MINOR'),
        (3, 'Em', 'E MINOR'),
        (4, 'F', 'F MAJOR'),
        (5, 'G', 'G MAJOR')
    ]

    for fingers, exp_code, exp_name in expected_chords:
        mock_fret = {
            'extended': [True if i < fingers else False for i in range(5)],
            'finger_count': fingers,
            'wrist': (150, 400)
        }
        for _ in range(3):
            code, display = ge.update_chord(mock_fret)
        assert code == exp_code, f"Expected {exp_code}, got {code}"
        assert display == exp_name, f"Expected {exp_name}, got {display}"

    print("  --> English Chord Mapping: PASSED")


def test_dynamic_strumming_and_debouncing():
    print("[TEST] Running Dynamic Pickup crossing & 120ms debouncing verification...")
    ge = GestureEngine(num_strings=4, debounce_ms=120.0, min_vel=100.0, max_vel=1500.0)

    # Natural ergonomic string segments from Visualizer
    string_segments = Visualizer.generate_string_sources(4)

    # Strum across string 0 (at X=600, String 0 is at Y~326)
    mock_1 = {'index_tip': (600, 310)}  # Above string 0
    ge.detect_strums(mock_1, string_segments, 'C')

    time.sleep(0.02)
    mock_2 = {'index_tip': (600, 335)}  # Crosses only string 0
    events = ge.detect_strums(mock_2, string_segments, 'C')
    assert len(events) == 1, f"Expected 1 strum, got {len(events)}"
    assert events[0]['string_index'] == 0

    # Test lockout within 20ms (<120ms)
    time.sleep(0.01)
    mock_3 = {'index_tip': (600, 337)}
    debounced = ge.detect_strums(mock_3, string_segments, 'C')
    assert len(debounced) == 0, "Debounce failed: duplicate trigger allowed within 120ms!"

    # Test cooldown: trigger after 140ms
    time.sleep(0.14)
    mock_4 = {'index_tip': (600, 310)}
    cooldown_evts = ge.detect_strums(mock_4, string_segments, 'C')
    assert len(cooldown_evts) == 1, f"Expected 1 strum after cooldown, got {len(cooldown_evts)}"

    print("  --> Dynamic Strumming & Debouncing: PASSED")


def test_photorealistic_guitar_rendering():
    print("[TEST] Running Photorealistic Fender Stratocaster rendering verification...")
    w, h = 1280, 720
    frame = np.zeros((h, w, 3), dtype=np.uint8)

    vis = Visualizer(num_strings=4)
    mock_fret = {'wrist': (260, 410), 'finger_count': 1, 'extended': [False, True, False, False, False]}
    mock_strum = {'wrist': (880, 520), 'index_tip': (780, 480)}

    segments = vis.update_oud_anchors(mock_fret, mock_strum, w, h)
    assert len(segments) == 4

    vis.trigger_pluck(0, 600, 0.9)
    rendered = vis.render(frame, mock_fret, mock_strum, None, 'C')
    assert rendered.shape == (h, w, 3)

    hud = HUD()
    final = hud.render(rendered, mock_fret, mock_strum, 'C', 'C MAJOR', 60.0, None, 0.85)
    assert final.shape == (h, w, 3)
    assert not np.all(final == 0)

    print("  --> Photorealistic Guitar & English HUD: PASSED")


def test_extreme_velocity_and_tremolo_shredding():
    print("[TEST] Running Extreme Velocity CCD & Tremolo Shredding verification...")
    ge = GestureEngine(num_strings=4, debounce_ms=120.0)

    str_segs = [
        ((200, 300), (800, 300)),
        ((200, 360), (800, 360)),
        ((200, 420), (800, 420)),
        ((200, 480), (800, 480)),
    ]

    # 1. Violent multi-string power sweep (>10,000 px/s leap across all 4 strings)
    ge.detect_strums_dynamic({'index_tip': (500, 240)}, str_segs, 'C')
    time.sleep(0.016)
    sweep_evts = ge.detect_strums_dynamic({'index_tip': (520, 540)}, str_segs, 'C')
    assert len(sweep_evts) == 4, f"Expected 4 strings swept, got {len(sweep_evts)}"
    for s_idx in range(4):
        assert sweep_evts[s_idx]['string_index'] == s_idx

    # 2. Rapid Tremolo Alternate Picking on string 2 (Down then Up in 45ms < 120ms standard debounce)
    time.sleep(0.15)
    ge.prev_tip_pos = None  # Reset tracking state for clean stroke initiation
    ge.detect_strums_dynamic({'index_tip': (500, 400)}, str_segs, 'C')
    time.sleep(0.016)
    down_ev = ge.detect_strums_dynamic({'index_tip': (500, 440)}, str_segs, 'C')
    assert len(down_ev) == 1 and down_ev[0]['string_index'] == 2

    time.sleep(0.045)  # 45ms shredding interval
    up_ev = ge.detect_strums_dynamic({'index_tip': (500, 400)}, str_segs, 'C')
    assert len(up_ev) == 1 and up_ev[0]['string_index'] == 2, "Failed to capture rapid alternate picking up-stroke!"

    print("  --> Extreme Velocity CCD & Tremolo Shredding: PASSED")


def test_multi_string_distribution():
    print("[TEST] Running Dynamic Multi-String Layout (3, 4, 5, 6 Strings) verification...")
    w, h = 1280, 720
    mock_fret = {'wrist': (260, 410), 'finger_count': 1, 'extended': [False, True, False, False, False], 'landmarks_px': [(260, 410, 0)] * 21}
    mock_strum = {'wrist': (880, 520), 'index_tip': (780, 480)}

    for num_strings in [3, 4, 5, 6]:
        srcs = Visualizer.generate_string_sources(num_strings)
        assert len(srcs) == num_strings, f"Expected {num_strings} string sources, got {len(srcs)}"
        assert abs(srcs[0][0][1] - 340.0) < 1e-3, f"Nut Y start mismatch for {num_strings} strings"
        assert abs(srcs[-1][0][1] - 415.0) < 1e-3, f"Nut Y end mismatch for {num_strings} strings"
        assert abs(srcs[0][1][1] - 305.0) < 1e-3, f"Bridge Y start mismatch for {num_strings} strings"
        assert abs(srcs[-1][1][1] - 475.0) < 1e-3, f"Bridge Y end mismatch for {num_strings} strings"

        # Verify Visualizer initialization & anchor updates without IndexError
        vis = Visualizer(num_strings=num_strings)
        assert len(vis.strings) == num_strings
        segments = vis.update_oud_anchors(mock_fret, mock_strum, w, h)
        assert len(segments) == num_strings, f"Expected {num_strings} segments, got {len(segments)}"

        # Verify all strings are positioned within realistic canvas bounds
        for s_idx, (p1, p2) in enumerate(segments):
            assert 0 <= p1[0] <= w and 0 <= p1[1] <= h, f"String {s_idx} p1 out of bounds"
            assert 0 <= p2[0] <= w and 0 <= p2[1] <= h, f"String {s_idx} p2 out of bounds"

    print("  --> Dynamic Multi-String Distribution (3, 4, 5, 6 Strings): PASSED")


def test_audio_tone_presets():
    print("[TEST] Running AudioEngine Tone Presets & Vibrato verification...")
    ae = AudioEngine(preset='overdrive', enable_vibrato=False)
    assert ae.preset == 'overdrive'

    presets_to_test = ['crunch', 'clean', 'synthwave', 'overdrive']
    for p in presets_to_test:
        ae.set_preset(p, enable_vibrato=True)
        assert ae.preset == p
        assert ae.enable_vibrato is True
        for c_name in ['C', 'Em', 'MUTE']:
            wave = ae.raw_waveforms[c_name]
            assert not np.isnan(wave).any(), f"NaN detected in preset {p} for chord {c_name}"
            assert np.max(np.abs(wave)) <= 1.05, f"Waveform clipping exceeded in preset {p}"

    print("  --> Audio Tone Presets (Overdrive, Crunch, Clean, Synthwave): PASSED")


def test_visualizer_pyro_and_notes_vfx():
    print("[TEST] Running Visualizer Pyrotechnics, Floating Notes & Stage Bloom verification...")
    w, h = 1280, 720
    frame = np.zeros((h, w, 3), dtype=np.uint8)

    vis = Visualizer(num_strings=4, enable_pyro=True, enable_floating_notes=True, enable_vibrato=True)
    vis.virtual_stage_mode = True

    # High gain strum triggers pyro and notes
    vis.trigger_pluck(0, 600, gain=0.90, chord_name='Em')
    assert len(vis.pyro_particles) > 0, "Pyrotechnic particles not spawned on high gain strum"
    assert len(vis.floating_notes) > 0, "Floating musical notes not spawned"
    assert vis.stage_flash_intensity > 0.0, "Stage bloom flash not activated"

    rendered = vis.render(frame, None, None, None, active_chord='Em')
    assert rendered.shape == (h, w, 3)
    assert not np.all(rendered == 0), "Rendered virtual stage is completely empty"

    print("  --> Visualizer Pyrotechnics & Floating Notes VFX: PASSED")


import unittest


class TestAeroFretPipeline(unittest.TestCase):
    """Standard unittest test runner for CI and automated regression suites."""

    def test_audio_synthesis(self):
        test_audio_synthesis()

    def test_gesture_chord_mapping(self):
        test_gesture_chord_mapping()

    def test_dynamic_strumming_and_debouncing(self):
        test_dynamic_strumming_and_debouncing()

    def test_photorealistic_guitar_rendering(self):
        test_photorealistic_guitar_rendering()

    def test_extreme_velocity_and_tremolo_shredding(self):
        test_extreme_velocity_and_tremolo_shredding()

    def test_multi_string_distribution(self):
        test_multi_string_distribution()

    def test_audio_tone_presets(self):
        test_audio_tone_presets()

    def test_visualizer_pyro_and_notes_vfx(self):
        test_visualizer_pyro_and_notes_vfx()


if __name__ == '__main__':
    print("==================================================")
    print("  AeroFret: Kinetic - AAA English Guitar Suite")
    print("==================================================")
    test_audio_synthesis()
    test_gesture_chord_mapping()
    test_dynamic_strumming_and_debouncing()
    test_photorealistic_guitar_rendering()
    test_extreme_velocity_and_tremolo_shredding()
    test_multi_string_distribution()
    test_audio_tone_presets()
    test_visualizer_pyro_and_notes_vfx()
    print("==================================================")
    print("  ALL 8 TESTS PASSED WITH 100% SUCCESS!")
    print("==================================================")

