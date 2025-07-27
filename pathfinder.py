import sys
import time
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

# The Area class remains exactly the same.
class Area:
    def __init__(self, M: int, N: int, default_value: any = 0):
        if not (isinstance(M, int) and M > 0 and isinstance(N, int) and N > 0):
            raise ValueError("Area dimensions M and N must be positive integers.")
        self._rows = M
        self._cols = N
        self._grid = [[default_value for _ in range(N)] for _ in range(M)]
    @property
    def rows(self) -> int: return self._rows
    @property
    def cols(self) -> int: return self._cols
    def set_cell(self, row: int, col: int, value: any):
        if not (0 <= row < self._rows and 0 <= col < self._cols): raise IndexError("Cell out of bounds.")
        self._grid[row][col] = value
    def get_cell(self, row: int, col: int) -> any:
        if not (0 <= row < self._rows and 0 <= col < self._cols): raise IndexError("Cell out of bounds.")
        return self._grid[row][col]
    def __str__(self) -> str: return "\n".join(" ".join(map(str, row)) for row in self._grid)

class Game:
    """ Manages the game state, now with an AI player. """
    def __init__(self, area: Area, color_map: dict, non_walkable_tiles: set):
        self.area = area
        self.color_map = color_map
        self.non_walkable = non_walkable_tiles
        
        # Find start and goal positions
        self.player_pos = self._find_char('P')
        self.exit_pos = self._find_char('E')
        
        if self.player_pos is None: raise ValueError("Player 'P' not found.")
        if self.exit_pos is None: raise ValueError("Exit 'E' not found.")

        # --- Matplotlib Setup (same as before) ---
        self.unique_values = sorted(list(self.color_map.keys()))
        self.value_to_int = {val: i for i, val in enumerate(self.unique_values)}
        cmap_colors = [self.color_map[val] for val in self.unique_values]
        cmap = matplotlib.colors.ListedColormap(cmap_colors)
        self.fig, self.ax = plt.subplots(figsize=(self.area.cols / 2.5, self.area.rows / 2.5))
        numeric_grid = self._create_numeric_grid()
        self.im = self.ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')
        self._format_plot("AI Player with Heuristics")

    def _find_char(self, char: str) -> tuple[int, int] | None:
        """Finds the coordinates of a given character."""
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                if self.area.get_cell(r, c) == char:
                    return (r, c)
        return None

    # --- AI HEURISTIC AND MOVEMENT LOGIC ---
    def _heuristic_distance(self, pos1: tuple, pos2: tuple) -> int:
        """Calculates the Manhattan distance between two points."""
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) + abs(c1 - c2)

    def _get_best_move(self) -> tuple[int, int] | None:
        """Finds the best neighboring cell to move to based on the heuristic."""
        r, c = self.player_pos
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        
        best_move = None
        min_dist = float('inf')

        for n_r, n_c in neighbors:
            # Check for valid move (within bounds and not an obstacle)
            if (0 <= n_r < self.area.rows and 
                0 <= n_c < self.area.cols and
                self.area.get_cell(n_r, n_c) not in self.non_walkable):
                
                dist = self._heuristic_distance((n_r, n_c), self.exit_pos)
                if dist < min_dist:
                    min_dist = dist
                    best_move = (n_r, n_c)
                    
        return best_move

    def run_ai_step(self) -> bool:
        """Executes a single step of the AI's logic."""
        # Find the best move from the current position
        next_move = self._get_best_move()

        if next_move is None:
            print("AI is stuck!")
            return True # End the simulation

        # Move the player
        old_r, old_c = self.player_pos
        self.area.set_cell(old_r, old_c, 'V')
        
        new_r, new_c = next_move
        self.area.set_cell(new_r, new_c, 'P')
        self.player_pos = (new_r, new_c)

        # Update the display
        self.update_display()
        
        # Check if the player has reached the exit
        if self.player_pos == self.exit_pos:
            print("Success! The AI has reached the exit.")
            return True # End the simulation
        
        return False # Continue simulation

    def run_ai_simulation(self):
        """Runs the AI simulation with animation."""
        print("Starting AI simulation...")
        is_done = False
        while not is_done:
            is_done = self.run_ai_step()
            plt.pause(0.15) # Pause to animate the movement
        plt.show() # Keep the final window open

    # --- Display Functions (mostly unchanged) ---
    def _create_numeric_grid(self):
        # ... (code is identical to before)
        numeric_grid = np.zeros((self.area.rows, self.area.cols), dtype=int)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                value = self.area.get_cell(r, c)
                numeric_grid[r, c] = self.value_to_int.get(value)
        return numeric_grid

    def _format_plot(self, title: str):
        # ... (code is identical to before)
        self.ax.set_xticks(np.arange(-.5, self.area.cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.area.rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=1.5)
        self.ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
        self.ax.set_title(title, fontsize=16)

    def update_display(self):
        # ... (code is identical to before)
        new_numeric_grid = self._create_numeric_grid()
        self.im.set_data(new_numeric_grid)
        self.fig.canvas.draw_idle()

# --- Main execution block ---
if __name__ == "__main__":
    try:
        game_map = Area(M=10, N=15, default_value='.')
        
        # A map with a U-shaped obstacle to show a potential weakness
        game_map.set_cell(row=8, col=2, value='P') 
        game_map.set_cell(row=1, col=13, value='E')
        for r in range(2, 8): game_map.set_cell(r, 6, value='X')
        for c in range(7, 13): game_map.set_cell(2, c, value='X')
        for c in range(7, 13): game_map.set_cell(7, c, value='X')

        color_map = {
            '.': '#d3d3d3', 'V': '#fef08a', 'P': '#3498db',
            'E': '#2ecc71', 'X': '#34495e', 'W': '#5dade2'
        }
        non_walkable_tiles = {'X', 'W'}

        # Create and run the AI game
        game = Game(game_map, color_map, non_walkable_tiles)
        game.run_ai_simulation()

    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)