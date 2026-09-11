"""AeroFret: Kinetic Core Modules"""
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from .hand_tracker import HandTracker
from .gesture_engine import GestureEngine
from .audio_synth import AudioEngine
from .rhythm_manager import RhythmManager
from .version import __version__, __author__, __app_name__, get_version_info
from .config import CONFIG, AppConfig

__all__ = [
    'HandTracker',
    'GestureEngine',
    'AudioEngine',
    'RhythmManager',
    'CONFIG',
    'AppConfig',
    '__version__',
    '__author__',
    '__app_name__',
    'get_version_info'
]

