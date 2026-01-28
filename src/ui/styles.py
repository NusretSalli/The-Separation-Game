"""
CSS styles for The Separation Game.
Enhanced with theme support, responsive design, and modern aesthetics.
"""

import streamlit as st
from ..config import THEMES, DEFAULT_THEME


def get_current_theme() -> dict:
    """Get the current theme configuration."""
    if "theme" not in st.session_state:
        st.session_state.theme = DEFAULT_THEME
    return THEMES.get(st.session_state.theme, THEMES[DEFAULT_THEME])


def toggle_theme() -> None:
    """Toggle between light and dark themes."""
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"


def inject_styles() -> None:
    """Inject all CSS styles into the Streamlit app."""
    theme = get_current_theme()
    st.markdown(get_theme_styles(theme), unsafe_allow_html=True)


def get_theme_styles(theme: dict) -> str:
    """Return the complete CSS stylesheet with theme variables."""
    return f"""
<style>
    /* ========================================
       CSS VARIABLES (Theme-based)
       ======================================== */
    
    :root {{
        --bg-primary: {theme['bg_primary']};
        --bg-secondary: {theme['bg_secondary']};
        --bg-tertiary: {theme['bg_tertiary']};
        --text-primary: {theme['text_primary']};
        --text-secondary: {theme['text_secondary']};
        --text-muted: {theme['text_muted']};
        --border-color: {theme['border']};
        --accent: {theme['accent']};
        --accent-dark: {theme['accent_dark']};
        --success: {theme['success']};
        --warning: {theme['warning']};
        --error: {theme['error']};
        --card-shadow: {theme['card_shadow']};
    }}

    /* ========================================
       RESET & BASE STYLES
       ======================================== */
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Smooth scrolling & transitions */
    html {{
        scroll-behavior: smooth;
    }}
    
    * {{
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }}
    
    /* Override Streamlit background */
    .stApp {{
        background-color: var(--bg-primary) !important;
    }}
    
    .stApp > div {{
        background-color: var(--bg-primary) !important;
    }}

    /* ========================================
       LAYOUT & CONTAINER
       ======================================== */
    
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 920px;
        background-color: var(--bg-primary);
    }}
    
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}

    /* ========================================
       NAVIGATION BAR
       ======================================== */
    
    .nav-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.5rem;
        background: var(--bg-secondary);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 8px var(--card-shadow);
    }}
    
    .nav-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .nav-actions {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .theme-toggle {{
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 1.1rem;
        transition: all 0.2s ease;
        color: var(--text-primary);
    }}
    
    .theme-toggle:hover {{
        background: var(--accent);
        color: white;
        border-color: var(--accent);
    }}

    /* ========================================
       HERO HEADER
       ======================================== */
    
    .hero-header {{
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }}
    
    .hero-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }}
    
    .hero-header h1 {{
        color: #ffffff;
        font-size: 2.75rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}
    
    .hero-header p {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.15rem;
        margin-top: 0.75rem;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }}
    
    .hero-stats {{
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.5rem;
        position: relative;
        z-index: 1;
    }}
    
    .hero-stat {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .hero-stat-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }}
    
    .hero-stat-label {{
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.8);
    }}
    
    @media (max-width: 768px) {{
        .hero-header h1 {{
            font-size: 2rem;
        }}
        .hero-header p {{
            font-size: 1rem;
        }}
        .hero-stats {{
            flex-direction: column;
            gap: 0.75rem;
        }}
    }}

    /* ========================================
       MODE TABS (Navigation)
       ======================================== */
    
    .mode-tabs {{
        display: flex;
        gap: 0.5rem;
        background: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }}
    
    .mode-tab {{
        flex: 1;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-decoration: none;
    }}
    
    .mode-tab-inactive {{
        background: transparent;
        color: var(--text-muted);
    }}
    
    .mode-tab-inactive:hover {{
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }}
    
    .mode-tab-active {{
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }}

    /* ========================================
       CARD STYLES
       ======================================== */
    
    .game-card {{
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px var(--card-shadow);
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .game-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px var(--card-shadow);
    }}
    
    .game-card h3 {{
        color: var(--text-primary);
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }}
    
    .game-card p {{
        color: var(--text-muted);
        margin: 0;
        line-height: 1.5;
    }}
    
    .card-icon {{
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }}

    /* ========================================
       CONNECTION RESULT CARD
       ======================================== */
    
    .connection-card {{
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.35);
        position: relative;
        overflow: hidden;
    }}
    
    .connection-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    }}
    
    .connection-card h2 {{
        margin: 0 0 1rem 0;
        font-size: 1.75rem;
        position: relative;
        z-index: 1;
        font-weight: 700;
    }}

    /* ========================================
       PLAYER NODE STYLES
       ======================================== */
    
    .player-node {{
        background: var(--bg-secondary);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border-left: 4px solid var(--accent);
        margin: 0.5rem 0;
        font-weight: 500;
        font-size: 1rem;
        color: var(--text-primary);
        box-shadow: 0 2px 8px var(--card-shadow);
        transition: all 0.2s ease;
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--accent);
    }}
    
    .player-node:hover {{
        border-left-color: var(--accent-dark);
        transform: translateX(4px);
        box-shadow: 0 4px 12px var(--card-shadow);
    }}
    
    .player-node-mystery {{
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left-color: #f59e0b;
        color: #92400e;
    }}

    /* ========================================
       ARROW CONNECTOR
       ======================================== */
    
    .arrow {{
        text-align: center;
        color: var(--accent);
        font-size: 1.1rem;
        margin: 0.75rem 0;
        line-height: 1.5;
    }}
    
    .arrow em {{
        color: var(--text-muted);
        font-size: 0.9rem;
    }}
    
    .arrow small {{
        display: block;
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }}

    /* ========================================
       DEGREE BADGE
       ======================================== */
    
    .degree-badge {{
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.75rem;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.1rem;
        display: inline-block;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4);
    }}

    /* ========================================
       QUIZ MODE STYLES
       ======================================== */
    
    .quiz-header {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(245, 87, 108, 0.3);
    }}
    
    .quiz-header h3 {{
        margin: 0;
        font-size: 1.5rem;
        font-weight: 700;
    }}
    
    .quiz-header p {{
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }}
    
    .quiz-player-card {{
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem 1rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    .quiz-player-card:hover {{
        transform: scale(1.02);
    }}
    
    @media (max-width: 768px) {{
        .quiz-player-card {{
            font-size: 0.9rem;
            padding: 1rem 0.75rem;
        }}
    }}
    
    .quiz-vs {{
        text-align: center;
        font-size: 2rem;
        color: var(--accent);
        font-weight: bold;
        padding: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* ========================================
       DIFFICULTY SELECTOR
       ======================================== */
    
    .difficulty-cards {{
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .difficulty-card {{
        flex: 1;
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px solid var(--border-color);
        background: var(--bg-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
    }}
    
    .difficulty-card:hover {{
        border-color: var(--accent);
        transform: translateY(-2px);
    }}
    
    .difficulty-card-active {{
        border-color: var(--accent);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }}
    
    .difficulty-emoji {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}
    
    .difficulty-name {{
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }}
    
    .difficulty-desc {{
        font-size: 0.85rem;
        color: var(--text-muted);
    }}

    /* ========================================
       SCORE & FEEDBACK STYLES
       ======================================== */
    
    .score-display {{
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem 2rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 600;
        color: #744210;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(252, 182, 159, 0.4);
    }}
    
    .hint-box {{
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 2px solid var(--warning);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        line-height: 1.8;
        color: #92400e;
    }}
    
    .hint-box strong {{
        color: #78350f;
    }}
    
    .success-guess {{
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid var(--success);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: #065f46;
        font-weight: 600;
        font-size: 1.1rem;
    }}
    
    .wrong-guess {{
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid var(--error);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: #991b1b;
        font-weight: 500;
    }}

    /* ========================================
       STATS BOX
       ======================================== */
    
    .stats-box {{
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        margin: 1rem 0;
        font-size: 1rem;
        color: var(--text-secondary);
    }}
    
    .stats-box strong {{
        color: var(--accent);
    }}

    /* ========================================
       BUTTON STYLES
       ======================================== */
    
    .stButton > button {{
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        border: none !important;
        font-size: 0.95rem !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%) !important;
        color: white !important;
    }}
    
    .stButton > button[kind="secondary"] {{
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }}

    /* ========================================
       FORM ELEMENTS
       ======================================== */
    
    .stSelectbox > div > div {{
        border-radius: 12px !important;
        border-color: var(--border-color) !important;
        background: var(--bg-secondary) !important;
    }}
    
    .stSelectbox label {{
        color: var(--text-primary) !important;
    }}
    
    .stRadio > div {{
        background: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }}
    
    .stRadio label {{
        color: var(--text-primary) !important;
    }}

    /* ========================================
       FOOTER STYLES
       ======================================== */
    
    .footer {{
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }}
    
    .footer a {{
        color: var(--accent);
        text-decoration: none;
    }}
    
    .footer a:hover {{
        text-decoration: underline;
    }}

    /* ========================================
       RESPONSIVE ADJUSTMENTS
       ======================================== */
    
    @media (max-width: 480px) {{
        .hero-header {{
            padding: 2rem 1rem;
        }}
        
        .game-card {{
            padding: 1rem;
        }}
        
        .connection-card {{
            padding: 1.5rem 1rem;
        }}
        
        .quiz-header {{
            padding: 1.5rem 1rem;
        }}
        
        .degree-badge {{
            padding: 0.5rem 1.25rem;
            font-size: 1rem;
        }}
        
        .stButton > button {{
            padding: 0.6rem 1.5rem !important;
        }}
        
        .difficulty-cards {{
            flex-direction: column;
        }}
    }}

    /* ========================================
       ANIMATIONS
       ======================================== */
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .game-card, .connection-card, .quiz-header {{
        animation: fadeIn 0.3s ease-out;
    }}
    
    .player-node {{
        animation: slideIn 0.3s ease-out;
    }}

    /* ========================================
       SCROLLBAR STYLING
       ======================================== */
    
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-secondary);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--text-muted);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--text-secondary);
    }}
</style>
"""
