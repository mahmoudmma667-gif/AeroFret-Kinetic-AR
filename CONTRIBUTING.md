# 🤝 Contributing to AeroFret: Kinetic

Thank you for your interest in contributing to **AeroFret: Kinetic**!

This project is a transdisciplinary research initiative pioneered by **Mahmoud Labib** at the nexus of Human-Computer Interaction (HCI), Human-Centered Technology (HCT), Human-Centered Computing (HCC), and Science, Technology & Society (STS).

---

## 🛠️ Development Philosophy & Clean Code Standards

To preserve the architectural integrity of AeroFret:

1. **Sub-8ms Audio Latency is Non-Negotiable:**
   - Any modification to the audio synthesis pipeline must preserve low-latency execution (<8ms).
   - Avoid disk I/O, heavy memory allocations, or garbage collection triggers in the audio callback or frame loop.
2. **60 FPS Real-Time Spatial Tracking:**
   - The computer vision loop must execute within $\le 16.6\text{ms}$ per frame.
   - Use vectorized NumPy operations and pre-allocated memory buffers.
3. **Clean Code & Type Hints:**
   - Follow PEP 8 guidelines.
   - Add explicit Python type annotations (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Tuple`).
   - Maintain clear docstrings explaining mathematical models and kinematic rationales.
4. **Asset Organization:**
   - All image and graphic assets must reside exclusively inside the `assets/` directory.
   - Keep the project root directory clean.

---

## 🧪 Testing & Verification Workflow

Before submitting any Pull Request:

1. **Run the Diagnostic Doctor:**
   ```bash
   python tools/doctor.py
   ```
2. **Execute the Full Automated Test Suite:**
   ```bash
   python -m unittest discover tests
   ```
   *All 5 core tests (AudioEngine, English Chord Mapping, Dynamic Strumming, Extreme Velocity CCD, Photorealistic Rendering) must pass with 100% success.*

---

## 📬 Academic Collaboration & Inquiries

For academic partnerships, spatial computing workshops, or transdisciplinary research inquiries, please reach out to:
- **Principal Investigator:** Mahmoud Labib
- **Affiliation:** Transdisciplinary HCI / STS Research
