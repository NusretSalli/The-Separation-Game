"""
Configuration constants for The Separation Game.
"""

# Application metadata
APP_TITLE = "The Separation Game ⚽"
APP_ICON = "⚽"
APP_TAGLINE = "Discover how football players are connected through their teammates!"

# Data file paths
PLAYER_PROFILES_PATH = "data/player_profiles.csv"
PLAYER_TEAMMATES_PATH = "data/player_teammates_played_with.csv"

# Difficulty settings for Quiz Mode
DIFFICULTY_SETTINGS = {
    "Easy": {
        "emoji": "🟢",
        "description": "2-3 degrees, popular players",
        "min_degrees": 2,
        "max_degrees": 3,
        "min_teammates": 50,  # More connected = more famous
    },
    "Medium": {
        "emoji": "🟡",
        "description": "3-4 degrees, mixed fame",
        "min_degrees": 3,
        "max_degrees": 4,
        "min_teammates": 20,
    },
    "Hard": {
        "emoji": "🔴",
        "description": "4-5 degrees, obscure players",
        "min_degrees": 4,
        "max_degrees": 5,
        "min_teammates": 5,
    },
}

# Quiz settings
MAX_QUIZ_ATTEMPTS = 100
MIN_ELIGIBLE_PLAYERS = 100
MAX_HINT_LEVELS = 5

# Theme configurations
DEFAULT_THEME = "dark"  # Default to dark theme

THEMES = {
    "light": {
        "name": "Light",
        "icon": "☀️",
        "bg_primary": "#ffffff",
        "bg_secondary": "#f8fafc",
        "bg_tertiary": "#f1f5f9",
        "text_primary": "#1a202c",
        "text_secondary": "#4a5568",
        "text_muted": "#718096",
        "border": "#e2e8f0",
        "accent": "#667eea",
        "accent_dark": "#764ba2",
        "success": "#10b981",
        "warning": "#fbbf24",
        "error": "#ef4444",
        "card_shadow": "rgba(0, 0, 0, 0.08)",
    },
    "dark": {
        "name": "Dark",
        "icon": "🌙",
        "bg_primary": "#0f172a",
        "bg_secondary": "#1e293b",
        "bg_tertiary": "#334155",
        "text_primary": "#f1f5f9",
        "text_secondary": "#cbd5e1",
        "text_muted": "#94a3b8",
        "border": "#475569",
        "accent": "#818cf8",
        "accent_dark": "#a78bfa",
        "success": "#34d399",
        "warning": "#fbbf24",
        "error": "#f87171",
        "card_shadow": "rgba(0, 0, 0, 0.3)",
    },
}

DEFAULT_THEME = "light"
