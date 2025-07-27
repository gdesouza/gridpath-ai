import random
import os
from src.core.area import Area
from src.game.game import Game
from src.agents.a_star_agent import AStarAgent # Import AStarAgent

def generate_random_map(M: int, N: int, wall_density=0.35):
    """
    Generates a new random Area object by first creating a guaranteed solvable path
    and then adding random walls. This is much more efficient than brute-force.
    """
    print("Generating a new solvable map...")
    # 1. Create the actual map, initially filled with walls
    game_map = Area(M, N, default_value='X')

    # 2. Find a guaranteed path using a temporary, open-field map
    pathfinder_map = Area(M, N, default_value='.')
    # Create a headless Game instance for pathfinding check
    pathfinder_game = Game(pathfinder_map, {}, set(), headless=True)
    # Create a temporary AStarAgent instance for the pathfinding check
    temp_astar_agent = AStarAgent(pathfinder_game)
    
    # Select start and end points that are reasonably far apart
    start_pos = (random.randint(0, M//4), random.randint(0, N//4))
    exit_pos = (random.randint(M*3//4, M-1), random.randint(N*3//4, N-1))

    # The pathfinder will never fail on an open map. Request the full path.
    guaranteed_path = temp_astar_agent._a_star_pathfinding(start_pos, exit_pos, include_start=True)

    # 3. Carve the guaranteed path into the wall-filled map
    path_cells = set(guaranteed_path)
    for r, c in guaranteed_path:
        game_map.set_cell(r, c, '.')

    # 4. Randomly add open spaces (remove walls), avoiding the main path
    for r in range(M):
        for c in range(N):
            if (r, c) in path_cells:
                continue # Don't touch the guaranteed path
            if random.random() > wall_density:
                game_map.set_cell(r, c, '.')

    # 5. Set the player and exit points for the reachability test
    game_map.set_cell(start_pos[0], start_pos[1], 'P')
    game_map.set_cell(exit_pos[0], exit_pos[1], 'E')

    # 6. Flood fill to find all reachable cells from 'P'
    reachable_cells = set()
    q = [start_pos]
    visited_flood_fill = {start_pos}
    
    while q:
        r, c = q.pop(0)
        reachable_cells.add((r, c))
        
        # Check neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_r, n_c = r + dr, c + dc
            neighbor = (n_r, n_c)
            if (0 <= n_r < M and 0 <= n_c < N and
                neighbor not in visited_flood_fill and
                game_map.get_cell(n_r, n_c) != 'X'):
                visited_flood_fill.add(neighbor)
                q.append(neighbor)

    # 7. Fill in all non-reachable cells with walls
    for r in range(M):
        for c in range(N):
            if (r, c) not in reachable_cells:
                game_map.set_cell(r, c, 'X')
    
    print("Map generated and cleaned successfully.")
    return game_map

def load_map_from_file(filepath: str) -> Area | None:
    """
    Loads a map from a text file and returns an Area object.

    The map file should be a grid of characters, where each character
    represents a cell type. Rows are separated by newlines, and columns
    can be separated by spaces.

    Args:
        filepath (str): The path to the map file.

    Returns:
        An Area object if the map is loaded successfully, otherwise None.
    """
    try:
        with open(filepath, 'r') as f:
            lines = [line.rstrip() for line in f.readlines()]
        
        while lines and not lines[-1]:
            lines.pop()

        grid = [line.split() for line in lines]
        
        if not grid:
            raise ValueError("Map file is empty.")
        num_cols = len(grid[0])
        if any(len(row) != num_cols for row in grid):
            raise ValueError("Map file has inconsistent row lengths.")
        
        print(f"Successfully loaded map '{os.path.basename(filepath)}'.")
        return Area.from_list(grid)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'.")
        return None
    except Exception as e:
        print(f"Error loading map: {e}")
        return None
