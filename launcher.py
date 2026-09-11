"""
AeroFret: Kinetic - Control Center & GUI Launcher
Studio-Grade AAA Cyberpunk Game Launcher built with CustomTkinter.
Engineered & Developed by Mahmoud Labib.

Provides rich system controls (10+ interactive parameters):
- Camera Source Selector
- Game Mode (Free-Play vs Guitar Hero)
- Dynamic Rhythm BPM Tempo (60-200 BPM)
- String Count Configuration (3, 4, 5, 6 strings)
- Master Amp Power & Overdrive Level (10%-100%)
- MediaPipe Hand Tracking Sensitivity & Confidence
- Physical Pick Debounce Lockout (50-250ms)
- Auto-Borderless Fullscreen Toggle
- Virtual Stage Mode (Camera-Hide) Toggle
- Real-Time Procedural Tone Synthesizer Test
- Developer Credits & Architecture Info Modal
- 1-Click Instant Engine Launch
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.terminal_banner import print_cyberpunk_banner
from core.audio_synth import AudioEngine
from main import AeroFretApp


class AeroFretLauncher(ctk.CTk):
    """Futuristic Cyberpunk Game Launcher & Configuration Suite for AeroFret: Kinetic."""

    def __init__(self):
        super().__init__()

        self.title("AeroFret: Kinetic — Studio Control Center")
        self.geometry("800x600")
        self.minsize(720, 480)

        # Set custom electric guitar icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'app_icon.ico')
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        print_cyberpunk_banner("Control Center & Studio Launcher Active")

        self.audio_engine = AudioEngine()
        self._build_ui()

    def _build_ui(self):
        # 1. Header Banner (Docked Top - Compact 56px)
        header_frame = ctk.CTkFrame(self, fg_color="#0D111A", corner_radius=10, border_width=1, border_color="#232B3E")
        header_frame.pack(side="top", fill="x", padx=14, pady=(8, 3))

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="🎸 AEROFRET : KINETIC",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#00E5FF"
        )
        title_lbl.pack(pady=(6, 0))

        subtitle_lbl = ctk.CTkLabel(
            header_frame,
            text="PRO TOUCHLESS AIR GUITAR & AUGMENTED REALITY RHYTHM SIMULATOR",
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            text_color="#8F9BB3"
        )
        subtitle_lbl.pack(pady=(0, 1))

        author_lbl = ctk.CTkLabel(
            header_frame,
            text="Created & Engineered by Mahmoud Labib  •  Transdisciplinary HCI / STS Researcher  •  60 FPS",
            font=ctk.CTkFont(family="Segoe UI", size=9),
            text_color="#00FFAA"
        )
        author_lbl.pack(pady=(0, 6))

        # 2. Fixed Docked Bottom Bar (Always 100% visible on any screen resolution/DPI scaling)
        bottom_frame = ctk.CTkFrame(self, fg_color="#0D111A", corner_radius=10, border_width=1, border_color="#232B3E")
        bottom_frame.pack(side="bottom", fill="x", padx=14, pady=(3, 8))

        action_row = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        action_row.pack(fill="x", padx=10, pady=(6, 4))

        credits_btn = ctk.CTkButton(
            action_row,
            text="ℹ️ About & Research (HCI/STS)",
            width=190,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#182030",
            hover_color="#00FFAA",
            text_color="#00FFAA",
            command=self.show_credits
        )
        credits_btn.pack(side="left")

        reset_btn = ctk.CTkButton(
            action_row,
            text="🔄 Reset Presets",
            width=110,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#182030",
            hover_color="#F43F5E",
            text_color="#E2E8F0",
            command=self.reset_presets
        )
        reset_btn.pack(side="left", padx=8)

        tip_lbl = ctk.CTkLabel(
            action_row,
            text="⚡ Sub-8ms Audio  |  Continuous Swept-Line Physics",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#64748B"
        )
        tip_lbl.pack(side="right", padx=6)

        # Big Glowing Launch Button (Always docked, always in view)
        self.launch_btn = ctk.CTkButton(
            bottom_frame,
            text="▶️   START GAME (LAUNCH AEROFRET KINETIC)   🎸",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="#00E5FF",
            text_color="#090D16",
            hover_color="#33EFFF",
            height=42,
            corner_radius=8,
            command=self.launch_game
        )
        self.launch_btn.pack(fill="x", padx=10, pady=(0, 6))

        # 3. Main Scrollable Container for Controls (Takes all available remaining space)
        content_frame = ctk.CTkScrollableFrame(self, fg_color="#131722", corner_radius=10, border_width=1, border_color="#212838")
        content_frame.pack(side="top", fill="both", expand=True, padx=14, pady=3)

        # ====== SECTION A: Core Video & Gameplay ======
        sec_a_lbl = ctk.CTkLabel(
            content_frame,
            text="⚡ CORE SYSTEM & DISPLAY MODES",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00E5FF"
        )
        sec_a_lbl.pack(anchor="w", padx=16, pady=(12, 6))

        sec_a_card = ctk.CTkFrame(content_frame, fg_color="#181D2B", corner_radius=10)
        sec_a_card.pack(fill="x", padx=12, pady=(0, 12))

        # Camera Source
        r0 = ctk.CTkFrame(sec_a_card, fg_color="transparent")
        r0.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r0, text="📹 Camera Source:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.cam_combo = ctk.CTkComboBox(
            r0,
            values=["Camera 0 (Default Integrated)", "Camera 1 (External USB)", "Camera 2 (Secondary)"],
            width=260,
            fg_color="#232838",
            button_color="#00E5FF"
        )
        self.cam_combo.set("Camera 0 (Default Integrated)")
        self.cam_combo.pack(side="right")

        # Starting Game Mode
        r1 = ctk.CTkFrame(sec_a_card, fg_color="transparent")
        r1.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r1, text="🎮 Starting Game Mode:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.mode_combo = ctk.CTkComboBox(
            r1,
            values=["Free-Play Air Guitar", "Guitar Hero (Rhythm Beat-Match)"],
            width=260,
            fg_color="#232838",
            button_color="#FF007F"
        )
        self.mode_combo.set("Free-Play Air Guitar")
        self.mode_combo.pack(side="right")

        # Display Toggles (Auto Fullscreen & Virtual Stage)
        r2 = ctk.CTkFrame(sec_a_card, fg_color="transparent")
        r2.pack(fill="x", padx=16, pady=(8, 12))
        self.fullscreen_var = ctk.BooleanVar(value=True)
        self.fullscreen_switch = ctk.CTkSwitch(
            r2,
            text="Auto-Borderless Fullscreen (Hide Titlebar)",
            variable=self.fullscreen_var,
            font=ctk.CTkFont(size=12),
            text_color="#E0E5FF",
            progress_color="#00E5FF"
        )
        self.fullscreen_switch.pack(side="left")

        self.stage_var = ctk.BooleanVar(value=False)
        self.stage_switch = ctk.CTkSwitch(
            r2,
            text="Virtual Stage Mode (Hide Camera)",
            variable=self.stage_var,
            font=ctk.CTkFont(size=12),
            text_color="#E0E5FF",
            progress_color="#FF007F"
        )
        self.stage_switch.pack(side="right")

        # ====== SECTION B: Acoustic & Rhythm Configuration ======
        sec_b_lbl = ctk.CTkLabel(
            content_frame,
            text="🎛️ ACOUSTIC & RHYTHM CONTROLS",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00FFAA"
        )
        sec_b_lbl.pack(anchor="w", padx=16, pady=(8, 6))

        sec_b_card = ctk.CTkFrame(content_frame, fg_color="#181D2B", corner_radius=10)
        sec_b_card.pack(fill="x", padx=12, pady=(0, 12))

        # Amp Overdrive / Power Level Slider
        r_amp = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_amp.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r_amp, text="🔊 Amp Power / Gain:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.amp_val_lbl = ctk.CTkLabel(r_amp, text="85%", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00E5FF", width=45)
        self.amp_val_lbl.pack(side="right")
        self.amp_slider = ctk.CTkSlider(
            r_amp,
            from_=0.10,
            to=1.00,
            number_of_steps=18,
            width=200,
            progress_color="#00E5FF",
            command=self._on_amp_slider
        )
        self.amp_slider.set(0.85)
        self.amp_slider.pack(side="right", padx=10)

        # Rhythm BPM Slider
        r_bpm = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_bpm.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r_bpm, text="⏱️ Rhythm Tempo (BPM):", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.bpm_val_lbl = ctk.CTkLabel(r_bpm, text="105 BPM", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FFB300", width=65)
        self.bpm_val_lbl.pack(side="right")
        self.bpm_slider = ctk.CTkSlider(
            r_bpm,
            from_=60,
            to=200,
            number_of_steps=28,
            width=200,
            progress_color="#FFB300",
            command=self._on_bpm_slider
        )
        self.bpm_slider.set(105)
        self.bpm_slider.pack(side="right", padx=10)

        # String Count Selection
        r_str = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_str.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r_str, text="🎸 Guitar String Count:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.str_combo = ctk.CTkComboBox(
            r_str,
            values=["4 Strings (Standard)", "3 Strings (Beginner)", "5 Strings (Extended)", "6 Strings (Full Electric)"],
            width=260,
            fg_color="#232838",
            button_color="#00FFAA"
        )
        self.str_combo.set("4 Strings (Standard)")
        self.str_combo.pack(side="right")

        # Tone & Sonic Style Model
        r_tone = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_tone.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r_tone, text="⚡ Electric Guitar Tone:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.tone_combo = ctk.CTkComboBox(
            r_tone,
            values=[
                "Heavy Metal Overdrive (Max Crunch)",
                "Rock & Blues Crunch (Warm Tube)",
                "Clean Stratocaster (Acoustic Sparkle)",
                "Synthwave Cyberpunk (Detuned Analog)"
            ],
            width=260,
            fg_color="#232838",
            button_color="#FFB300",
            command=self._on_tone_change
        )
        self.tone_combo.set("Heavy Metal Overdrive (Max Crunch)")
        self.tone_combo.pack(side="right")

        # Visual FX & Atmosphere Toggles
        r_fx = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_fx.pack(fill="x", padx=16, pady=(6, 6))
        self.pyro_var = ctk.BooleanVar(value=True)
        self.pyro_switch = ctk.CTkSwitch(
            r_fx,
            text="Stage Flame Cannons (مضخة النار)",
            variable=self.pyro_var,
            font=ctk.CTkFont(size=11),
            text_color="#E0E5FF",
            progress_color="#FF4500"
        )
        self.pyro_switch.pack(side="left")

        self.notes_var = ctk.BooleanVar(value=True)
        self.notes_switch = ctk.CTkSwitch(
            r_fx,
            text="Floating Musical Notes (نوتات طافية)",
            variable=self.notes_var,
            font=ctk.CTkFont(size=11),
            text_color="#E0E5FF",
            progress_color="#00FFAA"
        )
        self.notes_switch.pack(side="right")

        r_vib = ctk.CTkFrame(sec_b_card, fg_color="transparent")
        r_vib.pack(fill="x", padx=16, pady=(4, 12))
        self.vibrato_var = ctk.BooleanVar(value=True)
        self.vibrato_switch = ctk.CTkSwitch(
            r_vib,
            text="String Wave Vibrato & Ripple (شد المعزوفة والتموج)",
            variable=self.vibrato_var,
            font=ctk.CTkFont(size=11),
            text_color="#E0E5FF",
            progress_color="#00E5FF",
            command=self._on_vibrato_change
        )
        self.vibrato_switch.pack(side="left")

        # ====== SECTION C: Spatial Vision & Tracking Engine ======
        sec_c_lbl = ctk.CTkLabel(
            content_frame,
            text="👁️ COMPUTER VISION & GESTURE SENSITIVITY",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FF007F"
        )
        sec_c_lbl.pack(anchor="w", padx=16, pady=(8, 6))

        sec_c_card = ctk.CTkFrame(content_frame, fg_color="#181D2B", corner_radius=10)
        sec_c_card.pack(fill="x", padx=12, pady=(0, 12))

        # MediaPipe Tracking Confidence
        r_conf = ctk.CTkFrame(sec_c_card, fg_color="transparent")
        r_conf.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(r_conf, text="🎯 Tracking Confidence:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.conf_val_lbl = ctk.CTkLabel(r_conf, text="0.65", font=ctk.CTkFont(size=12, weight="bold"), text_color="#FF007F", width=45)
        self.conf_val_lbl.pack(side="right")
        self.conf_slider = ctk.CTkSlider(
            r_conf,
            from_=0.40,
            to=0.90,
            number_of_steps=10,
            width=200,
            progress_color="#FF007F",
            command=self._on_conf_slider
        )
        self.conf_slider.set(0.65)
        self.conf_slider.pack(side="right", padx=10)

        # Pick Strum Debounce Lockout (ms)
        r_deb = ctk.CTkFrame(sec_c_card, fg_color="transparent")
        r_deb.pack(fill="x", padx=16, pady=(8, 8))
        ctk.CTkLabel(r_deb, text="⚡ Strum Debounce Lockout:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.deb_val_lbl = ctk.CTkLabel(r_deb, text="120 ms", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00E5FF", width=55)
        self.deb_val_lbl.pack(side="right")
        self.deb_slider = ctk.CTkSlider(
            r_deb,
            from_=50,
            to=250,
            number_of_steps=20,
            width=200,
            progress_color="#00E5FF",
            command=self._on_deb_slider
        )
        self.deb_slider.set(120)
        self.deb_slider.pack(side="right", padx=10)

        # Performance Play Style (Hybrid, Solo Precision, Full Strum)
        r_style = ctk.CTkFrame(sec_c_card, fg_color="transparent")
        r_style.pack(fill="x", padx=16, pady=(4, 8))
        ctk.CTkLabel(r_style, text="🎸 Performance Play Style:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.style_combo = ctk.CTkComboBox(
            r_style,
            values=["Dynamic Hybrid (Solo + Strum)", "Solo Precision (Melodic Shredding)", "Full Strum (Chord Sweeps)"],
            width=220,
            state="readonly",
            fg_color="#101420",
            button_color="#FF007F"
        )
        self.style_combo.set("Dynamic Hybrid (Solo + Strum)")
        self.style_combo.pack(side="right")

        # Vision Latency Profile
        r_lat = ctk.CTkFrame(sec_c_card, fg_color="transparent")
        r_lat.pack(fill="x", padx=16, pady=(4, 12))
        ctk.CTkLabel(r_lat, text="⚡ Vision Latency Profile:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#E0E5FF").pack(side="left")
        self.latency_combo = ctk.CTkComboBox(
            r_lat,
            values=["⚡ Zero Latency 60 FPS (Fastest Response)", "Balanced Studio (Default)", "Cinematic Smooth (Ultra Stable)"],
            width=220,
            state="readonly",
            fg_color="#101420",
            button_color="#00E5FF",
            command=self._on_latency_profile
        )
        self.latency_combo.set("⚡ Zero Latency 60 FPS (Fastest Response)")
        self.latency_combo.pack(side="right")

        # ====== SECTION D: Procedural Tone Audition ======
        sec_d_lbl = ctk.CTkLabel(
            content_frame,
            text="🔊 PROCEDURAL AUDIO ENGINE AUDITION",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFB300"
        )
        sec_d_lbl.pack(anchor="w", padx=16, pady=(8, 6))

        sec_d_card = ctk.CTkFrame(content_frame, fg_color="#181D2B", corner_radius=10)
        sec_d_card.pack(fill="x", padx=12, pady=(0, 12))

        chords_box = ctk.CTkFrame(sec_d_card, fg_color="transparent")
        chords_box.pack(pady=10)

        chords = [
            ("C Major", "C", "#00E5FF"),
            ("D Minor", "Dm", "#3B82F6"),
            ("E Minor", "Em", "#10B981"),
            ("F Major", "F", "#F59E0B"),
            ("G Major", "G", "#EC4899"),
            ("Palm Mute", "MUTE", "#64748B")
        ]
        for name, chord, col in chords:
            btn = ctk.CTkButton(
                chords_box,
                text=name,
                width=88,
                height=32,
                fg_color="#242B3D",
                hover_color=col,
                text_color="#F1F5F9",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda c=chord: self.audio_engine.play_chord(c, self.amp_slider.get())
            )
            btn.pack(side="left", padx=4)

        # ====== Quick Play Instructions Card ======
        guide_frame = ctk.CTkFrame(content_frame, fg_color="#101420", corner_radius=10, border_width=1, border_color="#1F283D")
        guide_frame.pack(fill="x", padx=12, pady=(4, 12))

        guide_text = (
            "🎸 LEFT HAND (FRETTING) : Grip the guitar neck in air (Fist=Mute | 1 Finger=C | 2=Dm | 3=Em | 4=F | 5=G)\n"
            "🎯 RIGHT HAND (PICKING) : Index finger is your Plectrum! Pluck any string individually or sweep across to strum.\n"
            "⌨️ HOTKEYS              : [F] Fullscreen Borderless | [C] Virtual Stage | [M] Guitar Hero | [P] Power | [Q] Quit"
        )
        guide_lbl = ctk.CTkLabel(
            guide_frame,
            text=guide_text,
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
            justify="left"
        )
        guide_lbl.pack(padx=16, pady=10)

        # 3. Bottom Bar is docked at window bottom (defined in _build_ui header)

    def _on_amp_slider(self, val):
        self.amp_val_lbl.configure(text=f"{int(val * 100)}%")

    def _on_bpm_slider(self, val):
        self.bpm_val_lbl.configure(text=f"{int(val)} BPM")

    def _on_conf_slider(self, val):
        self.conf_val_lbl.configure(text=f"{val:.2f}")

    def _on_deb_slider(self, val):
        self.deb_val_lbl.configure(text=f"{int(val)} ms")

    def _on_latency_profile(self, choice):
        """Auto-configures vision confidence and debouncing based on selected latency profile."""
        if "Zero Latency" in choice:
            self.conf_slider.set(0.50)
            self.conf_val_lbl.configure(text="0.50")
            self.deb_slider.set(80)
            self.deb_val_lbl.configure(text="80 ms")
        elif "Balanced" in choice:
            self.conf_slider.set(0.65)
            self.conf_val_lbl.configure(text="0.65")
            self.deb_slider.set(120)
            self.deb_val_lbl.configure(text="120 ms")
        elif "Cinematic" in choice:
            self.conf_slider.set(0.75)
            self.conf_val_lbl.configure(text="0.75")
            self.deb_slider.set(150)
            self.deb_val_lbl.configure(text="150 ms")

    def _on_tone_change(self, choice):
        norm = 'overdrive'
        if 'Crunch' in choice:
            norm = 'crunch'
        elif 'Clean' in choice:
            norm = 'clean'
        elif 'Synthwave' in choice:
            norm = 'synthwave'
        self.audio_engine.set_preset(norm, enable_vibrato=self.vibrato_var.get())

    def _on_vibrato_change(self):
        self.audio_engine.enable_vibrato = self.vibrato_var.get()
        self.audio_engine._precompute_chords()

    def reset_presets(self):
        """Restores optimal studio default parameters."""
        self.cam_combo.set("Camera 0 (Default Integrated)")
        self.mode_combo.set("Free-Play Air Guitar")
        self.fullscreen_var.set(True)
        self.stage_var.set(False)
        self.amp_slider.set(0.85)
        self.amp_val_lbl.configure(text="85%")
        self.bpm_slider.set(105)
        self.bpm_val_lbl.configure(text="105 BPM")
        self.str_combo.set("4 Strings (Standard)")
        self.tone_combo.set("Heavy Metal Overdrive (Max Crunch)")
        self.style_combo.set("Dynamic Hybrid (Solo + Strum)")
        self.latency_combo.set("⚡ Zero Latency 60 FPS (Fastest Response)")
        self.pyro_var.set(True)
        self.notes_var.set(True)
        self.vibrato_var.set(True)
        self.audio_engine.set_preset('overdrive', enable_vibrato=True)
        self.conf_slider.set(0.65)
        self.conf_val_lbl.configure(text="0.65")
        self.deb_slider.set(120)
        self.deb_val_lbl.configure(text="120 ms")

    def show_credits(self):
        """Displays project documentation and credits modal highlighting researcher Mahmoud Labib's background in HCI, HCT, HCC & STS."""
        about_win = ctk.CTkToplevel(self)
        about_win.title("AeroFret: Kinetic — Transdisciplinary Research & Architecture")
        about_win.geometry("680x580")
        about_win.minsize(620, 500)
        about_win.attributes("-topmost", True)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'app_icon.ico')
        if os.path.exists(icon_path):
            try:
                about_win.iconbitmap(icon_path)
            except Exception:
                pass

        c_frame = ctk.CTkScrollableFrame(about_win, fg_color="#0D111A", corner_radius=12, border_width=1, border_color="#232B3E")
        c_frame.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            c_frame,
            text="🎸 AEROFRET : KINETIC",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#00E5FF"
        ).pack(pady=(12, 2))

        ctk.CTkLabel(
            c_frame,
            text="Architect & Principal Investigator: Mahmoud Labib",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00FFAA"
        ).pack(pady=(0, 2))

        ctk.CTkLabel(
            c_frame,
            text="Transdisciplinary Researcher at the Nexus of HCI • HCT • HCC • STS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#94A3B8"
        ).pack(pady=(0, 14))

        # Academic Pillars Card
        pillars_frame = ctk.CTkFrame(c_frame, fg_color="#141926", corner_radius=10, border_width=1, border_color="#232B3E")
        pillars_frame.pack(fill="x", padx=10, pady=(0, 12))

        pillars_text = (
            "🏛️ TRANSDISCIPLINARY RESEARCH EPISTEMOLOGY\n\n"
            "• HCI (Human-Computer Interaction):\n"
            "  Pioneers Touchless Spatial Interaction and 'Zero-Haptic Sensorimotor Substitution'.\n"
            "  By coupling sub-8ms auditory response with synchronized visual shockwaves and chromatic\n"
            "  micro-flashes, the user's sensorimotor cortex perceives an embodied proprioceptive\n"
            "  illusion of physical resistance where no physical strings exist.\n\n"
            "• HCT (Human-Centered Technology):\n"
            "  Engineered around musculoskeletal biomechanics rather than forcing human anatomy\n"
            "  to conform to rigid peripherals. Hand pose kinematics mirror natural finger joint\n"
            "  degrees of freedom, carpal flexion, and radial/ulnar wrist deviation.\n\n"
            "• HCC (Human-Centered Computing):\n"
            "  Minimizes cognitive load via 'Natural Mapping' (Don Norman). Finger extension cardinality\n"
            "  directly controls harmonic triad complexity (1=C, 2=Dm, 3=Em, 4=F, 5=G, fist=mute),\n"
            "  bypassing the mental translation bottleneck and unlocking instantaneous motor flow.\n\n"
            "• STS (Science, Technology, and Society):\n"
            "  Democratizes musical expression by abolishing socio-economic barriers to entry.\n"
            "  Collapses thousands of dollars of hardware (instruments, pickups, amplifiers, pedals)\n"
            "  into pure dematerialized software running on commodity webcams and laptops."
        )
        ctk.CTkLabel(
            pillars_frame,
            text=pillars_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#E2E8F0",
            justify="left"
        ).pack(padx=16, pady=12)

        # Technical Architecture Card
        tech_frame = ctk.CTkFrame(c_frame, fg_color="#141926", corner_radius=10, border_width=1, border_color="#232B3E")
        tech_frame.pack(fill="x", padx=10, pady=(0, 12))

        tech_text = (
            "⚡ TECHNICAL ARCHITECTURE & SYSTEMS SPECIFICATIONS\n\n"
            "• Vision Pipeline: MediaPipe Hands BlazeHand + CLAHE adaptive contrast normalization.\n"
            "• Strum Physics: Continuous Swept-Line Collision Detection (Swept Ray Intersection)\n"
            "  guarantees 100% pluck detection during violent hand motions (>3000 px/s).\n"
            "• Tremolo Alternate Picking: Directional alternating debounce (38ms lockout on opposite\n"
            "  stroke directions) enables ultra-fast shredding up to 20 notes/sec without false triggers.\n"
            "• Audio Engine: Physical Karplus-Strong string synthesis with circular delay line buffers,\n"
            "  exponential decay, and dynamic velocity impact gain (<8ms end-to-end latency).\n"
            "• Visuals: Vectorized stage lighting, volumetric spotlights, ambient bokeh dust motes,\n"
            "  and photorealistic hand rendering with anatomical creases, shading, and nail beds."
        )
        ctk.CTkLabel(
            tech_frame,
            text=tech_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#CBD5E1",
            justify="left"
        ).pack(padx=16, pady=12)

        ctk.CTkButton(
            c_frame,
            text="Close",
            width=120,
            height=34,
            fg_color="#00E5FF",
            text_color="#0A0E18",
            hover_color="#33EFFF",
            command=about_win.destroy
        ).pack(pady=(4, 12))

    def launch_game(self):
        """Starts AeroFret with all user-configured parameters."""
        cam_text = self.cam_combo.get()
        cam_idx = 0
        if "1" in cam_text:
            cam_idx = 1
        elif "2" in cam_text:
            cam_idx = 2

        str_text = self.str_combo.get()
        num_strings = 4
        if "3" in str_text:
            num_strings = 3
        elif "5" in str_text:
            num_strings = 5
        elif "6" in str_text:
            num_strings = 6

        bpm = float(self.bpm_slider.get())
        amp_power = float(self.amp_slider.get())
        conf = float(self.conf_slider.get())
        deb_ms = float(self.deb_slider.get())
        start_fs = bool(self.fullscreen_var.get())
        stage_mode = bool(self.stage_var.get())
        init_mode = "rhythm" if "Guitar Hero" in self.mode_combo.get() else "free"

        tone_text = self.tone_combo.get()
        tone_key = 'overdrive'
        if 'Crunch' in tone_text:
            tone_key = 'crunch'
        elif 'Clean' in tone_text:
            tone_key = 'clean'
        elif 'Synthwave' in tone_text:
            tone_key = 'synthwave'

        # Play Style mapping
        style_text = self.style_combo.get()
        play_style = "hybrid"
        if "Solo" in style_text:
            play_style = "solo"
        elif "Full Strum" in style_text:
            play_style = "strum"

        enable_pyro = bool(self.pyro_var.get())
        enable_notes = bool(self.notes_var.get())
        enable_vibrato = bool(self.vibrato_var.get())

        self.launch_btn.configure(text="⏳ Initializing Vision & 60 FPS Audio Engine...", state="disabled")
        self.withdraw()

        def run_proc():
            try:
                app = AeroFretApp(
                    camera_index=cam_idx,
                    bpm=bpm,
                    num_strings=num_strings,
                    power_level=amp_power,
                    start_fullscreen=start_fs,
                    virtual_stage=stage_mode,
                    debounce_ms=deb_ms,
                    confidence=conf,
                    initial_mode=init_mode,
                    tone_preset=tone_key,
                    enable_pyro=enable_pyro,
                    enable_floating_notes=enable_notes,
                    enable_vibrato=enable_vibrato,
                    play_style=play_style
                )
                app.run()
            except Exception as e:
                print(f"[Launcher Error]: {e}")
            finally:
                self.after(0, self._on_game_close)

        threading.Thread(target=run_proc, daemon=True).start()

    def _on_game_close(self):
        self.deiconify()
        self.launch_btn.configure(text="▶️   START GAME (LAUNCH AEROFRET KINETIC)   🎸", state="normal")


if __name__ == '__main__':
    launcher = AeroFretLauncher()
    launcher.mainloop()
