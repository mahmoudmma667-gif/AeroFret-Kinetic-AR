# 🔧 AeroFret: Kinetic — Troubleshooting & Diagnostic Guide
## دليل حل المشكلات واستكشاف الأخطاء والتشخيص

> **Author & Systems Architect:** **Mahmoud Labib**  
> *Transdisciplinary Researcher in HCI • HCT • HCC • STS*

---

## 📑 Common Scenarios & Resolutions

### 1. Camera Not Detected / Black Screen
- **Symptom:** Application launches into `[DEMO MODE: NO WEBCAM DETECTED]`.
- **Cause:** Camera is occupied by another app (Zoom, Teams, Discord) or index is wrong.
- **Solution:**
  1. Close any other applications using the webcam.
  2. In **Studio Control Center** (`launcher.py`), change **Camera Source** from `Camera 0` to `Camera 1` or `Camera 2`.
  3. Ensure Windows Camera privacy settings permit desktop applications to access the camera:
     `Windows Settings -> Privacy -> Camera -> Allow desktop apps to access your camera (ON)`.

---

### 2. Camera Running at Low Frame Rate (<30 FPS)
- **Symptom:** Sluggish video feed or stuttering.
- **Cause:** Windows USB driver defaulting to uncompressed YUY2 format over USB 2.0 bandwidth.
- **Solution:**
  - AeroFret automatically requests `MJPG` codec compression at 60 FPS.
  - Connect your webcam directly to a **USB 3.0 / USB-C** port (blue port) rather than an unpowered USB hub.
  - Ensure ambient lighting is adequate (webcams automatically drop FPS in very dark rooms to compensate for exposure).

---

### 3. Hand Tracking Jitter in Dim Environments
- **Symptom:** The guitar neck vibrates slightly when your hands are stationary.
- **Solution:**
  1. AeroFret includes automatic **CLAHE** histogram equalization, but optimal performance requires reasonable room lighting.
  2. In **Studio Control Center**, adjust the **Tracking Confidence** slider to `0.70` or `0.75`.
  3. Avoid strong direct backlighting (e.g., sitting directly in front of a bright sunny window).

---

### 4. Audio Crackling or Audio Delay
- **Symptom:** Audio has static or latency feels delayed.
- **Solution:**
  - AeroFret operates with a ultra-low 256-sample ring buffer (<6ms latency).
  - If your audio driver crackles, ensure your audio device's default sample rate in Windows is set to **44,100 Hz (16-bit or 24-bit CD/Studio Quality)**:
    `Sound Settings -> Device Properties -> Additional Device Properties -> Advanced -> Default Format -> 24-bit, 44100 Hz`.

---

### 5. Building Standalone Executable Fails (`No space left on device`)
- **Symptom:** `build_standalone.bat` fails with `OSError: [Errno 28] No space left on device`.
- **Cause:** Drive C: has less than 1.5 GB of free space required for PyInstaller compilation.
- **Solution:**
  1. Empty your Windows Recycle Bin.
  2. Run Windows Disk Cleanup (`cleanmgr.exe`).
  3. Delete temporary files in `%TEMP%`.
  4. Or run the software natively without building an executable:
     ```bash
     python launcher.py
     ```
     *(Runs instantly at full 60 FPS without consuming any build disk space).*

---

### 6. Running System Diagnostics Anytime
Whenever in doubt, run the automated health doctor check:
```bash
python tools/doctor.py
# or double-click: run_diagnostics.bat
```
This utility audits all 10 system layers and flags any configuration warnings immediately!
