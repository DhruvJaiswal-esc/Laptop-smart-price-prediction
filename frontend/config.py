from pathlib import Path
import os

# =====================================================
# PROJECT INFO
# =====================================================

PROJECT_NAME = "Laptop Price Checker"
PROJECT_TITLE = "Laptop Price Checker"
PROJECT_TAGLINE = "Smart pricing, clear answers."
PAGE_TITLE = "Laptop Price Checker"
PAGE_ICON = "◈"
LAYOUT = "wide"

# =====================================================
# API
# =====================================================

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
PREDICTION_ENDPOINT = f"{API_BASE_URL}/prediction"
RECOMMENDATION_ENDPOINT = f"{API_BASE_URL}/recommendation"
EXPLAINABILITY_ENDPOINT = f"{API_BASE_URL}/explainability"
REQUEST_TIMEOUT = 120
VERIFY_SSL = False

# =====================================================
# DIRECTORIES
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
STYLE_DIR = BASE_DIR / "styles"
CSS_PATH = STYLE_DIR / "style.css"

# =====================================================
# THEME — Clean dark, one accent color
# No gradients. No glow. No rainbow.
# =====================================================

PRIMARY_COLOR = "#FF7849"          # coral — the one accent
PRIMARY_COLOR_BRIGHT = "#FF8E63"
PRIMARY_COLOR_DIM = "#E6633A"

SECONDARY_COLOR = "#ECECF1"        # off-white
TERTIARY_COLOR = "#9A9AAB"

SUCCESS_COLOR = "#4ADE80"
WARNING_COLOR = "#FBBF24"
ERROR_COLOR = "#F87171"

BACKGROUND_COLOR = "#0A0A0E"
SURFACE_COLOR = "#FFFFFF"
SURFACE_RAISED = "#F8FAFF"

TEXT_COLOR = "#ECECF1"
TEXT_MUTED = "#9A9AAB"
TEXT_FAINT = "#5C5C6E"

BORDER_COLOR = "#1A1A24"
RULE_COLOR = "#16161E"

# =====================================================
# TYPOGRAPHY
# =====================================================

FONT_MONO = "'JetBrains Mono', 'Courier New', monospace"
FONT_SANS = "'Inter', 'Segoe UI', sans-serif"
FONT_HEADING = "'Sora', 'Segoe UI', sans-serif"
FONT_DISPLAY = "'Sora', 'Segoe UI', sans-serif"

# =====================================================
# CHART COLORS
# =====================================================

POSITIVE_COLOR = "#4ADE80"
NEGATIVE_COLOR = "#F87171"
NEUTRAL_COLOR = "#FF7849"
GRID_COLOR = "#16161E"

# =====================================================
# SESSION STATE DEFAULTS
# =====================================================

SESSION_DEFAULTS = {
    "prediction_id": None,
    "prediction": None,
    "recommendations": None,
    "explainability": None,
    "prediction_complete": False,
    "laptop_information": None,
    "api_connected": False,
    "current_page": "home",
}

# =====================================================
# FORM OPTIONS
# =====================================================

RAM_TYPES = ["DDR4", "DDR5", "LPDDR4X", "LPDDR5", "LPDDR5X"]
SSD_TYPES = ["M.2 NVMe", "SATA"]
BATTERY_TYPES = ["Li-Ion", "Li-Polymer"]
WARRANTY_OPTIONS = [1, 2, 3]
WIFI_OPTIONS = ["Wi-Fi 5", "Wi-Fi 6", "Wi-Fi 6E", "Wi-Fi 7"]
BLUETOOTH_OPTIONS = ["5.0", "5.1", "5.2", "5.3", "5.4", "6.0"]

# =====================================================
# LOADING MESSAGES
# =====================================================

SPINNER_PREDICTION = "Working out a price…"
SPINNER_RECOMMENDATION = "Looking for similar laptops…"
SPINNER_EXPLAINABILITY = "Breaking down what shaped this price…"

# =====================================================
# PAGE CONFIG
# =====================================================

PAGE_CONFIG = {
    "page_title": PAGE_TITLE,
    "page_icon": PAGE_ICON,
    "layout": LAYOUT,
    "initial_sidebar_state": "expanded",
}
