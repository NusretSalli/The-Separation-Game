"""
Reusable UI components for The Separation Game.
Enhanced with modern styling and theme support.
"""

from typing import Dict, Set

import streamlit as st

from ..config import APP_TITLE, APP_TAGLINE, THEMES, DEFAULT_THEME


def get_current_theme_name() -> str:
    """Get the current theme name from session state."""
    if "theme" not in st.session_state:
        st.session_state.theme = DEFAULT_THEME
    return st.session_state.theme


def render_theme_toggle() -> None:
    """Render a theme toggle button."""
    current = get_current_theme_name()
    theme_config = THEMES[current]
    next_theme = "light" if current == "dark" else "dark"
    next_icon = THEMES[next_theme]["icon"]
    
    if st.button(f"{next_icon}", key="theme_toggle", help=f"Switch to {next_theme} mode"):
        st.session_state.theme = next_theme
        st.rerun()


def render_header(
    display_names: list = None, teammate_graph: Dict[int, Set[int]] = None
) -> None:
    """Render the hero header with optional stats."""
    stats_html = ""
    if display_names and teammate_graph:
        player_count = len(display_names)
        connection_count = sum(len(v) for v in teammate_graph.values()) // 2
        stats_html = f"""
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">{player_count:,}</div>
                <div class="hero-stat-label">Players</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{connection_count:,}</div>
                <div class="hero-stat-label">Connections</div>
            </div>
        </div>
        """

    st.markdown(
        f"""
        <div class="hero-header">
            <h1>{APP_TITLE}</h1>
            <p>{APP_TAGLINE}</p>
            {stats_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_nav_bar() -> str:
    """Render the navigation bar with mode selector and theme toggle. Returns selected mode."""
    col1, col2 = st.columns([6, 1])
    
    with col2:
        render_theme_toggle()
    
    # Mode selector tabs
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "explorer"
    
    col1, col2 = st.columns(2)
    
    with col1:
        explorer_active = st.session_state.game_mode == "explorer"
        btn_class = "primary" if explorer_active else "secondary"
        if st.button("🔍 Explorer", key="nav_explorer", use_container_width=True, type=btn_class):
            st.session_state.game_mode = "explorer"
            st.rerun()
    
    with col2:
        quiz_active = st.session_state.game_mode == "quiz"
        btn_class = "primary" if quiz_active else "secondary"
        if st.button("🧩 Quiz", key="nav_quiz", use_container_width=True, type=btn_class):
            st.session_state.game_mode = "quiz"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    return "🔍 Explorer Mode" if st.session_state.game_mode == "explorer" else "🧩 Quiz Mode"


def render_footer() -> None:
    """Render the application footer."""
    st.markdown(
        """
        <div class="footer">
            Built with ❤️ using Streamlit | Data from Transfermarkt<br>
            <small>Discover the hidden connections in the world of football</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_box(display_names: list, teammate_graph: Dict[int, Set[int]]) -> None:
    """Render the stats box showing player and connection counts."""
    player_count = len(display_names)
    connection_count = sum(len(v) for v in teammate_graph.values()) // 2

    st.markdown(
        f"""
        <div class="stats-box">
            📊 <strong>{player_count:,}</strong> players • 
            <strong>{connection_count:,}</strong> connections
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mode_selector() -> str:
    """Render the game mode selector and return the selected mode."""
    mode = st.radio(
        "Choose Game Mode:",
        options=["🔍 Explorer Mode", "🧩 Quiz Mode"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("---")
    return mode


def render_game_card(icon: str, title: str, description: str) -> None:
    """Render a game feature card."""
    st.markdown(
        f"""
        <div class="game-card">
            <div class="card-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_player_node(
    index: int, player_name: str, is_endpoint: bool = False, is_mystery: bool = False
) -> None:
    """Render a single player node in the connection chain."""
    if is_mystery:
        st.markdown(
            f'<div class="player-node player-node-mystery">❓ <strong>{index}.</strong> ???</div>',
            unsafe_allow_html=True,
        )
    else:
        icon = "⚽" if is_endpoint else "✅"
        st.markdown(
            f'<div class="player-node">{icon} <strong>{index}.</strong> {player_name}</div>',
            unsafe_allow_html=True,
        )


def render_arrow(show_stats: bool = False, stats_text: str = "") -> None:
    """Render an arrow connector between players."""
    if show_stats and stats_text:
        st.markdown(
            f'<div class="arrow">⬇️ <em>played with</em><small>📊 {stats_text}</small></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="arrow">⬇️</div>',
            unsafe_allow_html=True,
        )


def render_connection_result(degree: int, path_length: int) -> None:
    """Render the connection result card."""
    st.markdown(
        f"""
        <div class="connection-card">
            <h2>🎯 Connection Found!</h2>
            <div class="degree-badge">{degree} Degrees of Separation</div>
            <p style="margin-top: 1rem; opacity: 0.9;">{path_length} players in the chain</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success_message(message: str) -> None:
    """Render a success message box."""
    st.markdown(
        f'<div class="success-guess">✅ {message}</div>',
        unsafe_allow_html=True,
    )


def render_error_message(message: str) -> None:
    """Render an error message box."""
    st.markdown(
        f'<div class="wrong-guess">❌ {message}</div>',
        unsafe_allow_html=True,
    )


def render_hint_box(header: str, content: str) -> None:
    """Render a hint box with header and content."""
    st.markdown(
        f'<div class="hint-box">💡 <strong>{header}</strong><br><br>{content}</div>',
        unsafe_allow_html=True,
    )


def render_score_display(score: int, total: int) -> None:
    """Render the score display."""
    percentage = (score / total * 100) if total > 0 else 0
    st.markdown(
        f"""
        <div class="score-display">
            🏆 Score: {score} / {total} correct ({percentage:.0f}%)
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz_header(
    difficulty: str, difficulty_emoji: str, players_to_guess: int
) -> None:
    """Render the quiz challenge header."""
    plural = "s" if players_to_guess > 1 else ""
    st.markdown(
        f"""
        <div class="quiz-header">
            <h3>🧩 Quiz Challenge {difficulty_emoji}</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.95;">
                Difficulty: <strong>{difficulty}</strong>
            </p>
            <p style="margin: 0.75rem 0 0 0;">
                Find the {players_to_guess} player{plural} connecting these two!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz_players(player1_name: str, player2_name: str) -> None:
    """Render the two endpoint players in quiz mode."""
    col1, col2, col3 = st.columns([5, 1, 5])

    with col1:
        st.markdown(
            f'<div class="quiz-player-card">⚽ {player1_name}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown('<div class="quiz-vs">↔️</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(
            f'<div class="quiz-player-card">⚽ {player2_name}</div>',
            unsafe_allow_html=True,
        )


def render_difficulty_selector(current_difficulty: str) -> str:
    """Render difficulty selector cards. Returns selected difficulty."""
    from ..config import DIFFICULTY_SETTINGS
    
    st.markdown("### Select Difficulty")
    
    cols = st.columns(3)
    selected = current_difficulty
    
    for idx, (name, settings) in enumerate(DIFFICULTY_SETTINGS.items()):
        with cols[idx]:
            is_active = name == current_difficulty
            card_class = "difficulty-card difficulty-card-active" if is_active else "difficulty-card"
            
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="difficulty-emoji">{settings['emoji']}</div>
                    <div class="difficulty-name">{name}</div>
                    <div class="difficulty-desc">{settings['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            if st.button(f"Select {name}", key=f"diff_{name}", use_container_width=True):
                selected = name
    
    return selected


def render_progress_bar(current: int, total: int) -> None:
    """Render a progress indicator for quiz guessing."""
    filled = "🟢" * current
    empty = "⚪" * (total - current)
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 1.25rem; margin: 0.5rem 0;">
            {filled}{empty} ({current}/{total} found)
        </div>
        """,
        unsafe_allow_html=True,
    )
