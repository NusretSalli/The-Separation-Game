"""
Explorer mode game logic.
"""

from typing import Dict, Set, List, Any, Tuple

import streamlit as st
import pandas as pd

from .pathfinder import find_separation_path


def render_explorer_mode(
    display_names: List[str],
    display_to_id: Dict[str, int],
    player_id_to_name: Dict[int, str],
    teammate_graph: Dict[int, Set[int]],
    teammate_stats: Dict[Tuple[int, int], Dict[str, Any]],
) -> None:
    """Render the Explorer mode UI and handle user interactions."""

    st.markdown(
        """
        <div class="game-card">
            <h3 style="margin-top: 0;">🎯 Select Two Players</h3>
            <p style="color: #666;">Choose any two football players to discover how they're connected through teammates.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox(
            "First Player",
            options=display_names,
            index=None,
            placeholder="🔍 Type to search...",
            key="explorer_player1",
        )

    with col2:
        player2 = st.selectbox(
            "Second Player",
            options=display_names,
            index=None,
            placeholder="🔍 Type to search...",
            key="explorer_player2",
        )

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        find_button = st.button(
            "🔍 Find Connection", type="primary", use_container_width=True
        )

    if find_button:
        _handle_find_connection(
            player1,
            player2,
            display_to_id,
            player_id_to_name,
            teammate_graph,
            teammate_stats,
        )


def _handle_find_connection(
    player1: str | None,
    player2: str | None,
    display_to_id: Dict[str, int],
    player_id_to_name: Dict[int, str],
    teammate_graph: Dict[int, Set[int]],
    teammate_stats: Dict[Tuple[int, int], Dict[str, Any]],
) -> None:
    """Handle the find connection button click."""

    if not player1 or not player2:
        st.warning("⚠️ Please select both players!")
        return

    if player1 == player2:
        st.info("🤔 That's the same player! Select two different players.")
        return

    start_id = display_to_id.get(player1)
    end_id = display_to_id.get(player2)

    if start_id is None or end_id is None:
        st.error("❌ Could not find one or both players.")
        return

    with st.spinner("🔍 Searching for connection..."):
        path = find_separation_path(start_id, end_id, teammate_graph)

    if path:
        display_path_result(path, player_id_to_name, teammate_stats)
    else:
        st.error("❌ No connection found between these players!")


def display_path_result(
    path: List[int],
    player_id_to_name: Dict[int, str],
    teammate_stats: Dict[Tuple[int, int], Dict[str, Any]],
) -> None:
    """Display the connection path in a visually appealing way."""
    degrees = len(path) - 1

    st.markdown(
        f"""
        <div class="connection-card">
            <h2>✅ Connection Found!</h2>
            <div class="degree-badge">{degrees} degree{"s" if degrees != 1 else ""} of separation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔗 Connection Chain")

    for i, player_id in enumerate(path):
        player_name = player_id_to_name.get(player_id, str(player_id))
        icon = "⚽ " if i == 0 or i == len(path) - 1 else "👤 "

        st.markdown(
            f'<div class="player-node">{icon}<strong>{i + 1}.</strong> {player_name}</div>',
            unsafe_allow_html=True,
        )

        if i < len(path) - 1:
            _render_arrow_with_stats(player_id, path[i + 1], teammate_stats)


def _render_arrow_with_stats(
    player_id: int,
    next_player_id: int,
    teammate_stats: Dict[Tuple[int, int], Dict[str, Any]],
) -> None:
    """Render the arrow connector with optional stats."""
    stats = teammate_stats.get((player_id, next_player_id), {})

    minutes = stats.get("minutes")
    goals = stats.get("goals")

    stats_parts = []
    if pd.notna(minutes) and minutes:
        stats_parts.append(f"{int(minutes):,} mins together")
    if pd.notna(goals) and goals:
        stats_parts.append(f"{int(goals)} joint goals")

    if stats_parts:
        stats_str = " • ".join(stats_parts)
        st.markdown(
            f'<div class="arrow">⬇️ <em>played with</em><small>📊 {stats_str}</small></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="arrow">⬇️ <em>played with</em></div>',
            unsafe_allow_html=True,
        )
