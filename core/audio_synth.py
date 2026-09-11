"""
AeroFret: Kinetic - Audio Synthesis Engine
High-Power Procedural Physical-Modeling Electric & Acoustic Guitar Synthesizer.
Zero external asset dependencies: generates pure, loud, punchy polyphonic guitar chords
via Karplus-Strong physical modeling, tube saturation overdrive, and ultra-low latency playback.
"""

import os
import math
import time
import random
from typing import Optional, List, Dict, Tuple
import numpy as np

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
try:
    import pygame
    import pygame.sndarray
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False


class AudioEngine:
    """
    High-power procedural audio engine synthesizing punchy electric guitar chords
    with maximum headroom, tube saturation crunch, and instant polyphonic response.
    """

    SAMPLE_RATE = 44100
    BUFFER_SIZE = 256  # Ultra-low latency ~5.8ms buffer

    CHORD_FREQS = {
        'C': [130.81, 164.81, 196.00, 261.63, 329.63, 392.00],        # C3, E3, G3, C4, E4, G4 (Root, 3rd, 5th, Octave, 10th, 12th)
        'Dm': [146.83, 220.00, 293.66, 349.23, 440.00, 587.33],       # D3, A3, D4, F4, A4, D5
        'Em': [82.41, 123.47, 164.81, 196.00, 246.94, 329.63],        # E2, B2, E3, G3, B3, E4 (Full open 6-string Em)
        'F': [87.31, 130.81, 174.61, 220.00, 261.63, 349.23],         # F2, C3, F3, A3, C4, F4 (Barre F)
        'G': [98.00, 123.47, 146.83, 196.00, 246.94, 392.00],         # G2, B2, D3, G3, B3, G4 (Full open 6-string G)
        'MUTE': [110.0]                                               # Damped percussive thud
    }

    PRESETS = {
        'overdrive': {'name': 'Heavy Metal Overdrive', 'drive': 2.8, 'decay': 0.995, 'blend_ks': 0.55, 'blend_hm': 0.45},
        'crunch': {'name': 'Rock & Blues Crunch', 'drive': 1.65, 'decay': 0.992, 'blend_ks': 0.65, 'blend_hm': 0.35},
        'clean': {'name': 'Clean Stratocaster', 'drive': 0.88, 'decay': 0.988, 'blend_ks': 0.80, 'blend_hm': 0.20},
        'synthwave': {'name': 'Synthwave Cyberpunk', 'drive': 2.4, 'decay': 0.996, 'blend_ks': 0.30, 'blend_hm': 0.70}
    }

    def __init__(
        self,
        sample_rate: int = 44100,
        buffer_size: int = 256,
        preset: str = 'overdrive',
        enable_vibrato: bool = False
    ):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.preset = preset.lower() if preset.lower() in self.PRESETS else 'overdrive'
        self.enable_vibrato = enable_vibrato
        self.backend = None
        self.sounds = {}
        self.raw_waveforms = {}
        self.single_string_sounds = {}
        self.single_string_waveforms = {}
        self.is_initialized = False

        # Humanized micro-dynamics & tempo tracking
        self.recent_strum_times: List[float] = []
        self.strum_count = 0

        self._init_audio_backend()
        self._precompute_chords()

    def set_preset(self, preset_name: str, enable_vibrato: Optional[bool] = None):
        """Dynamically switches tone model (Overdrive, Crunch, Clean, Synthwave) and re-synthesizes chords and strings."""
        norm_name = preset_name.lower()
        for k in self.PRESETS.keys():
            if k in norm_name:
                self.preset = k
                break
        if enable_vibrato is not None:
            self.enable_vibrato = enable_vibrato
        self._precompute_chords()

    def _init_audio_backend(self):
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.pre_init(
                    frequency=self.sample_rate,
                    size=-16,
                    channels=2,
                    buffer=self.buffer_size
                )
                pygame.mixer.init()
                pygame.mixer.set_num_channels(32)
                self.backend = 'pygame'
                self.is_initialized = True
                return
            except Exception as e:
                print(f"[AudioEngine] Warning: Pygame mixer init failed ({e}). Trying sounddevice...")

        if SOUNDDEVICE_AVAILABLE:
            try:
                sd.check_output_settings(samplerate=self.sample_rate, channels=2)
                self.backend = 'sounddevice'
                self.is_initialized = True
                return
            except Exception as e:
                print(f"[AudioEngine] Warning: Sounddevice init failed ({e}).")

        self.backend = 'dummy'
        self.is_initialized = False

    @staticmethod
    def _synthesize_karplus_strong(freq: float, duration: float, sample_rate: int, decay: float = 0.993) -> np.ndarray:
        n_samples = int(sample_rate * duration)
        period = int(sample_rate / freq)
        if period <= 0:
            period = 1

        rng = np.random.default_rng()
        # High-energy pluck burst
        pluck_noise = rng.uniform(-1.0, 1.0, period).astype(np.float32)
        # Gentle smoothing for authentic pick attack
        pluck_noise = np.convolve(pluck_noise, np.ones(3)/3.0, mode='same')

        samples = np.zeros(n_samples, dtype=np.float32)
        samples[:period] = pluck_noise

        for i in range(period, n_samples):
            samples[i] = 0.5 * (samples[i - period] + samples[i - period + 1 if i - period + 1 < n_samples else 0]) * decay

        return samples

    @staticmethod
    def _synthesize_guitar_harmonic(freq: float, duration: float, sample_rate: int) -> np.ndarray:
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False, dtype=np.float32)
        sig = np.zeros_like(t)

        harmonics = [
            (1.0, 0.70, 2.0),   # Fundamental (loud)
            (2.0, 0.50, 3.2),   # Octave
            (3.0, 0.35, 4.5),   # 5th
            (4.0, 0.22, 5.8),   # 2nd Octave
            (5.0, 0.15, 7.2),   # 3rd
            (6.0, 0.10, 8.8)    # Overtone
        ]

        for mult, amp, decay_rate in harmonics:
            harmonic_freq = freq * mult
            if harmonic_freq > sample_rate / 2.0:
                continue
            phase = 2.0 * math.pi * harmonic_freq * t
            envelope = amp * np.exp(-decay_rate * t)
            sig += envelope * np.sin(phase)

        # Pick attack transient
        attack_env = np.exp(-48.0 * t)
        sig += 0.25 * attack_env * np.sin(2.0 * math.pi * (freq * 4.0) * t)
        return sig

    def _precompute_chords(self):
        """Precomputes down-strums, up-strums, and all individual string notes for 0-latency playback."""
        self.sounds.clear()
        self.raw_waveforms.clear()
        self.single_string_sounds.clear()
        self.single_string_waveforms.clear()

        preset_cfg = self.PRESETS.get(self.preset, self.PRESETS['overdrive'])
        decay = preset_cfg['decay']
        drive = preset_cfg['drive']
        blend_ks = preset_cfg['blend_ks']
        blend_hm = preset_cfg['blend_hm']

        for name, freqs in self.CHORD_FREQS.items():
            if name == 'MUTE':
                duration = 0.28
                n_samples = int(self.sample_rate * duration)
                t = np.linspace(0, duration, n_samples, endpoint=False, dtype=np.float32)
                noise = np.random.uniform(-1.0, 1.0, n_samples).astype(np.float32)
                thud = np.sin(2.0 * math.pi * 95.0 * t)
                mono = (0.75 * thud + 0.35 * noise) * np.exp(-28.0 * t)
                peak_m = np.max(np.abs(mono))
                if peak_m > 1e-4:
                    mono = mono / peak_m * 0.95
                stereo = np.column_stack((mono, mono)).astype(np.float32)
                self.raw_waveforms['MUTE'] = stereo
                self.raw_waveforms['MUTE_down'] = stereo
                self.raw_waveforms['MUTE_up'] = stereo
                self.single_string_waveforms[('MUTE', 0)] = stereo
                if self.backend == 'pygame':
                    snd = pygame.sndarray.make_sound((np.clip(stereo, -1.0, 1.0) * 32767).astype(np.int16))
                    self.sounds['MUTE'] = snd
                    self.sounds['MUTE_down'] = snd
                    self.sounds['MUTE_up'] = snd
                    self.single_string_sounds[('MUTE', 0)] = snd
                continue

            duration = 2.4
            n_samples = int(self.sample_rate * duration)
            str_mono_list = []

            # Synthesize each string's physical note once
            for str_i, f in enumerate(freqs):
                ks = self._synthesize_karplus_strong(f, duration, self.sample_rate, decay=decay)
                hm = self._synthesize_guitar_harmonic(f, duration, self.sample_rate)
                blended = blend_ks * ks + blend_hm * hm
                if self.preset == 'synthwave':
                    t_str = np.linspace(0, duration, len(blended), endpoint=False, dtype=np.float32)
                    saw = 0.25 * (2.0 * (t_str * f - np.floor(0.5 + t_str * f)))
                    sub = 0.20 * np.sign(np.sin(2.0 * math.pi * (f * 0.5) * t_str))
                    blended = 0.60 * blended + (saw + sub) * np.exp(-2.2 * t_str)

                # Store single note waveform
                note_copy = np.copy(blended)
                if self.enable_vibrato:
                    t_all = np.linspace(0, duration, len(note_copy), endpoint=False, dtype=np.float32)
                    note_copy *= (1.0 + 0.024 * np.sin(2.0 * math.pi * 6.2 * t_all) * (1.0 - np.exp(-3.0 * t_all)))
                peak_n = np.max(np.abs(note_copy))
                if peak_n > 1e-4:
                    note_copy = np.tanh(note_copy / peak_n * drive) * 1.0
                stereo_note = np.column_stack((note_copy * 0.99, note_copy * 0.99)).astype(np.float32)
                self.single_string_waveforms[(name, str_i)] = stereo_note
                if self.backend == 'pygame':
                    self.single_string_sounds[(name, str_i)] = pygame.sndarray.make_sound(
                        (np.clip(stereo_note, -1.0, 1.0) * 32767).astype(np.int16)
                    )

                str_mono_list.append(blended)

            # Compose down-strum (normal rake, 13ms stagger)
            chord_down = np.zeros(n_samples, dtype=np.float32)
            stagger_d = int(0.013 * self.sample_rate)
            for idx, sm in enumerate(str_mono_list):
                off = idx * stagger_d
                if off < n_samples:
                    L = min(len(sm), n_samples - off)
                    chord_down[off:off + L] += sm[:L]

            # Compose up-strum (reverse rake, 10ms snap)
            chord_up = np.zeros(n_samples, dtype=np.float32)
            stagger_u = int(0.010 * self.sample_rate)
            for idx, sm in enumerate(reversed(str_mono_list)):
                off = idx * stagger_u
                if off < n_samples:
                    L = min(len(sm), n_samples - off)
                    chord_up[off:off + L] += sm[:L]

            for c_mono, key_suffix in [(chord_down, 'down'), (chord_up, 'up')]:
                if self.enable_vibrato:
                    t_all = np.linspace(0, duration, n_samples, endpoint=False, dtype=np.float32)
                    c_mono *= (1.0 + 0.028 * np.sin(2.0 * math.pi * 5.8 * t_all) * (1.0 - np.exp(-3.5 * t_all)))
                peak = np.max(np.abs(c_mono))
                if peak > 1e-4:
                    c_mono = np.tanh(c_mono / peak * drive) * 1.0
                stereo_chord = np.column_stack((c_mono * 0.99, c_mono * 0.99)).astype(np.float32)
                self.raw_waveforms[f"{name}_{key_suffix}"] = stereo_chord
                if key_suffix == 'down':
                    self.raw_waveforms[name] = stereo_chord
                if self.backend == 'pygame':
                    snd = pygame.sndarray.make_sound((np.clip(stereo_chord, -1.0, 1.0) * 32767).astype(np.int16))
                    self.sounds[f"{name}_{key_suffix}"] = snd
                    if key_suffix == 'down':
                        self.sounds[name] = snd

    def play_single_string(self, chord_name: str, string_index: int, velocity: float = 1.0):
        """
        Plays a crisp, articulate individual scale note for melodic solo picking.
        Polyphonic: does not cut off other ringing notes.
        """
        if chord_name not in self.CHORD_FREQS:
            chord_name = 'C'

        freqs = self.CHORD_FREQS[chord_name]
        clamped_idx = string_index % len(freqs)
        key = (chord_name, clamped_idx)
        volume = float(np.clip(velocity, 0.15, 1.0))

        if self.backend == 'pygame':
            try:
                sound = self.single_string_sounds.get(key)
                if sound is None and chord_name in self.sounds:
                    sound = self.sounds[chord_name]
                if sound:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        # Subtle stereo panning based on string position (bass=left, treble=right)
                        pan_right = 0.35 + 0.30 * (clamped_idx / max(1, len(freqs) - 1))
                        pan_left = 1.0 - pan_right
                        channel.set_volume(volume * pan_left, volume * pan_right)
                        channel.play(sound)
            except Exception as e:
                print(f"[AudioEngine] Single-string playback error: {e}")

        elif self.backend == 'sounddevice':
            try:
                waveform = self.single_string_waveforms.get(key)
                if waveform is not None:
                    scaled = (waveform * volume).astype(np.float32)
                    sd.play(scaled, samplerate=self.sample_rate, blocking=False)
            except Exception as e:
                print(f"[AudioEngine] Sounddevice single-string error: {e}")

    def play_chord(self, chord_name: str, velocity: float = 1.0, direction: int = 1):
        """
        Plays a full, rich chord with directional stroke nuance and human micro-dynamics.
        direction: +1 for down-strum, -1 for up-strum.
        """
        if chord_name not in self.CHORD_FREQS:
            chord_name = 'C'

        self.strum_count += 1
        now = time.time()
        self.recent_strum_times.append(now)
        # Keep recent 2.0s strum history
        self.recent_strum_times = [t for t in self.recent_strum_times if now - t < 2.0]

        # Expressive human velocity micro-variation (+/- 4%)
        human_jitter = 1.0 + random.uniform(-0.04, 0.04)
        volume = float(np.clip(velocity * human_jitter, 0.15, 1.0))

        # Select directional sound
        sound_key = f"{chord_name}_up" if direction < 0 else f"{chord_name}_down"

        if self.backend == 'pygame':
            try:
                sound = self.sounds.get(sound_key) or self.sounds.get(chord_name)
                if sound:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        # Slightly alternate stereo field for live organic room feel
                        pan_offset = random.uniform(-0.06, 0.06)
                        channel.set_volume(
                            float(np.clip(volume * (1.0 - pan_offset), 0.1, 1.0)),
                            float(np.clip(volume * (1.0 + pan_offset), 0.1, 1.0))
                        )
                        channel.play(sound)
            except Exception as e:
                print(f"[AudioEngine] Playback error: {e}")

        elif self.backend == 'sounddevice':
            try:
                waveform = self.raw_waveforms.get(sound_key) or self.raw_waveforms.get(chord_name)
                if waveform is not None:
                    scaled = (waveform * volume).astype(np.float32)
                    sd.play(scaled, samplerate=self.sample_rate, blocking=False)
            except Exception as e:
                print(f"[AudioEngine] Sounddevice error: {e}")

    def stop_all(self):
        if self.backend == 'pygame':
            pygame.mixer.stop()
        elif self.backend == 'sounddevice':
            sd.stop()
