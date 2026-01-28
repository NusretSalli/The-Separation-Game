"""
The Separation Game - Main Application Entry Point

A "Six Degrees of Separation" style game for football players.
Find connections between any two players through their shared teammates.
"""

import streamlit as st

from src.config import APP_TITLE, APP_ICON, DIFFICULTY_SETTINGS
from src.data.loader import load_data
from src.game.explorer import render_explorer_mode
from src.game.quiz import (
    initialize_quiz_state,
    start_new_quiz,
    build_hint_text,
    check_guess,
    reveal_answer,
    complete_quiz,
)
from src.ui.styles import inject_styles
from src.ui.components import (
    render_header,
    render_footer,
    render_nav_bar,
    render_score_display,
    render_quiz_header,
    render_quiz_players,
    render_hint_box,
    render_success_message,
    render_error_message,
)


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)


def render_quiz_mode(
    display_names: list,
    display_to_id: dict,
    id_to_display: dict,
    player_id_to_name: dict,
    teammate_graph: dict,
    teammate_stats: dict,
    player_details: dict,
) -> None:
    """Render the Quiz Mode UI."""

    initialize_quiz_state()

    # Difficulty selector (only show when quiz is not active)
    if not st.session_state.quiz_active:
        st.markdown(
            """
            <div class="game-card">
                <h3 style="margin-top: 0;">⚙️ Select Difficulty</h3>
                <p style="color: #666;">Choose your challenge level before starting.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        difficulty_options = list(DIFFICULTY_SETTINGS.keys())
        difficulty_labels = [
            f"{DIFFICULTY_SETTINGS[d]['emoji']} {d} - {DIFFICULTY_SETTINGS[d]['description']}"
            for d in difficulty_options
        ]

        selected_idx = difficulty_options.index(st.session_state.quiz_difficulty)

        selected_label = st.radio(
            "Difficulty:",
            options=difficulty_labels,
            index=selected_idx,
            horizontal=True,
            label_visibility="collapsed",
        )

        st.session_state.quiz_difficulty = selected_label.split(" ")[1]

    # Score display
    if st.session_state.quiz_total > 0:
        render_score_display(st.session_state.quiz_score, st.session_state.quiz_total)

    # Start new quiz button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        difficulty = st.session_state.quiz_difficulty
        difficulty_emoji = DIFFICULTY_SETTINGS[difficulty]["emoji"]
        button_label = (
            f"🎲 New {difficulty_emoji} {difficulty} Challenge"
            if not st.session_state.quiz_active
            else "🎲 New Quiz Challenge"
        )

        if st.button(button_label, type="primary", use_container_width=True):
            if start_new_quiz(display_names, display_to_id, teammate_graph, difficulty):
                st.rerun()
            else:
                st.error(
                    f"Couldn't find a suitable {difficulty} quiz. Try again or change difficulty!"
                )

    # Active quiz display
    if st.session_state.quiz_active and st.session_state.quiz_path:
        path = st.session_state.quiz_path
        degrees = len(path) - 1

        difficulty = st.session_state.quiz_difficulty
        difficulty_emoji = DIFFICULTY_SETTINGS[difficulty]["emoji"]

        render_quiz_header(difficulty, difficulty_emoji, degrees - 1)
        render_quiz_players(
            player_id_to_name.get(path[0], "Unknown"),
            player_id_to_name.get(path[-1], "Unknown"),
        )

        st.markdown("---")
        st.markdown("### 🔗 Connection Chain")

        # Render the chain
        all_guessed = True
        for i, player_id in enumerate(path):
            player_name = player_id_to_name.get(player_id, str(player_id))

            if st.session_state.quiz_guessed[i]:
                icon = "⚽" if i == 0 or i == len(path) - 1 else "✅"
                st.markdown(
                    f'<div class="player-node">{icon} <strong>{i + 1}.</strong> {player_name}</div>',
                    unsafe_allow_html=True,
                )
            else:
                all_guessed = False
                st.markdown(
                    f'<div class="player-node" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left-color: #f59e0b;">❓ <strong>{i + 1}.</strong> ???</div>',
                    unsafe_allow_html=True,
                )

            if i < len(path) - 1:
                st.markdown('<div class="arrow">⬇️</div>', unsafe_allow_html=True)

        # Guess input
        if not all_guessed:
            st.markdown("### 🎯 Make Your Guess")

            next_to_guess = next(
                i
                for i, guessed in enumerate(st.session_state.quiz_guessed)
                if not guessed
            )

            st.info(f"Guess player #{next_to_guess + 1} in the chain")

            guess = st.selectbox(
                "Your guess:",
                options=display_names,
                index=None,
                placeholder="🔍 Type player name...",
                key=f"quiz_guess_{next_to_guess}",
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("✅ Submit Guess", use_container_width=True):
                    if guess:
                        guessed_id = display_to_id.get(guess)
                        correct_id = path[next_to_guess]

                        if check_guess(guessed_id, correct_id, next_to_guess):
                            st.balloons()
                            st.rerun()
                        else:
                            render_error_message("❌ Wrong! Try again or use a hint.")

            with col2:
                if st.button("💡 Get Hint", use_container_width=True):
                    correct_id = path[next_to_guess]
                    current_level = st.session_state.quiz_hint_level.get(
                        next_to_guess, 0
                    )

                    st.session_state.quiz_hint_level[next_to_guess] = current_level + 1
                    st.session_state.quiz_hints_used += 1

                    hint_header, hint_text = build_hint_text(
                        correct_id, player_id_to_name, player_details, current_level
                    )
                    render_hint_box(hint_header, hint_text)

            with col3:
                if st.button("🏳️ Show Answer", use_container_width=True):
                    reveal_answer(next_to_guess)
                    st.rerun()
        else:
            render_success_message(
                "🎉 Congratulations! You found the complete connection!"
            )
            complete_quiz()


def main():
    """Main application entry point."""

    # Inject styles
    inject_styles()

    # Load data
    with st.spinner("🔄 Loading player database..."):
        (
            display_names,
            display_to_id,
            id_to_display,
            player_id_to_name,
            teammate_graph,
            teammate_stats,
            player_details,
        ) = load_data()

    # Render header with stats
    render_header(display_names, teammate_graph)

    # Navigation bar (mode selector + theme toggle)
    mode = render_nav_bar()

    # Render selected mode
    if mode == "🔍 Explorer Mode":
        render_explorer_mode(
            display_names,
            display_to_id,
            player_id_to_name,
            teammate_graph,
            teammate_stats,
        )
    else:
        render_quiz_mode(
            display_names,
            display_to_id,
            id_to_display,
            player_id_to_name,
            teammate_graph,
            teammate_stats,
            player_details,
        )

    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
