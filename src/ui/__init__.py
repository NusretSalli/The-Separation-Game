# UI components and styles module
from .styles import inject_styles, toggle_theme, get_current_theme
from .components import (
    render_header,
    render_footer,
    render_nav_bar,
    render_stats_box,
    render_theme_toggle,
)

__all__ = [
    "inject_styles",
    "toggle_theme",
    "get_current_theme",
    "render_header",
    "render_footer",
    "render_nav_bar",
    "render_stats_box",
    "render_theme_toggle",
]
