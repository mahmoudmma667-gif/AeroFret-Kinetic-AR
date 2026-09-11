"""
AeroFret: Kinetic - Terminal Experience & Cyberpunk Telemetry
Engineered by Mahmoud Labib.
Provides a studio-grade, vibrant console UI with ANSI styling,
ASCII art branding, telemetry diagnostics, and keyboard shortcuts guide.
"""

import os
import sys
import ctypes

# Suppress Pygame welcome message globally
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


def init_console_ansi():
    """Enables Windows 10/11 Virtual Terminal Processing for ANSI colors and sets UTF-8."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
            kernel32.SetConsoleCP(65001)

            STD_OUTPUT_HANDLE = -11
            hOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(hOut, ctypes.byref(mode)):
                ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                kernel32.SetConsoleMode(hOut, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        except Exception:
            pass


def print_cyberpunk_banner(title: str = "AeroFret: Kinetic - Engine Active"):
    """Prints a cyberpunk ASCII art banner and project dashboard to the console."""
    init_console_ansi()

    # ANSI Color definitions
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    banner = f"""
{CYAN}{BOLD}================================================================================
   █████╗ ███████╗██████╗  ██████╗ ███████╗██████╗ ███████╗████████╗
  ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝
  ███████║█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝█████╗     ██║   
  ██╔══██║██╔══╝  ██╔══██╗██║   ██║██╔══╝  ██╔══██╗██╔══╝     ██║   
  ██║  ██║███████╗██║  ██║╚██████╔╝██║     ██║  ██║███████╗   ██║   
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   
{MAGENTA}             ⚡  K I N E T I C   A I R   G U I T A R  ⚡{RESET}
{CYAN}================================================================================{RESET}
  {WHITE}{BOLD}Project:{RESET}       AeroFret: Kinetic (Studio v1.5.0)
  {WHITE}{BOLD}Status:{RESET}        {GREEN}● ONLINE{RESET} — {title}
  {WHITE}{BOLD}Audio Engine:{RESET}  <8ms Ultra-Low Latency Procedural Karplus-Strong Synthesizer
  {WHITE}{BOLD}Vision Core:{RESET}   60 FPS MediaPipe Hand Kinematics & Dual-Hand Spatial Anchoring
  {WHITE}{BOLD}Architect:{RESET}     {YELLOW}Created & Engineered by Mahmoud Labib{RESET}
{GRAY}--------------------------------------------------------------------------------{RESET}
  {WHITE}{BOLD}🎮 QUICK CONTROLS & SHORTCUT CHEAT SHEET:{RESET}
    {CYAN}[M]{RESET} Toggle Game Mode        : Free-Play <-> Guitar Hero Rhythm Mode
    {CYAN}[C]{RESET} Virtual Stage Mode      : Sleek Neon Studio & 3D Fleshy Organic Hands
    {CYAN}[F]{RESET} Fullscreen Mode         : True Win32 Borderless Fullscreen (WS_POPUP)
    {CYAN}[[] / []]{RESET} Amp Gain Control : Step Master Gain & Overdrive (-5% / +5%)
    {CYAN}[R]{RESET} Reset Score             : Clear Streak and Multiplier in Hero Mode
    {CYAN}[Q / ESC]{RESET} Exit Game         : Clean Engine Shutdown
    
  {WHITE}{BOLD}🖐️ FRET HAND CHORD MAPPINGS:{RESET}
    {YELLOW}Fist (0 Fingers){RESET}  -> {MAGENTA}PALM MUTE{RESET} (Acoustic harmonic dampening)
    {YELLOW}1 Finger (Index){RESET}  -> {CYAN}C MAJOR{RESET}
    {YELLOW}2 Fingers{RESET}         -> {CYAN}D MINOR{RESET}
    {YELLOW}3 Fingers{RESET}         -> {CYAN}E MINOR{RESET}
    {YELLOW}4 Fingers{RESET}         -> {CYAN}F MAJOR{RESET}
    {YELLOW}5 Fingers (Open){RESET}  -> {CYAN}G MAJOR{RESET}
{CYAN}================================================================================{RESET}
"""
    try:
        print(banner, flush=True)
    except Exception:
        # Fallback for plain environments
        print(f"=== AeroFret: Kinetic v1.5.0 - Engineered by Mahmoud Labib ===")
