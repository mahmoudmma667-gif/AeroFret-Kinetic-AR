# 🎸 AR AeroFret: Kinetic (Touchless Spatial Air Guitar Simulator)
### Augmented Reality Musical Spatial Computing • Real-Time Computer Vision • Sub-8ms Procedural Acoustics
> *"Strings of Light, Music of Motion: Where Musculoskeletal Biomechanics Meets Computational Acoustics."*  
> **Principal Investigator & Systems Architect:** **Mahmoud Labib**  
> *Transdisciplinary Researcher at the Nexus of Human-Computer Interaction (HCI), Human-Centered Technology (HCT), Human-Centered Computing (HCC), and Science, Technology & Society (STS).*

---

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MediaPipe Version](https://img.shields.io/badge/MediaPipe-Hands_v0.10.14-00C7B7?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![OpenCV Version](https://img.shields.io/badge/OpenCV-v5.0.0-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Audio Latency](https://img.shields.io/badge/Audio_Latency-%3C8ms_Ultra--Low-00E5FF?style=for-the-badge&logo=speaker&logoColor=black)]()
[![Frame Rate](https://img.shields.io/badge/FPS-60_Solid_Realtime-00FFAA?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT_Open_Access-FF007F?style=for-the-badge)](LICENSE)
[![Doctor Health](https://img.shields.io/badge/System_Health-100%25_EXCELLENT-brightgreen?style=for-the-badge)]()

</div>

---

<div align="center">

## 🖼️ Project Hero Overview & Architectural Blueprint
![AR AeroFret Kinetic Infographic](assets/readme_hero_infographic.jpg)

</div>

---

## 🎬 Live Interactive Gameplay & Demonstration Video
Experience **AR AeroFret: Kinetic** in action. The video below demonstrates real-time spatial hand tracking, sub-8ms Karplus-Strong string synthesis, directional strumming sweeps, dynamic chord switching, and interactive Guitar Hero rhythm gameplay:

<div align="center">

<iframe src="https://drive.google.com/file/d/1DgHXcSM3Gk2akURZVJK5H97WfAJJyL5D/preview" width="100%" height="480" allow="autoplay; fullscreen" frameborder="0" style="border-radius: 12px; box-shadow: 0px 8px 24px rgba(0,229,255,0.25);"></iframe>

<br/><br/>

[![Watch on Google Drive](https://img.shields.io/badge/▶_Watch_Full_HD_Video_on_Google_Drive-4285F4?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1DgHXcSM3Gk2akURZVJK5H97WfAJJyL5D/view?usp=drivesdk)
[![Download Gameplay MP4](https://img.shields.io/badge/📥_Direct_Video_Link-00E5FF?style=for-the-badge&logo=video&logoColor=black)](https://drive.google.com/file/d/1DgHXcSM3Gk2akURZVJK5H97WfAJJyL5D/view?usp=drivesdk)

</div>

---

## 📑 Table of Contents / فهرس المحتويات
1. [Executive Summary / الملخص التنفيذي](#-executive-summary)
2. [Target Audiences & Societal Purpose / الفئات المستهدفة وأهداف المشروع](#-target-audiences--societal-purpose)
3. [The Transdisciplinary Theoretical Framework (HCI • HCT • HCC • STS)](#-the-transdisciplinary-theoretical-framework)
4. [Master Feature Highlights & Game Modes](#-master-feature-highlights--game-modes)
5. [Visual Showcase & Mode Gallery](#-visual-showcase--mode-gallery)
6. [System Architecture & Dataflow (Mermaid Diagrams)](#-system-architecture--dataflow)
7. [Step-by-Step Installation & Download Guide / دليل التنزيل والتشغيل](#-step-by-step-installation--download-guide)
8. [Interaction Controls & Cheat Sheet](#-interaction-controls--cheat-sheet)
9. [الدليل الموسوعي الشامل باللغة العربية](#-الدليل-الموسوعي-الشامل-باللغة-العربية)
10. [Intellectual Property, Licensing & Academic Citation](#-intellectual-property-licensing--academic-citation)
11. [Search Engine & AI Discovery Metadata](#-search-engine--ai-discovery-metadata)

---

## 🌟 Executive Summary
**AR AeroFret: Kinetic** is an open-access, studio-grade augmented reality air guitar performance suite and spatial computing rhythm game. Designed and developed by transdisciplinary researcher **Mahmoud Labib**, the project turns any standard PC, laptop, or commodity webcam into a responsive musical instrument.

Without requiring specialized hardware, VR headsets, wearable sensors, electronic gloves, or physical instruments:
- **Left Hand:** Physically grips and orients a photorealistic Fender Stratocaster neck in 3D mid-air space. Finger extension cardinality instantly governs harmonic triads (C, Dm, Em, F, G, and Palm Mute).
- **Right Hand:** The index fingertip serves as an optical laser plectrum, triggering individual strings or full chords with real-time physical velocity ($dy/dt$) gain modulation.
- **Computational Audio Engine:** Fully procedural physical string modeling (Karplus-Strong DSP + tube overdrive saturation) responding in **under 8 milliseconds**, inducing an embodied **phantom haptic illusion** of physical string resistance.
- **Visual Engine:** Delivers solid 60 FPS real-time compositing with dynamic string vibration physics, mother-of-pearl fret markers, particle sparks, chromatic shockwaves, volumetric concert stage spotlights, and authentic 3D hand anatomy.

---

## 🎯 Target Audiences & Societal Purpose

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AR AEROFRET KINETIC: CORE AUDIENCE MATRIX                       │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 🎓 Academic & STEM Students│ 🎵 Music Education Faculty │ ♿ Inclusive Accessibility   │
│ • Computer Vision (OpenCV) │ • Faculty of Music Educ.   │ • Motor Rehabilitation       │
│ • Kinematics & MediaPipe   │ • Triad & Ear Training     │ • Zero Hand Grip Fatigue     │
│ • Real-time DSP Acoustics  │ • Pain-free Callus-free    │ • Assistive Spatial Music    │
├────────────────────────────┼────────────────────────────┼──────────────────────────────┤
│ 🎮 Gamers & Air-Guitarists │ 🔬 Transdisciplinary HCI   │ 🌍 Socio-Economic Equity     │
│ • Guitar Hero Rhythm Game  │ • Sensorimotor Cortex STS  │ • $0 Hardware Barrier        │
│ • Free-play Solo Shredding │ • Don Norman Natural Map   │ • Dematerialized Software    │
└────────────────────────────┴────────────────────────────┴──────────────────────────────┘
```

### 1. 🎓 University & STEM Students (Computer Vision, AI & Software Engineering)
- **Living Pedagogical Codebase:** Provides students and researchers with a production-grade blueprint for integrating Computer Vision (OpenCV, MediaPipe), real-time physical DSP audio synthesis (Karplus-Strong algorithm), and GUI architecture (CustomTkinter) in Python.
- **Algorithm Demonstrator:** Demonstrates continuous swept-line collision detection (CCD), velocity-adaptive exponential smoothing (EMA), and affine perspective matrix mapping.

### 2. 🎵 Music Education Students & Conservatories (تربية موسيقية ومعاهد الكونسرفتوار)
- **Democratizing Instrument Learning:** Traditional guitar education suffers from high dropout rates caused by painful epidermal finger calluses, hand cramps, and tendon strain during initial barre chord mastery.
- **Instant Harmonic Fluency:** Students master fundamental harmonic progressions (Tonic $\rightarrow$ Subdominant $\rightarrow$ Dominant $\rightarrow$ Tonic) in under 60 seconds through natural finger cardinality (1=C, 2=Dm, 3=Em, 4=F, 5=G).
- **Rhythm & Timing Coordination:** The built-in Guitar Hero mode trains ear-to-hand synchronization and tempo consistency without instrument maintenance hurdles.

### 3. ♿ Inclusive Accessibility & Neuro-Rehabilitation (الإتاحة وإعادة التأهيل الحركي)
- **Zero-Force Musicality:** Individuals with arthritis, muscular dystrophy, or limited grip strength who cannot press high-tension steel strings can express themselves freely through gentle touchless air motions.
- **Proprioceptive Therapy:** Engages shoulder, forearm, and finger motor coordination in physical therapy and neuro-rehabilitation programs.

### 4. 🌍 Socio-Economic Equity & Art Democratization (العدالة الاجتماعية وإتاحة الفنون)
- **Abolishing the Equipment Barrier:** A quality electric guitar, tube amplifier, audio interface, and patch cables cost $1,000–$3,000+. AeroFret collapses this entire physical signal chain into zero-cost, open-source software running on hardware students already own.

---

## 🏛️ The Transdisciplinary Theoretical Framework
Conceived and theorized by **Mahmoud Labib**, AeroFret operates at the confluence of four epistemological pillars:

### 1. Human-Computer Interaction (HCI): Zero-Haptic Sensorimotor Substitution
Traditional instruments rely on epidermal mechanoreceptors (Merkel discs & Meissner corpuscles) for tactile feedback. AeroFret bridges this absence via cross-modal sensory substitution:
- **Temporal Synchrony ($<8\text{ms}$):** Cross-modal sensory integration in the human brain requires auditory and visual stimuli to coincide within $10\text{ms}$. With $<8\text{ms}$ latency from pick crossing to sound pressure, the brain undergoes sensory transfer, generating an embodied **phantom haptic illusion** of tangible string tension.

### 2. Human-Centered Technology (HCT): Musculoskeletal Biomechanical Alignment
Rather than forcing human anatomy into repetitive, unnatural postures dictated by rigid plastic peripherals:
- Hand tracking respects biological degrees of freedom: carpal flexion, thumb opposition, and radial/ulnar deviation.
- The virtual guitar dynamically conforms to the user's natural lap posture and arm span.

### 3. Human-Centered Computing (HCC): Direct Natural Mapping
Minimizes cognitive translation latency (*Don Norman, 1988*):
- Extended finger count directly corresponds to harmonic triad scale degrees ($1 = I$, $2 = ii$, $3 = iii$, $4 = IV$, $5 = V$, $\text{Fist} = \text{Mute}$). Bypasses the analytical translation bottleneck to unlock instant flow state (*Csíkszentmihályi, 1990*).

### 4. Science, Technology & Society (STS): Radical Technological Dematerialization
Abolishes physical, economic, and ecological constraints. Zero mined nickel/copper extraction for strings, zero toxic electronic waste, and zero shipping carbon footprint.

---

## ⚡ Master Feature Highlights & Game Modes

| Subsystem | Technical Specification & Innovation |
| :--- | :--- |
| **Vision Tracking** | MediaPipe BlazeHand with CLAHE adaptive contrast normalization for dark/dim rooms at 60 FPS. |
| **Collision Physics** | Continuous Swept-Line Collision Detection (Swept Ray Intersection) detects plucks even at $>3000\text{ px/s}$. |
| **Tremolo Shredding** | Directional stroke-reversal debounce ($38\text{ms}$ lockout) unlocks up to $26\text{ notes/sec}$ alternate picking. |
| **Audio Synthesizer** | Procedural Karplus-Strong string modeling with non-linear hyperbolic tangent ($\tanh$) tube saturation. |
| **Guitar Body** | High-resolution Fender Stratocaster Candy Apple Red lacquer warped in real time via unified Affine matrix $M$. |
| **Strings & Glow** | Multi-tier neon bloom (atmospheric glow, electric core, superheated white filament) with harmonic wave sine curves. |
| **Pyrotechnics** | Twin volumetric stage flame plumes with buoyancy convection, ember streaks, and optical additive blending. |

### Available Game Modes:
1. **Free-Play Air Guitar Mode:** Open jam session with real-time velocity dynamics, directional up/down strums, and single-string melodic picking.
2. **Guitar Hero Rhythm Mode (`[M]` Key):** Falling musical targets synchronized to song tempo (BPM), combo multiplier streaks (up to 4x), dynamic floating judgments (`PERFECT`, `GOOD`, `MISS`), and live scoreboard.
3. **Virtual Stage Concert Mode (`[C]` Key):** Dark stadium concert arena with sweeping dual spotlights, ambient dust motes, roaring flame cannons, and stylized 3D anatomical hands.

---

## 📸 Visual Showcase & Mode Gallery

| Free-Play Air Guitar Mode (C Major) | Virtual Stage Neon Concert Mode |
| :---: | :---: |
| ![Free Play Mode](assets/showcase_freeplay_v2.png) | ![Virtual Stage Mode](assets/showcase_virtual_stage_v2.png) |

| Guitar Hero Interactive Rhythm Mode | Palm Mute Acoustic Dampening |
| :---: | :---: |
| ![Guitar Hero Mode](assets/mode_rhythm_guitar_hero.png) | ![Palm Mute Stance](assets/mode_palm_mute_stance.png) |

| Single-String Melodic Picking | Interactive Rotary Amp Power Dial |
| :---: | :---: |
| ![Single String Picking](assets/mode_single_string_picking.png) | ![Power Dial Overdrive](assets/mode_power_dial_overdrive.png) |

| Cyberpunk Studio Control Center Launcher | Academic Epistemology & Credits Modal |
| :---: | :---: |
| ![Launcher](assets/control_center_main.png) | ![Credits Modal](assets/control_center_credits.png) |

---

## 🏛️ System Architecture & Dataflow

### High-Level Architecture Pipeline
```mermaid
flowchart TD
    subgraph Inputs["1. Hardware & Perception"]
        CAM["Webcam Feed (1280x720 @ 60 FPS)"]
        GUI["CustomTkinter Studio Control Center"]
    end

    subgraph Vision["2. Spatial Kinematics Core"]
        CLAHE["CLAHE Adaptive Contrast Normalization"]
        MP["MediaPipe Hand Inference (448x252)"]
        EMA["Velocity-Aware Kinematic EMA Filter"]
        CAM --> CLAHE --> MP --> EMA
    end

    subgraph Engine["3. Gesture & Musical Intelligence"]
        FRET["Left Hand: Finger Extension Cardinality"]
        STRUM["Right Hand: Continuous Swept-Line CCD"]
        CHORD["Harmonic Triad Classifier (C, Dm, Em, F, G, Mute)"]
        PICK["Single-String Proximity / Directional Strum"]
        EMA --> FRET --> CHORD
        EMA --> STRUM --> PICK
    end

    subgraph DSP["4. Computational Audio Engine"]
        KS["Karplus-Strong Physical String Synthesis"]
        SAT["Tube Saturation Non-Linear Overdrive (tanh)"]
        BUF["Direct Ring Buffer Streaming (<8ms)"]
        CHORD & PICK --> KS --> SAT --> BUF
    end

    subgraph Graphics["5. Visualizer & AAA HUD"]
        WARP["Affine Stratocaster Posture Warping (Matrix M)"]
        STRINGS["Radiant 4-Layer Neon Vibrating Strings"]
        HANDS["Solid 3D Fleshy Organic Hands Layering"]
        STAGE["Concert Spotlights & Volumetric Flame Cannons"]
        HUD["Holographic Glass Telemetry & Rotary Power Dial"]
        WARP --> STRINGS --> HANDS --> STAGE --> HUD
    end

    BUF --> OUT_AUDIO["Speaker / Headphone Output"]
    HUD --> OUT_SCREEN["60 FPS Borderless Fullscreen Display"]
```

### Real-Time Frame Lifecycle (Sequence Diagram)
```mermaid
sequenceDiagram
    autonumber
    actor User as Performer (Air Guitarist)
    participant Cam as Video Capture (OpenCV)
    participant Tracker as Hand Tracker (MediaPipe)
    participant Gesture as Gesture & CCD Engine
    participant Audio as Audio Engine (DSP)
    participant Vis as Visualizer & 3D Renderer
    participant Screen as Display Window

    loop Every 16.6ms (60 FPS)
        User->>Cam: Physical hand motion in camera view
        Cam->>Tracker: Raw BGR Frame (1280x720)
        Tracker->>Tracker: CLAHE Normalize + BlazeHand Inference
        Tracker->>Gesture: 21 Landmarks (Fret Hand & Strum Hand)
        Gesture->>Gesture: Evaluate Chord Cardinality + Swept CCD
        alt String Strum Detected
            Gesture->>Audio: Trigger Pluck / Chord (<8ms)
            Audio-->>User: Instant Acoustic Feedback
            Gesture->>Vis: Trigger Wave Vibration + Particles + Shockwaves
        end
        Vis->>Vis: Render Guitar Neck, Strings, 3D Hands & Stage
        Vis->>Screen: Present Composite Frame
        Screen-->>User: Visual & Auditory Sensory Convergence
    end
```

---

## 🚀 Step-by-Step Installation & Download Guide

### 📋 Prerequisites & System Requirements
| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Operating System** | Windows 10 / 11 (64-bit) | Windows 10 / 11 (64-bit) |
| **Processor** | Intel Core i3 6th Gen / AMD Ryzen 3 | Intel Core i5 8th Gen+ / AMD Ryzen 5+ |
| **Memory (RAM)** | 4 GB | 8 GB+ |
| **Camera** | Standard USB / Integrated Webcam (720p @ 30 FPS) | 720p / 1080p @ 60 FPS |
| **Python Environment** | Python 3.10, 3.11, or 3.12 (64-bit) | Python 3.11.9 (64-bit) |

---

### Option A: 1-Click Launchers (Windows Users — Fastest)
Double-click either of the pre-configured launcher scripts in the repository root:
1. **`شغل_لوحة_التحكم.bat`** (or `run.bat`): Opens the **Cyberpunk Studio Control Center GUI** to configure camera, BPM, power dial, audio presets, and string count.
2. **`شغل_اللعبة.bat`**: Directly launches the full-screen game session immediately.

---

### Option B: Standard Python Setup (Git & Terminal)

#### 1. Clone the Repository
```bash
git clone https://github.com/mahmoudmma667-gif/AeroFret-Kinetic-AR.git
cd AeroFret-Kinetic-AR
```

#### 2. Create and Activate a Virtual Environment
```bash
# Windows (cmd / powershell)
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Run System Health Pre-Flight Check
Verify your camera, audio ring-buffer, assets, and dependencies in one command:
```bash
python tools/doctor.py
```
Expected output:
```text
[AEROFRET SYSTEM HEALTH: 100% EXCELLENT — READY FOR HIGH-SPEED PERFORMANCE]
```

#### 5. Run the Automated Test Suite
Confirm all 8 subsystem verification tests pass:
```bash
python -m unittest discover tests
```

#### 6. Launch the Studio Control Center
```bash
python launcher.py
```
*(Or launch the direct game loop without the launcher GUI via `python main.py`)*

---

### Option C: Anaconda / Miniconda Environment
```bash
conda create -n aerofret python=3.11 -y
conda activate aerofret
pip install -r requirements.txt
python launcher.py
```

---

## 🎮 Interaction Controls & Cheat Sheet

### 🖐️ Left Hand: Fret Hand Chord Mappings
| Hand Posture | Finger Count | Target Harmonic Chord | Acoustic Character |
| :---: | :---: | :---: | :--- |
| ✊ **Closed Fist** | **0 Fingers** | **PALM MUTE** | Acoustic harmonic dampening (percussive chug) |
| ☝️ **Index Only** | **1 Finger** | **C MAJOR** | Root tonic chord, bright and open |
| ✌️ **Index + Middle** | **2 Fingers** | **D MINOR** | Melancholic, expressive supertonic minor |
| 🤟 **3 Fingers** | **3 Fingers** | **E MINOR** | Heavy, brooding, dark metal power chord |
| 🖖 **4 Fingers** | **4 Fingers** | **F MAJOR** | Rich subdominant barre-style resonance |
| 🖐️ **Open Palm** | **5 Fingers** | **G MAJOR** | Triumphant dominant chord, rich harmonic overtone |

### ⌨️ Master Keyboard Shortcuts
| Hotkey | Action / Feature |
| :---: | :--- |
| `[F]` | **Toggle True Borderless Fullscreen** (hides OS titlebar & taskbar completely) |
| `[C]` | **Toggle Virtual Stage Mode** (dark neon concert studio & 3D hands) |
| `[M]` | **Toggle Mode** (Free-Play Air Guitar $\leftrightarrow$ Guitar Hero Rhythm Game) |
| `[R]` | **Reset Score & Combo Multiplier** (in Rhythm Game mode) |
| `[P]` | **Cycle Amp Power Level Presets** (50% $\rightarrow$ 75% $\rightarrow$ 100%) |
| `[ [ ]` / `[ ] ]` | **Fine-Tune Amp Gain & Overdrive** (Decrease / Increase by 5%) |
| `[SPACE]` | **Manual Trigger Strum** (test pluck at 65% width) |
| `[1]` – `[5]`, `[0]` | **Manual Keyboard Chord Overrides** (1=C, 2=Dm, 3=Em, 4=F, 5=G, 0=Mute) |
| `[Q]` / `[ESC]` | **Graceful Engine Shutdown** (releases camera, audio, and windows) |

---

## 🌐 الدليل الموسوعي الشامل باللغة العربية

### ما هو مشروع AeroFret: Kinetic؟
**أيرو فريت كينيتك (AeroFret: Kinetic)** هو نظام محاكاة وعزف جيتار هوائي بالواقع المعزز والحوسبة المكانية التفاعلية من ابتكار وتطوير الباحث المتعدد التخصصات **محمود لبيب**. يهدف المشروع إلى تحويل حركة الجسد البشري العادية أمام أي كاميرا ويب تقليدية إلى عزف موسيقي حقيقي متقن دون الحاجة إلى شراء آلات موسيقية أو ارتداء قفازات أو نظارات واقع افتراضي باهظة الثمن.

### أهداف المشروع ورسالته:
1. **تعليم طلاب كليات التربية الموسيقية والكونسرفتوار:**
   - التغلب على عقبة آلام الأصابع وتقرحات الأوتار المعدنية (Calluses) التي يعاني منها المبتدئون.
   - تعليم التوافق الهارموني والانتقال السلس بين الكوردات (Tonic, Subdominant, Dominant) في ثوانٍ معدودة.
   - تدريب الأذن الموسيقية والتحكم في الإيقاع الزمني عبر نمط لعبة الجيتار هيرو (Guitar Hero Mode).
2. **تعليم طلاب البرمجة والذكاء الاصطناعي والحوسبة (HCI / STEM):**
   - تقديم كود برمجي مفتوح المصدر ونموذجي يوضح كيفية الربط بين الرؤية الحاسوبية (OpenCV & MediaPipe)، والمعالجة الرقمية للإشارات الصوتية (DSP عبر خوارزمية Karplus-Strong)، وتصميم واجهات المستخدم (CustomTkinter) بمعدل 60 إطاراً في الثانية وزمن استجابة أقل من 8 ميلي ثانية.
3. **الإتاحة لذوي الاحتياجات الخاصة وإعادة التأهيل الحركي:**
   - تمكين الأشخاص الذين يعانون من ضعف عضلات اليدين أو صعوبة الإمساك بآلات ثقيلة من العزف والتعبير الفني الحر عبر حركات اليدين الهوائية.
4. **العدالة الاجتماعية وإلغاء الحاجز المادي:**
   - تكلفة الجيتار الكهربائي ومضخم الصوت والمؤثرات تفوق آلاف الدولارات؛ يختزل هذا المشروع كل تلك المعدات في برنامج ذكي مجاني يعمل على أي لابتوب.

### طريقة العزف باختصار:
- **اليد اليسرى:** تمسك عنق الجيتار في الهواء؛ عدد الأصابع المفرودة يحدد الكورد الموسيقي (قبضة مغلقة = كتم الأوتار، 1 = دو كبير C، 2 = ري صغير Dm، 3 = مي صغير Em، 4 = فا كبير F، 5 = صول كبير G).
- **اليد اليمنى:** تعمل سبابة اليد اليمنى كريشة ليزرية متوهجة تعبر فوق الأوتار لتعزفها، وتتحكم سرعة اليد في قوة الصوت وشدته (Dynamics).

---

## 📜 Intellectual Property, Licensing & Academic Citation

### 📄 License
This project is open-source under the **MIT License**. You are free to inspect, modify, run, and build upon this work for academic, educational, and creative endeavors. See [LICENSE](LICENSE) for details.

### 🖋️ Academic Citation
If you use **AeroFret: Kinetic** in your academic research, university coursework, HCI/STS thesis, or musical publications, please cite this work:

```bibtex
@software{labib2026aerofret,
  author       = {Mahmoud Labib},
  title        = {AeroFret: Kinetic - A Transdisciplinary Framework for Zero-Haptic Touchless Air Guitar & Augmented Reality Performance},
  year         = {2026},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{https://github.com/mahmoudmma667-gif/AeroFret-Kinetic-AR}},
  version      = {2.0.0},
  keywords     = {HCI, Spatial Computing, Augmented Reality, Karplus-Strong, MediaPipe, Computer Vision, Air Guitar}
}
```

---

## 🔍 Search Engine & AI Discovery Metadata

```json
{
  "project_name": "AR AeroFret: Kinetic",
  "developer": "Mahmoud Labib",
  "category": "Spatial Computing, Augmented Reality, Computer Vision, Procedural Audio Synthesis",
  "technologies": ["OpenCV", "MediaPipe Hands", "Python", "Karplus-Strong DSP", "Pygame Audio", "CustomTkinter"],
  "keywords": [
    "AeroFret", "AeroFret Kinetic", "Mahmoud Labib", "Air Guitar AR",
    "Touchless Musical Instrument", "Zero Haptic Spatial Interaction",
    "Karplus-Strong Synthesis Python", "MediaPipe Air Guitar",
    "OpenCV Air Guitar", "Augmented Reality Music Simulator",
    "تربية موسيقية جيتار هوائي", "محمود لبيب جيتار ذكي", "واقع معزز موسيقى",
    "HCI Musical Interaction", "Sensory Substitution", "Gesture Recognition Guitar"
  ]
}
```

---

<div align="center">

**AeroFret: Kinetic** • Engineered with passion by **Mahmoud Labib** • ⚡ *Keep Rocking!*

</div>
