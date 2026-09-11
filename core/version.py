"""
AeroFret: Kinetic - Version & Research Metadata
Single source of truth for project versioning, developer credits, and academic metadata.
"""

__app_name__ = "AeroFret: Kinetic"
__version__ = "2.0.0"
__edition__ = "Extreme Velocity & Spatial HCI Studio Edition"
__author__ = "Mahmoud Labib"
__author_title__ = "Transdisciplinary Researcher at the Nexus of HCI • HCT • HCC • STS"
__license__ = "MIT with Academic Attribution"
__status__ = "Production"
__release_date__ = "2026-09-11"

def get_version_info() -> str:
    return f"{__app_name__} v{__version__} ({__edition__}) — Engineered by {__author__}"
