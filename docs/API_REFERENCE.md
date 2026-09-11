# 📚 AeroFret: Kinetic — Public API Reference Manual
## الدليل المرجعي الشامل للواجهات البرمجية والدوال والكلاسات

> **Author & Systems Architect:** **Mahmoud Labib**  
> *Transdisciplinary Researcher in HCI • HCT • HCC • STS*

---

## 📑 Core Modules

### 1. `core.hand_tracker.HandTracker`
Coordinates MediaPipe 21-landmark spatial hand tracking with CLAHE contrast enhancement and velocity-adaptive EMA filtering.

#### `__init__(min_detection_confidence=0.65, min_tracking_confidence=0.65)`
- **Parameters:**
  - `min_detection_confidence` (*float*): Minimum threshold for initial palm detection.
  - `min_tracking_confidence` (*float*): Minimum threshold for continuous landmark tracking.

#### `process_frame(frame: np.ndarray) -> Dict[str, Optional[dict]]`
- Ingests raw BGR video frame.
- Returns dictionary containing `'fret_hand'` and `'strum_hand'` metadata.
- Each hand dictionary contains:
  - `'wrist'` (*Tuple[int, int]*): Pixel coordinates of the carpal joint.
  - `'index_tip'` (*Tuple[int, int]*): Pixel coordinates of landmark 8.
  - `'extended'` (*List[bool]*): 5-element boolean array for extended digits.
  - `'finger_count'` (*int*): Number of extended fingers (0–5).
  - `'landmarks_px'` (*np.ndarray*): $21 \times 2$ pixel coordinate array.

#### `draw_skeleton(frame: np.ndarray, hands: dict)`
- Draws anti-aliased cyberpunk hand skeletons and joint connection nodes.

---

### 2. `core.gesture_engine.GestureEngine`
Evaluates musical gestures, chord classifications, and Continuous Collision Detection (CCD).

#### `__init__(num_strings=4, debounce_ms=120.0, min_vel=100.0, max_vel=1500.0, proximity_radius=22.0, proximity_min_vel=120.0, play_style='hybrid')`
- Initializes the physical strumming engine, proximity picking registers, and play style mode (`'hybrid'`, `'solo'`, `'strum'`).

#### `update_chord(fret_hand: Optional[dict]) -> Tuple[str, str]`
- Evaluates finger cardinality (0–5) from the left fretting hand.
- Returns `(chord_code, chord_display_name)`.
  - `0` -> `('MUTE', 'PALM MUTE')`
  - `1` -> `('C', 'C MAJOR')`
  - `2` -> `('Dm', 'D MINOR')`
  - `3` -> `('Em', 'E MINOR')`
  - `4` -> `('F', 'F MAJOR')`
  - `5` -> `('G', 'G MAJOR')`

#### `detect_strums(strum_hand: Optional[dict], string_segments: List[Tuple], chord: str) -> List[dict]`
- Executes Parametric Swept-Ray Continuous Collision Detection (CCD) and Proximity solo detection.
- Includes **Precision String Skipping**: leaps between non-adjacent strings sound strictly the targeted string in solo/hybrid modes without sounding intermediate strings.
- Returns list of strum collision events:
  - `'string_index'` (*int*): Index of the triggered string (0–5).
  - `'strum_x'` (*int*): Horizontal pixel coordinate of string strike.
  - `'chord'` (*str*): Active harmonic triad.
  - `'gain'` (*float*): Physical velocity multiplier $\in [0.1, 1.0]$.
  - `'direction'` (*int*): Stroke direction (+1 for down-strum, -1 for up-strum).
  - `'is_solo'` (*bool*): True if individual string pick.

---

### 3. `core.audio_synth.AudioEngine`
Procedural Karplus-Strong physical modeling acoustic wave synthesizer with authentic 6-string voicings and polyphonic single-string synthesis.

#### `__init__(sample_rate=44100, buffer_size=256, preset='overdrive', enable_vibrato=False)`
- Initializes audio backend (Pygame / SoundDevice / Dummy) and precomputes polyphonic chords and single-string notes.
- **Parameters:**
  - `preset` (*str*): Sonic profile (`'overdrive'`, `'crunch'`, `'clean'`, `'synthwave'`).
  - `enable_vibrato` (*bool*): Enables 5.8 Hz LFO standing-wave frequency modulation.

