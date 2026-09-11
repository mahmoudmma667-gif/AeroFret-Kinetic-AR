# 📜 Changelog — AeroFret: Kinetic

All notable changes, architectural milestones, and performance breakthroughs across the AeroFret lifecycle.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-09-11
### ⚡ "Extreme Velocity & Spatial HCI Studio Suite"
#### Added
- **Continuous Collision Detection (CCD):** Implemented swept-ray line-segment determinant intersection to eliminate dropped notes during extreme-velocity arm sweeps (>10,000 px/s).
- **Sub-40ms Rapid Alternate Picking (Tremolo Shredding):** Directional debounce mechanics allowing rapid up-down shredding without note choking.
- **Centralized Architecture (`core/config.py`):** Unified typed configuration dataclasses for audio, video, physics, theme, and filesystem paths.
- **Pre-Flight Health Doctor (`tools/doctor.py`):** Cyberpunk diagnostic tool verifying hardware, camera, audio, dependencies, and DPI awareness.
- **PyInstaller Bundler (`tools/build_exe.py`):** 1-click standalone `.exe` packaging script with asset inclusion.
- **Centralized Asset Management:** All 37 images organized exclusively inside `assets/`.
- **Master Encyclopedia Documentation (`DOCUMENTATION.md`):** Comprehensive 5,000+ word whitepaper featuring complete system architecture, Mermaid sequence and dataflow diagrams, mathematical formulations, and Arabic/English user manuals.
- **Standard Open-Source Metadata:** Added `pyproject.toml`, `LICENSE`, `CITATION.cff`, `CITATION.bib`, and `CONTRIBUTING.md`.

---

## [1.5.0] - 2026-09-11
### 🎨 "Photorealistic Visuals & Studio Control Center"
#### Added
- **Studio Control Center (`launcher.py`):** CustomTkinter GUI featuring 10+ controls, live tone audition pads, and Win32 DPI scaling.
- **3D Anatomical Hands:** Virtual Stage Mode with realistic keratinized fingernails, lunula, PIP/DIP knuckle creases, and palm lines.
- **Candy Red Lacquer Fender Stratocaster:** Enhanced saturation and contrast on physical guitar body.
- **Holographic HUD Logo:** Audio-reactive pulsating electric guitar vector badge and 6-band dancing VU spectrum.
- **Rotary Power Dial:** Interactive circular gain dial with mouse drag and scroll wheel interaction.
- **True Win32 Borderless Fullscreen:** Eliminates titlebar flash via `user32.dll` `WS_POPUP` injection.

---

## [1.0.0] - 2026-09-10
### 🚀 "Initial Spatial Prototype"
#### Added
- Initial MediaPipe 21-landmark hand tracking pipeline.
- Procedural Karplus-Strong physical modeling audio synthesizer.
- Dynamic Fender Stratocaster mid-air kinematic anchoring.
- Interactive Guitar Hero rhythm mode with falling neon notes.
