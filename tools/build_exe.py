"""
AeroFret: Kinetic - Standalone Windows Executable Builder (PyInstaller)
Automates building a standalone single-file or folder distribution with all assets bundled.
Engineered & Developed by Mahmoud Labib.
"""

import os
import sys
import subprocess

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.version import __version__, __app_name__
from core.config import CONFIG

def build():
    print(f"Building Standalone Windows Distribution for {__app_name__} v{__version__}...")

    # Verify PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("[INFO] PyInstaller not found. Installing via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    root_dir = CONFIG.paths.PROJECT_ROOT
    assets_dir = CONFIG.paths.ASSETS_DIR
    icon_path = CONFIG.paths.APP_ICON_ICO

    # Command line arguments for PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=AeroFret_Kinetic",
        "--onedir",  # Folder mode for high reliability and instant cold startup
        "--windowed", # Windows GUI mode (no black cmd popup)
        f"--icon={icon_path}",
        f"--add-data={assets_dir};assets",
        "--collect-all=customtkinter",
        "--collect-all=mediapipe",
        "--collect-submodules=core",
        "--collect-submodules=ui",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=sounddevice",
        "--hidden-import=pygame",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--clean",
        "--noconfirm",
        os.path.join(root_dir, "launcher.py")
    ]

    print("Running command:")
    print(" ".join(cmd))
    subprocess.check_call(cmd, cwd=root_dir)
    print("\n[SUCCESS] Build complete! Output available in 'dist/AeroFret_Kinetic/'")

if __name__ == '__main__':
    build()