#### `set_preset(preset_name: str, enable_vibrato: Optional[bool] = None)`
- Dynamically shifts sonic profile and re-synthesizes chord buffers in real-time.

#### `play_chord(chord_name: str, velocity: float = 1.0, direction: int = 1)`
- Triggers acoustic playback of target chord with directional rake sweep (down-strum bass-to-treble, up-strum treble-to-bass) and tube amplifier non-linear overdrive.
- **Latency:** Strictly $<8\text{ms}$.

#### `play_single_string(chord_name: str, string_index: int, velocity: float = 1.0)`
- Triggers acoustic playback of an individual isolated string within the current chord voicing, enabling articulate solo shredding without cutting off previous polyphony.

---

### 4. `core.rhythm_manager.RhythmManager`
Spatial Highway interactive rhythm game engine.

#### `update(current_time: float, string_segments: List[Tuple])`
- Advances trajectories of falling neon targets and calculates interpolated screen coordinates.

#### `check_hit(strum_event: dict) -> Optional[dict]`
- Evaluates timing window for current strum collision against active targets.
- Dispatches `'PERFECT'`, `'GOOD'`, or `'MISS'` scores and updates combo multipliers.

---

## 🎨 UI Modules

### 5. `ui.visualizer.Visualizer`
Renders the photorealistic Fender Stratocaster electric guitar, organic vector hand anatomy matching reference illustration, vibrating neon strings, and volumetric pyrotechnic flame systems.

#### `__init__(num_strings=4, enable_pyro=True, enable_floating_notes=True, enable_vibrato=False)`
- Dynamically allocates string endpoints along nut ($Y \in [340, 415]$) and bridge ($Y \in [305, 475]$) providing ~50px picking zone separation.
- Activates Stage Pyrotechnic Flame Cannons (`VolumetricFlameSystem`), Floating Musical Notes VFX, and Transverse Wave Vibrato.

#### `generate_string_sources(num_strings: int) -> List[Tuple]`
- Static mathematical generator distributing any string count $N \in [3, 6]$ with natural ergonomic spacing across the instrument neck and bridge.

#### `update_oud_anchors(fret_hand, strum_hand, width, height) -> List[Tuple]`
- Computes Unified Affine Transform Matrix $\mathbf{M}$ locking guitar neck and strings to human joints with velocity-adaptive EMA stabilization.

#### `trigger_pluck(s_idx: int, px: int, gain: float = 1.0, chord_name: str = 'C')`
- Triggers dynamic string vibration, shockwave ripple, chord-reactive multi-color stage bloom, volumetric flame eruption (gain > 0.60), and floating musical glyphs.

#### `render(frame, fret_hand, strum_hand, rhythm_manager, active_chord) -> np.ndarray`
- Composites all visual layers including unbroken anatomical hand vector contours (with transverse joint creases and palmar flexion lines) and returns the finished 60 FPS presentation canvas.

---

### 6. `ui.hud.HUD`
Holographic cyberpunk head-up display.

#### `render(frame, fret_hand, strum_hand, chord_code, chord_display, fps, rhythm, gain, power_level) -> np.ndarray`
- Overlays vector electric guitar logo badge, audio VU spectrum, mode indicator, and rotary power dial.

---

## 🔬 Scientific & Academic Treatises

1. **[Computational Acoustics & Digital Waveguide Specification](file:///c:/Users/DELL/Desktop/مشاريع/AeroFret%20Kinetic/docs/ACOUSTIC_PHYSICS_SPEC.md)**:
   - Digital waveguide PDEs, Karplus-Strong difference equations, inharmonicity coefficients, hyperbolic tangent saturation curves, and psychoacoustic latency budgeting.
2. **[Upper Extremity Biomechanics & Kinematics Specification](file:///c:/Users/DELL/Desktop/مشاريع/AeroFret%20Kinetic/docs/KINEMATIC_BIOMECHANICS.md)**:
   - Musculoskeletal ergonomics, 21-joint temporal filters, Continuous Swept-Line Collision Detection (CCD) determinant mathematics, and repetitive strain injury (RSI) prevention.
