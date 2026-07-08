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
# THEME — Glassmorphism over mesh gradient
# Indigo → Purple → Pink (harmonious, no clashing)
# =====================================================

PRIMARY_COLOR = "#A855F7"          # purple
PRIMARY_COLOR_BRIGHT = "#C084FC"
PRIMARY_COLOR_DIM = "#9333EA"

SECONDARY_COLOR = "#6366F1"        # indigo
SECONDARY_COLOR_DIM = "#4F46E5"

TERTIARY_COLOR = "#EC4899"         # pink
TERTIARY_COLOR_DIM = "#DB2777"

SUCCESS_COLOR = "#22C55E"
WARNING_COLOR = "#F59E0B"
ERROR_COLOR = "#EF4444"

BACKGROUND_COLOR = "#0D0D1A"
SURFACE_COLOR = "#FFFFFF"
SURFACE_RAISED = "#F8FAFF"

TEXT_COLOR = "#F1F5F9"
TEXT_MUTED = "#94A3B8"
TEXT_FAINT = "#64748B"

BORDER_COLOR = "#1E1E38"
RULE_COLOR = "#1E1E38"

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

POSITIVE_COLOR = "#22C55E"
NEGATIVE_COLOR = "#EF4444"
NEUTRAL_COLOR = "#A855F7"
GRID_COLOR = "#1E1E38"

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
