from pathlib import Path

# =====================================================
# PROJECT INFORMATION
# =====================================================

PROJECT_NAME = "Laptop Price Checker"

PROJECT_SHORT_NAME = "Price Checker"

PROJECT_TITLE = "Laptop Price Checker"

PROJECT_TAGLINE = "A clear, no-nonsense way to price a laptop."

PAGE_TITLE = "Laptop Price Checker"

PAGE_ICON = "◈"

LAYOUT = "wide"

INITIAL_SIDEBAR_STATE = "expanded"


# =====================================================
# API
# =====================================================

import os

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

PREDICTION_ENDPOINT = f"{API_BASE_URL}/prediction"

RECOMMENDATION_ENDPOINT = f"{API_BASE_URL}/recommendation"

EXPLAINABILITY_ENDPOINT = f"{API_BASE_URL}/explainability"


# =====================================================
# REQUEST SETTINGS
# =====================================================

REQUEST_TIMEOUT = 120

VERIFY_SSL = False


# =====================================================
# DIRECTORIES
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

STYLE_DIR = BASE_DIR / "styles"

LOGO_PATH = ASSETS_DIR / "logo.png"

BACKGROUND_PATH = ASSETS_DIR / "background.png"

CSS_PATH = STYLE_DIR / "style.css"


# # =====================================================
# # THEME
# # Graphite terminal palette. Copper reads as "value" (price,
# # positive signal, primary action). Cold cyan reads as
# # "comparison / secondary read". This is a ticker convention,
# # not one brand color reused for everything.
# # =====================================================

# PRIMARY_COLOR = "#C97C3D"       # copper - value, price, primary CTAs
# PRIMARY_COLOR_BRIGHT = "#E0954F"
# PRIMARY_COLOR_DIM = "#8A5A2E"   # muted copper for borders/hover states

# SECONDARY_COLOR = "#4FA6B0"     # cold cyan - comparison / secondary accent
# SECONDARY_COLOR_DIM = "#356870"

# SUCCESS_COLOR = "#5FA88A"       # desaturated sage
# WARNING_COLOR = "#C9A227"
# ERROR_COLOR = "#B85450"         # muted brick red

# BACKGROUND_COLOR = "#0A0C0E"    # near-black graphite
# SURFACE_COLOR = "#111417"       # panel background, one step up from bg
# SURFACE_RAISED = "#161A1E"      # elevated panel (hover / active)
# CARD_COLOR = "#15181C"

# TEXT_COLOR = "#EDEAE4"          # warm off-white
# TEXT_MUTED = "#8A8F98"
# TEXT_FAINT = "#5A5F66"

# BORDER_COLOR = "#2A2E33"
# RULE_COLOR = "#1D2024"          # hairline dividers
# =====================================================
# THEME
# Clean light mode palette: White backgrounds, crisp black text,
# and sharp red as the primary action/accent color.
# =====================================================

PRIMARY_COLOR = "#D92323"       # Sharp Red - value, price, primary CTAs
PRIMARY_COLOR_BRIGHT = "#EF4444"
PRIMARY_COLOR_DIM = "#991B1B"   

SECONDARY_COLOR = "#111827"     # Stark Black - comparison / secondary accent
SECONDARY_COLOR_DIM = "#374151"

SUCCESS_COLOR = "#111827"       # Black for neutral success states
WARNING_COLOR = "#F59E0B"
ERROR_COLOR = "#D92323"         # Sharp Red

BACKGROUND_COLOR = "#FFFFFF"    # Pure White
SURFACE_COLOR = "#F9FAFB"       # Very light gray for panels
SURFACE_RAISED = "#FFFFFF"      
CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#111827"          # Almost black
TEXT_MUTED = "#4B5563"          # Medium gray
TEXT_FAINT = "#9CA3AF"          # Light gray

BORDER_COLOR = "#E5E7EB"        # Soft gray borders
RULE_COLOR = "#F3F4F6"          # Hairline dividers

# =====================================================
# CHART COLORS
# =====================================================

POSITIVE_COLOR = "#111827"      # Black (Pushed price up)
NEGATIVE_COLOR = "#D92323"      # Red (Pushed price down)
NEUTRAL_COLOR = "#9CA3AF"       # Light Gray
GRID_COLOR = "#F3F4F6"


# =====================================================
# TYPOGRAPHY
# =====================================================

FONT_MONO = "'Space Mono', 'Courier New', monospace"
FONT_SANS = "'Archivo', 'Segoe UI', sans-serif"
FONT_HEADING = "'Fraunces', 'Georgia', serif"
FONT_DISPLAY = "'Space Grotesk', 'Segoe UI', sans-serif"


# =====================================================
# CHART COLORS
# =====================================================

POSITIVE_COLOR = "#5FA88A"
NEGATIVE_COLOR = "#B85450"
NEUTRAL_COLOR = "#C97C3D"
GRID_COLOR = "#1D2024"


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
}


# =====================================================
# FORM OPTIONS
# =====================================================

RAM_TYPES = ["DDR4", "DDR5", "LPDDR4X", "LPDDR5", "LPDDR5X"]

SSD_TYPES = ["M.2 NVMe", "SATA"]

BATTERY_TYPES = ["Li-Ion", "Li-Polymer"]

WARRANTY_OPTIONS = [1, 2, 3]

WIFI_OPTIONS = ["Wi-Fi 5", "Wi-Fi 6", "Wi-Fi 6E", "Wi-Fi 7"]

BLUETOOTH_OPTIONS = ["5.0", "5.1", "5.2", "5.3", "5.4","6.0"]


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
    "initial_sidebar_state": INITIAL_SIDEBAR_STATE,
}
