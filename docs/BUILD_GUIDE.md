# 📦 AeroFret: Kinetic — Standalone Build & Distribution Guide
## دليل التجميع والتوزيع الشامل لبرنامج AeroFret: Kinetic

> **"From Pure Mathematical Code to a Production-Ready Windows Executable."**  
> **Author & Systems Architect:** **Mahmoud Labib**  
> *Transdisciplinary Researcher in HCI • HCT • HCC • STS*

---

## 📑 Table of Contents / المحتويات

1. [Overview / نظرة عامة](#1-overview--نظرة-عامة)
2. [Prerequisites & System Requirements / المتطلبات الأساسية](#2-prerequisites--system-requirements)
3. [Method A: Instant Native Execution (No Build Required) / التشغيل المباشر](#3-method-a-instant-native-execution-no-build-required)
4. [Method B: 1-Click Local Build via Batch Script / التجميع المحلي بنقرة واحدة](#4-method-b-1-click-local-build-via-batch-script)
5. [Method C: Advanced Python CLI Build / التجميع اليدوي المتقدم](#5-method-c-advanced-python-cli-build)
6. [Method D: Automated Cloud CI/CD Build (GitHub Actions) / التجميع السحابي التلقائي](#6-method-d-automated-cloud-cicd-build-github-actions)
7. [PyInstaller Architecture & Bundling Details / كواليس التجميع](#7-pyinstaller-architecture--bundling-details)
8. [Troubleshooting Build Issues / استكشاف أخطاء التجميع وحلها](#8-troubleshooting-build-issues)

---

## 1. Overview / نظرة عامة

AeroFret: Kinetic can be distributed and executed in two primary forms:
1. **Source Code Execution:** Runs directly via Python with sub-8ms audio latency and instant startup.
2. **Standalone Windows Application (`.exe`):** Bundled into a standalone binary distribution with Python runtime, OpenCV, MediaPipe, CustomTkinter, and all 36+ assets self-contained, allowing anyone on Windows to run the application without installing Python or dependencies.

---

## 2. Prerequisites & System Requirements

| Requirement | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 (64-bit) | Windows 10 / 11 (64-bit) |
| **Python Environment** | Python 3.10 | Python 3.11 (64-bit) |
| **Free Disk Space (Running Source)** | ~ 250 MB | ~ 500 MB |
| **Free Disk Space (Building EXE)** | ~ 1.8 GB (temporary build cache) | $\ge 3.0\text{ GB}$ |
| **Camera** | 720p USB 2.0 Webcam | 1080p 60 FPS MJPG Webcam |
| **Audio** | Standard Stereo Speakers / Headphones | Low-latency ASIO / DirectSound |

---

## 3. Method A: Instant Native Execution (No Build Required)
### التشغيل المباشر الفوري بدون الحاجة للتجميع

If you simply want to play, practice, or explore the software, **you do NOT need to build an `.exe` file**. The native Python implementation runs with zero overhead:

```bash
# 1. Clone or download the repository
git clone https://github.com/mahmoudmma667-gif/AeroFret-Kinetic-AR.git
cd AeroFret-Kinetic-AR

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Launch Studio Control Center (GUI)
python launcher.py
# or double click: run.bat
```

---

## 4. Method B: 1-Click Local Build via Batch Script
### التجميع المحلي بنقرة واحدة عبر الملف الدفعي

To generate a standalone Windows application distribution on your local machine:

1. Ensure your **C: drive has at least 1.5 GB to 2.0 GB of free space** for temporary compiler cache.
2. Double-click the file:
   ```
   build_standalone.bat
   ```
3. The automated builder will:
   - Verify `pyinstaller` installation (auto-installs if missing).
   - Ingest [assets](file:///c:/Users/DELL/Desktop/مشاريع/AeroFret%20Kinetic/assets) folder, icons, and themes.
   - Collect MediaPipe machine-learning inference models and CustomTkinter fonts.
   - Output the finished bundle in:
     ```
     dist/AeroFret_Kinetic/AeroFret_Kinetic.exe
     ```

---

## 5. Method C: Advanced Python CLI Build
### التجميع اليدوي المتقدم عبر بايثون

You can run the builder directly with custom Python flags:

```bash
# Execute the custom build tool
python tools/build_exe.py
```

Under the hood, this executes the optimized PyInstaller command:
```bash
python -m PyInstaller \
  --name=AeroFret_Kinetic \
  --onedir \
  --windowed \
  --icon=assets/app_icon.ico \
  --add-data="assets;assets" \
  --collect-all=customtkinter \
  --collect-all=mediapipe \
  --collect-submodules=core \
  --collect-submodules=ui \
  --hidden-import=PIL._tkinter_finder \
  --hidden-import=sounddevice \
  --hidden-import=pygame \
  --hidden-import=cv2 \
  --hidden-import=numpy \
  --clean \
  --noconfirm \
  launcher.py
```

---

## 6. Method D: Automated Cloud CI/CD Build (GitHub Actions)
### التجميع السحابي التلقائي بدون استهلاك مساحة على جهازك

If your local computer has limited hard drive space (< 2 GB free), you can let **GitHub Actions** build the `.exe` for you in the cloud for free:

1. Push your code to your GitHub repository.
2. Navigate to the **Actions** tab on GitHub.
3. The `Build Standalone Windows Release` workflow runs automatically on Windows Server runners equipped with 30+ GB of SSD space.
4. Download the compiled `AeroFret_Kinetic_Windows_x64.zip` directly from GitHub Releases or workflow artifacts!

---

## 7. PyInstaller Architecture & Bundling Details

### Why `--onedir` instead of `--onefile`?
- **Sub-Second Cold Start:** `--onefile` compresses everything into a massive single executable that decompresses 1.2 GB of temporary DLLs into `%TEMP%` on **every single launch**, causing an 8–15 second startup lag.
- `--onedir` unpacks binaries once during build time, resulting in **instant 0.4s launch speeds** and 100% stable MediaPipe TFLite model resolution.

### Runtime Asset Resolution (`sys._MEIPASS`)
When frozen inside a PyInstaller executable, standard relative paths like `os.path.dirname(__file__)` point to temporary directories. AeroFret resolves this via [core/config.py](file:///c:/Users/DELL/Desktop/مشاريع/AeroFret%20Kinetic/core/config.py):

```python
def _get_base_dir() -> str:
    """Returns project root directory or PyInstaller _MEIPASS extraction path."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

---

## 8. Troubleshooting Build Issues

### Error: `OSError: [Errno 28] No space left on device`
- **Cause:** Drive C: has insufficient free space (< 1.5 GB) to complete the `COLLECT` phase.
- **Solution:** 
  1. Empty your Recycle Bin.
  2. Clear temporary files: Press `Win + R`, type `%temp%`, and delete unnecessary files.
  3. Re-run `build_standalone.bat`.

### Error: `ModuleNotFoundError: No module named 'customtkinter'`
- **Cause:** Dependencies not installed in the active Python environment.
- **Solution:**
  ```bash
  pip install -r requirements.txt
  ```

### Pre-Flight System Verification
Run the diagnostic doctor anytime to confirm your system is 100% ready:
```bash
python tools/doctor.py
# or double-click: run_diagnostics.bat
```
