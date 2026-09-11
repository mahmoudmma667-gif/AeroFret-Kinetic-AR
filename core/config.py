import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


def _get_base_dir() -> str:
    """Returns filesystem root directory or PyInstaller _MEIPASS extraction temp dir."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass(frozen=True)
class PathConfig:
    """Filesystem paths for application resources."""
    PROJECT_ROOT: str = _get_base_dir()
    ASSETS_DIR: str = os.path.join(_get_base_dir(), "assets")
    APP_ICON_ICO: str = os.path.join(ASSETS_DIR, "app_icon.ico")
    APP_ICON_PNG: str = os.path.join(ASSETS_DIR, "app_icon.png")
    GUITAR_IMAGE: str = os.path.join(ASSETS_DIR, "guitar_playing_stance.png")



@dataclass
class VideoConfig:
    """Camera capture and spatial computer vision settings."""
    DEFAULT_WIDTH: int = 1280
    DEFAULT_HEIGHT: int = 720
    TARGET_FPS: int = 60
    INFERENCE_WIDTH: int = 448
    INFERENCE_HEIGHT: int = 252
    DEFAULT_CAMERA_INDEX: int = 0
    BUFFER_SIZE: int = 1
    MIN_DETECTION_CONFIDENCE: float = 0.65
    MIN_TRACKING_CONFIDENCE: float = 0.65


@dataclass
class AudioConfig:
    """Procedural physical synthesizer and DSP parameters."""
    SAMPLE_RATE: int = 44100
    CHANNELS: int = 2
    BUFFER_SAMPLES: int = 256  # <6ms buffer latency at 44.1kHz
    DEFAULT_POWER_LEVEL: float = 0.85
    MIN_POWER_LEVEL: float = 0.10
    MAX_POWER_LEVEL: float = 1.00
    TUBE_SATURATION_BETA: float = 2.4
    EVEN_HARMONIC_WEIGHT: float = 0.12

    # Standard Karplus-Strong fundamental frequencies (Hz) for chords
    CHORD_FREQUENCIES: Dict[str, List[float]] = field(default_factory=lambda: {
        'C': [130.81, 164.81, 196.00, 261.63],     # C3, E3, G3, C4
        'Dm': [146.83, 174.61, 220.00, 293.66],    # D3, F3, A3, D4
        'Em': [164.81, 196.00, 246.94, 329.63],    # E3, G3, B3, E4
        'F': [174.61, 220.00, 261.63, 349.23],     # F3, A3, C4, F4
        'G': [196.00, 246.94, 293.66, 392.00],     # G3, B3, D4, G4
        'MUTE': [82.41, 110.00, 146.83, 196.00]    # Damped low strings
    })


@dataclass
class PhysicsConfig:
    """Continuous Collision Detection (CCD) and kinematic parameters."""
    DEFAULT_NUM_STRINGS: int = 4
    MIN_STRINGS: int = 3
    MAX_STRINGS: int = 6
    DEFAULT_DEBOUNCE_MS: float = 120.0
    PROXIMITY_THRESHOLD_PX: float = 22.0
    MIN_STRUM_VELOCITY: float = 100.0
    MAX_STRUM_VELOCITY: float = 1500.0
    RAPID_SHRED_LOCKOUT_MS: float = 40.0


@dataclass(frozen=True)
class ThemeConfig:
    """Cyberpunk color palette and aesthetic design tokens."""
    COLOR_CYAN: Tuple[int, int, int] = (255, 230, 0)       # BGR: Electric Cyan
    COLOR_YELLOW: Tuple[int, int, int] = (0, 255, 255)     # BGR: Golden Yellow
    COLOR_ORANGE: Tuple[int, int, int] = (0, 180, 255)     # BGR: Solar Orange
    COLOR_MAGENTA: Tuple[int, int, int] = (255, 0, 210)    # BGR: Hot Pink
    COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
    COLOR_BG_DARK: Tuple[int, int, int] = (18, 14, 24)

    # String colors mapped by index
    STRING_COLORS: Tuple[Tuple[int, int, int], ...] = (
        (255, 140, 0),   # Neon Electric Cyan
        (0, 255, 255),   # Golden Yellow
        (0, 180, 255),   # Solar Orange
        (255, 0, 210),   # Hot Pink / Magenta
        (0, 255, 120),   # Mint Green (5-string)
        (255, 180, 80)   # Sky Blue (6-string)
    )


@dataclass
class AppConfig:
    """Unified master configuration for AeroFret: Kinetic."""
    paths: PathConfig = field(default_factory=PathConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    theme: ThemeConfig = field(default_factory=ThemeConfig)


# Default global singleton instance
CONFIG = AppConfig()
