"""
Pathfinding algorithm for finding player connections.
"""

from collections import deque
from typing import Dict, Set, List


def find_separation_path(
    start_id: int, end_id: int, teammate_graph: Dict[int, Set[int]]
) -> List[int] | None:
    """
    Find the shortest path between two players using BFS.

    Args:
        start_id: Starting player's ID
        end_id: Target player's ID
        teammate_graph: Adjacency list of teammate connections

    Returns:
        List of player IDs representing the path, or None if no path exists
    """
    if start_id == end_id:
        return [start_id]

    queue = deque([(start_id, [start_id])])
    visited = {start_id}

    while queue:
        current_id, path = queue.popleft()

        for neighbor_id in teammate_graph.get(current_id, []):
            if neighbor_id == end_id:
                return path + [end_id]

            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None
