import random
import os
from area import Area
from game import Game

def generate_random_map(M: int, N: int, wall_density=0.3):
    """
    Generates a new random Area object and ensures a path exists.

    This function repeatedly creates random maps until it finds one where a path
    exists between a randomly placed Player ('P') and Exit ('E').

    Args:
        M (int): The number of rows for the map.
        N (int): The number of columns for the map.
        wall_density (float): The probability of a cell being a wall.

    Returns:
        An Area object representing the solvable map.
    """
    while True:
        game_map = Area(M, N, default_value='.')
        for r in range(M):
            for c in range(N):
                if random.random() < wall_density:
                    game_map.set_cell(r, c, 'X')
        empty_cells = []
        for r in range(M):
            for c in range(N):
                if game_map.get_cell(r, c) == '.':
                    empty_cells.append((r, c))
        if len(empty_cells) < 2:
            continue
        start_pos, exit_pos = random.sample(empty_cells, 2)
        game_map.set_cell(start_pos[0], start_pos[1], 'P')
        game_map.set_cell(exit_pos[0], exit_pos[1], 'E')
        # Use a headless Game instance to check for a path without rendering
        if Game(game_map, {}, {'X'}, headless=True)._a_star_pathfinding(start_pos, exit_pos) is not None:
            print(f"Generated a new solvable map ({M}x{N}).")
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
