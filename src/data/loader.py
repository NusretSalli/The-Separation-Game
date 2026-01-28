"""
Data loading and graph building module.
"""

import re
from datetime import datetime
from collections import defaultdict
from typing import Tuple, Dict, Set, List, Any

import pandas as pd
import streamlit as st

from ..config import PLAYER_PROFILES_PATH, PLAYER_TEAMMATES_PATH


def _clean_player_name(name: str) -> str:
    """Remove trailing disambiguation numbers from player names."""
    if pd.isna(name):
        return name
    cleaned = re.sub(r"\s*\(\d+\)$", "", str(name))
    return cleaned.strip()


def _calculate_age(dob: Any, current_year: int) -> int | None:
    """Calculate age from date of birth string."""
    if pd.isna(dob):
        return None
    try:
        birth_year = int(str(dob)[:4])
        return current_year - birth_year
    except (ValueError, TypeError):
        return None


def _get_safe_value(row: pd.Series, key: str, default: str = "Unknown") -> str:
    """Safely get a value from a row with fallback."""
    value = row.get(key, default)
    return default if pd.isna(value) else value


@st.cache_data(show_spinner=False)
def load_data() -> Tuple[
    List[str],
    Dict[str, int],
    Dict[int, str],
    Dict[int, str],
    Dict[int, Set[int]],
    Dict[Tuple[int, int], Dict[str, Any]],
    Dict[int, Dict[str, Any]],
]:
    """
    Load player data and build the teammate graph.

    Returns:
        Tuple containing:
        - display_names: Sorted list of player display names
        - display_to_id: Mapping from display name to player ID
        - id_to_display: Mapping from player ID to display name
        - player_id_to_name: Mapping from player ID to clean name
        - teammate_graph: Adjacency list of teammate connections
        - teammate_stats: Stats for each teammate pair
        - player_details: Detailed player info for hints
    """
    df_players = pd.read_csv(PLAYER_PROFILES_PATH, low_memory=False)
    df_teammates = pd.read_csv(PLAYER_TEAMMATES_PATH)

    df_players = df_players.dropna(subset=["player_name"])
    df_players["clean_name"] = df_players["player_name"].apply(_clean_player_name)

    player_id_to_name = df_players.set_index("player_id")["clean_name"].to_dict()
    current_year = datetime.now().year

    display_names = []
    display_to_id = {}
    id_to_display = {}
    player_details = {}

    for _, row in df_players.iterrows():
        player_id = row["player_id"]
        player_name = row["clean_name"]

        if pd.isna(player_name):
            continue

        dob = row.get("date_of_birth", None)
        age = _calculate_age(dob, current_year)
        age_str = f", {age} yrs" if age else ""

        club = _get_safe_value(row, "current_club_name")
        display_name = f"{player_name} ({club}{age_str})"

        display_names.append(display_name)
        display_to_id[display_name] = player_id
        id_to_display[player_id] = display_name

        # Store player details for hints
        player_details[player_id] = {
            "name": player_name,
            "club": club,
            "nationality": _get_safe_value(row, "citizenship"),
            "position": _get_safe_value(row, "position"),
            "country_of_birth": _get_safe_value(row, "country_of_birth"),
            "age": age,
        }

    display_names = sorted(
        [name for name in set(display_names) if isinstance(name, str)]
    )

    # Build teammate graph
    teammate_graph = defaultdict(set)
    teammate_stats = {}

    for _, row in df_teammates.iterrows():
        player_id = row["player_id"]
        teammate_id = row["teammate_player_id"]

        teammate_graph[player_id].add(teammate_id)
        teammate_graph[teammate_id].add(player_id)

        minutes = row.get("minutes_played_with", None)
        goals = row.get("joint_goal_participation", None)
        stats = {"minutes": minutes, "goals": goals}

        teammate_stats[(player_id, teammate_id)] = stats
        teammate_stats[(teammate_id, player_id)] = stats

    return (
        display_names,
        display_to_id,
        id_to_display,
        player_id_to_name,
        dict(teammate_graph),
        teammate_stats,
        player_details,
    )
