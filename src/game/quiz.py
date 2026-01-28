"""
Quiz mode game logic.
"""

import random
from typing import Dict, Set, List, Tuple, Any

import streamlit as st

from ..config import (
    DIFFICULTY_SETTINGS,
    MAX_QUIZ_ATTEMPTS,
    MIN_ELIGIBLE_PLAYERS,
    MAX_HINT_LEVELS,
)
from .pathfinder import find_separation_path


def get_random_quiz_players(
    display_names: List[str],
    display_to_id: Dict[str, int],
    teammate_graph: Dict[int, Set[int]],
    difficulty: str = "Medium",
) -> Tuple[str | None, str | None, List[int] | None]:
    """
    Get two random players that have a valid connection based on difficulty.

    Args:
        display_names: List of player display names
        display_to_id: Mapping from display name to player ID
        teammate_graph: Adjacency list of teammate connections
        difficulty: Difficulty level (Easy, Medium, Hard)

    Returns:
        Tuple of (player1_display, player2_display, path) or (None, None, None)
    """
    settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Medium"])
    min_degrees = settings["min_degrees"]
    max_degrees = settings["max_degrees"]
    min_teammates = settings["min_teammates"]

    # Filter players by connection count (popularity proxy)
    eligible_players = [
        display_name
        for display_name in display_names
        if (player_id := display_to_id.get(display_name))
        and len(teammate_graph.get(player_id, [])) >= min_teammates
    ]

    # Fallback to all players if filter is too strict
    if len(eligible_players) < MIN_ELIGIBLE_PLAYERS:
        eligible_players = display_names

    for _ in range(MAX_QUIZ_ATTEMPTS):
        player1_display = random.choice(eligible_players)
        player2_display = random.choice(eligible_players)

        if player1_display == player2_display:
            continue

        player1_id = display_to_id.get(player1_display)
        player2_id = display_to_id.get(player2_display)

        if player1_id and player2_id:
            path = find_separation_path(player1_id, player2_id, teammate_graph)
            if path and min_degrees <= len(path) - 1 <= max_degrees:
                return player1_display, player2_display, path

    return None, None, None


def initialize_quiz_state() -> None:
    """Initialize all quiz-related session state variables."""
    defaults = {
        "quiz_active": False,
        "quiz_score": 0,
        "quiz_total": 0,
        "quiz_path": None,
        "quiz_guessed": [],
        "quiz_hints_used": 0,
        "quiz_hint_level": {},
        "quiz_player1": None,
        "quiz_player2": None,
        "quiz_difficulty": "Medium",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def start_new_quiz(
    display_names: List[str],
    display_to_id: Dict[str, int],
    teammate_graph: Dict[int, Set[int]],
    difficulty: str,
) -> bool:
    """
    Start a new quiz challenge.

    Returns:
        True if quiz was successfully started, False otherwise
    """
    player1, player2, path = get_random_quiz_players(
        display_names, display_to_id, teammate_graph, difficulty
    )

    if not path:
        return False

    st.session_state.quiz_active = True
    st.session_state.quiz_player1 = player1
    st.session_state.quiz_player2 = player2
    st.session_state.quiz_path = path
    st.session_state.quiz_guessed = [True] + [False] * (len(path) - 2) + [True]
    st.session_state.quiz_hints_used = 0
    st.session_state.quiz_hint_level = {}

    return True


def build_hint_text(
    player_id: int,
    player_id_to_name: Dict[int, str],
    player_details: Dict[int, Dict[str, Any]],
    hint_level: int,
) -> Tuple[str, str]:
    """
    Build progressive hint text based on current level.

    Returns:
        Tuple of (hint_header, hint_text)
    """
    correct_name = player_id_to_name.get(player_id, "Unknown")
    details = player_details.get(player_id, {})

    hints = []

    # Level 1: First letter + name length (always shown)
    hints.append(
        f"📝 First letter: **{correct_name[0]}**, Name length: **{len(correct_name)}** characters"
    )

    # Level 2: Nationality
    if hint_level >= 1:
        nationality = details.get("nationality", "Unknown")
        hints.append(f"🌍 Nationality: **{nationality}**")

    # Level 3: Current club
    if hint_level >= 2:
        club = details.get("club", "Unknown")
        hints.append(f"🏟️ Current Club: **{club}**")

    # Level 4: Position
    if hint_level >= 3:
        position = details.get("position", "Unknown")
        hints.append(f"⚽ Position: **{position}**")

    # Level 5: Age
    if hint_level >= 4:
        age = details.get("age")
        hints.append(f"🎂 Age: **{age}** years old" if age else "🎂 Age: **Unknown**")

    hint_text = "<br>".join(hints)
    remaining = max(0, MAX_HINT_LEVELS - (hint_level + 1))

    hint_header = f"💡 Hint {hint_level + 1}/{MAX_HINT_LEVELS}"
    if remaining > 0:
        hint_header += f" ({remaining} more available)"
    else:
        hint_header += " (all hints revealed!)"

    return hint_header, hint_text


def check_guess(guess_id: int, correct_id: int, position: int) -> bool:
    """
    Check if a guess is correct and update state accordingly.

    Returns:
        True if guess is correct, False otherwise
    """
    if guess_id == correct_id:
        st.session_state.quiz_guessed[position] = True
        st.session_state.quiz_score += 1
        return True
    return False


def reveal_answer(position: int) -> None:
    """Reveal the answer at a given position."""
    st.session_state.quiz_guessed[position] = True
    st.session_state.quiz_total += 1


def complete_quiz() -> None:
    """Mark the quiz as completed."""
    st.session_state.quiz_total += 1
    st.session_state.quiz_active = False
