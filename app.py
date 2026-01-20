import streamlit as st
import pandas as pd
from collections import defaultdict, deque

# Page configuration
st.set_page_config(
    page_title="The Separation Game ⚽", page_icon="⚽", layout="centered"
)

# Custom CSS for styling
st.markdown(
    """
<style>
    .main-title {
        text-align: center;
        color: #1e3a5f;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .connection-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .player-node {
        background: #f8f9fa;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    .arrow {
        text-align: center;
        color: #667eea;
        font-size: 1.5rem;
        margin: 0.3rem 0;
    }
    .degree-badge {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_data():
    """Load player data and build the teammate graph."""
    from datetime import datetime
    import re

    # Load CSVs
    df_players = pd.read_csv("data/player_profiles.csv", low_memory=False)
    df_teammates = pd.read_csv("data/player_teammates_played_with.csv")

    # Filter out rows with missing player names
    df_players = df_players.dropna(subset=["player_name"])

    # Extract clean player name (remove ID from name like "Miroslav Klose (10)")
    def clean_player_name(name):
        if pd.isna(name):
            return name
        # Remove trailing " (ID)" pattern
        cleaned = re.sub(r"\s*\(\d+\)$", "", str(name))
        return cleaned.strip()

    df_players["clean_name"] = df_players["player_name"].apply(clean_player_name)

    # Create lookup dictionaries using clean names
    player_id_to_name = df_players.set_index("player_id")["clean_name"].to_dict()
    # player_name_to_id = df_players.set_index("clean_name")["player_id"].to_dict()

    current_year = datetime.now().year

    display_names = []
    display_to_id = {}

    for _, row in df_players.iterrows():
        player_id = row["player_id"]
        player_name = row["clean_name"]

        # Skip if player_name is somehow still NaN
        if pd.isna(player_name):
            continue

        # Calculate age from date_of_birth
        dob = row.get("date_of_birth", None)
        age_str = ""
        if pd.notna(dob):
            try:
                birth_year = int(str(dob)[:4])
                age = current_year - birth_year
                age_str = f", {age} yrs"
            except (ValueError, TypeError):
                pass

        # Add club info
        club = row.get("current_club_name", "Unknown")
        if pd.isna(club):
            club = "Unknown"
        display_name = f"{player_name} ({club}{age_str})"

        display_names.append(display_name)
        display_to_id[display_name] = player_id

    # Sort display names for better UX (filter out any non-strings just in case)
    display_names = sorted(
        [name for name in set(display_names) if isinstance(name, str)]
    )

    # Build teammate graph (adjacency list) and store teammate stats
    teammate_graph = defaultdict(set)
    teammate_stats = {}  # (player_id, teammate_id) -> {minutes, goals}

    for _, row in df_teammates.iterrows():
        player_id = row["player_id"]
        teammate_id = row["teammate_player_id"]
        teammate_graph[player_id].add(teammate_id)
        teammate_graph[teammate_id].add(player_id)

        # Store stats for both directions
        minutes = row.get("minutes_played_with", None)
        goals = row.get("joint_goal_participation", None)
        stats = {"minutes": minutes, "goals": goals}
        teammate_stats[(player_id, teammate_id)] = stats
        teammate_stats[(teammate_id, player_id)] = stats

    return (
        display_names,
        display_to_id,
        player_id_to_name,
        dict(teammate_graph),
        teammate_stats,
    )


def find_separation_path(
    start_id: int, end_id: int, teammate_graph: dict, player_id_to_name: dict
) -> list | None:
    """
    Find the shortest path between two players using BFS.
    Returns a list of player IDs representing the path, or None if no path exists.
    """
    if start_id == end_id:
        return [start_id]

    # BFS to find shortest path
    queue = deque([(start_id, [start_id])])
    visited = {start_id}

    while queue:
        current_id, path = queue.popleft()

        for neighbor_id in teammate_graph.get(current_id, []):
            if neighbor_id == end_id:
                # Found the target - return the path of IDs
                return path + [end_id]

            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None


def display_path_result(path: list, player_id_to_name: dict, teammate_stats: dict):
    """Display the connection path in a visually appealing way."""
    degrees = len(path) - 1

    # Success header
    st.markdown(
        f"""
    <div class="connection-card">
        <h2>✅ Connection Found!</h2>
        <div class="degree-badge">{degrees} degree{"s" if degrees != 1 else ""} of separation</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Display the path
    st.markdown("### 🔗 Connection Chain")

    for i, player_id in enumerate(path):
        player_name = player_id_to_name.get(player_id, str(player_id))
        st.markdown(
            f'<div class="player-node"><strong>{i + 1}.</strong> {player_name}</div>',
            unsafe_allow_html=True,
        )

        if i < len(path) - 1:
            # Get stats for this connection
            next_player_id = path[i + 1]
            stats = teammate_stats.get((player_id, next_player_id), {})

            minutes = stats.get("minutes")
            goals = stats.get("goals")

            # Build stats string
            stats_parts = []
            if pd.notna(minutes) and minutes:
                stats_parts.append(f"{int(minutes):,} mins together")
            if pd.notna(goals) and goals:
                stats_parts.append(f"{int(goals)} joint goals")

            if stats_parts:
                stats_str = " • ".join(stats_parts)
                st.markdown(
                    f'<div class="arrow">↓ <em>played with</em> ↓<br><small style="color: #888;">📊 {stats_str}</small></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="arrow">↓ <em>played with</em> ↓</div>',
                    unsafe_allow_html=True,
                )


def main():
    # Header
    st.markdown(
        '<h1 class="main-title">⚽ The Separation Game</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">Find the shortest connection between any two football players!</p>',
        unsafe_allow_html=True,
    )

    # Load data with spinner
    with st.spinner(
        "🔄 Loading player database... This may take a moment on first load."
    ):
        (
            display_names,
            display_to_id,
            player_id_to_name,
            teammate_graph,
            teammate_stats,
        ) = load_data()

    # Player count info
    st.info(
        f"📊 Database contains **{len(display_names):,}** players with **{sum(len(v) for v in teammate_graph.values()) // 2:,}** teammate connections"
    )

    # Player selection
    st.markdown("### 🎯 Select Two Players")

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox(
            "First Player",
            options=display_names,
            index=None,
            placeholder="Type to search...",
            key="player1",
        )

    with col2:
        player2 = st.selectbox(
            "Second Player",
            options=display_names,
            index=None,
            placeholder="Type to search...",
            key="player2",
        )

    # Find connection button
    st.markdown("")  # Spacing

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        find_button = st.button(
            "🔍 Find Connection", type="primary", use_container_width=True
        )

    # Results
    if find_button:
        if not player1 or not player2:
            st.warning("⚠️ Please select both players!")
        elif player1 == player2:
            st.info("🤔 That's the same player! Select two different players.")
        else:
            # Get player IDs
            start_id = display_to_id.get(player1)
            end_id = display_to_id.get(player2)

            if start_id is None or end_id is None:
                st.error("❌ Could not find one or both players in the database.")
            else:
                with st.spinner("🔍 Searching for connection..."):
                    path = find_separation_path(
                        start_id, end_id, teammate_graph, player_id_to_name
                    )

                if path:
                    display_path_result(path, player_id_to_name, teammate_stats)
                else:
                    st.error("❌ No connection found between these players!")
                    st.markdown(
                        "These players may be in separate components of the teammate network."
                    )

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
        "Built with ❤️ using Streamlit | Data from Transfermarkt"
        "</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
