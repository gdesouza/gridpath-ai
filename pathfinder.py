import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

class Area:
    """
    Represents an M x N area using a list of lists. (Unchanged)
    """
    def __init__(self, M: int, N: int, default_value: any = 0):
        if not (isinstance(M, int) and M > 0 and isinstance(N, int) and N > 0):
            raise ValueError("Area dimensions M and N must be positive integers.")
        self._rows = M
        self._cols = N
        self._grid = [[default_value for _ in range(N)] for _ in range(M)]

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def set_cell(self, row: int, col: int, value: any):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Cell coordinates are out of bounds.")
        self._grid[row][col] = value

    def get_cell(self, row: int, col: int) -> any:
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Cell coordinates are out of bounds.")
        return self._grid[row][col]

    def __str__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self._grid)

# --- NEW: Game class to manage state and interactivity ---
class Game:
    """
    Manages the game state, rendering, and player controls.
    """
    def __init__(self, area: Area, color_map: dict, non_walkable_tiles: set):
        self.area = area
        self.color_map = color_map
        self.non_walkable = non_walkable_tiles
        
        # Find the player's starting position
        self.player_pos = self._find_player()
        if self.player_pos is None:
            raise ValueError("Player 'P' not found in the area.")

        # --- Matplotlib Setup ---
        # Create a mapping from values like 'P' to integers for plotting
        self.unique_values = sorted(list(self.color_map.keys()))
        self.value_to_int = {val: i for i, val in enumerate(self.unique_values)}
        
        # Create the custom colormap
        cmap_colors = [self.color_map[val] for val in self.unique_values]
        cmap = matplotlib.colors.ListedColormap(cmap_colors)

        # Create the plot figure and axis
        self.fig, self.ax = plt.subplots(figsize=(self.area.cols / 2.5, self.area.rows / 2.5))
        numeric_grid = self._create_numeric_grid()
        self.im = self.ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')
        
        self._format_plot()
        
        # Connect the key press event to our handler function
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        print("Controls enabled. Use arrow keys to move the player. Close the window to exit.")

    def _find_player(self) -> tuple[int, int] | None:
        """Finds the coordinates of the player 'P'."""
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                if self.area.get_cell(r, c) == 'P':
                    return (r, c)
        return None

    def _create_numeric_grid(self) -> np.ndarray:
        """Converts the Area object's grid into a NumPy array of integers for plotting."""
        numeric_grid = np.zeros((self.area.rows, self.area.cols), dtype=int)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                value = self.area.get_cell(r, c)
                numeric_grid[r, c] = self.value_to_int.get(value)
        return numeric_grid

    def _format_plot(self):
        """Applies formatting to the plot for a clean grid appearance."""
        self.ax.set_xticks(np.arange(-.5, self.area.cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.area.rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=1.5)
        self.ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
        self.ax.set_title("Interactive Player", fontsize=16)

    def on_key_press(self, event):
        """Handles key press events to move the player."""
        old_r, old_c = self.player_pos
        new_r, new_c = old_r, old_c

        # Determine new position based on key pressed
        if event.key == 'up':
            new_r -= 1
        elif event.key == 'down':
            new_r += 1
        elif event.key == 'left':
            new_c -= 1
        elif event.key == 'right':
            new_c += 1
        else:
            return # Ignore other keys

        # --- Collision Detection ---
        # 1. Check if the move is within the grid boundaries
        if not (0 <= new_r < self.area.rows and 0 <= new_c < self.area.cols):
            return # Move is out of bounds
            
        # 2. Check if the destination tile is walkable
        destination_tile = self.area.get_cell(new_r, new_c)
        if destination_tile in self.non_walkable:
            return # Cannot walk into this tile

        # If move is valid, update the area
        self.area.set_cell(old_r, old_c, '.')   # Clear the old position
        self.area.set_cell(new_r, new_c, 'P')   # Set the new position
        self.player_pos = (new_r, new_c)        # Update player's tracked position

        # Redraw the display
        self.update_display()

    def update_display(self):
        """Updates the image data and redraws the canvas."""
        new_numeric_grid = self._create_numeric_grid()
        self.im.set_data(new_numeric_grid)
        self.fig.canvas.draw_idle()

    def run(self):
        """Starts the game by showing the plot."""
        plt.show()

# --- Main execution block ---
if __name__ == "__main__":
    try:
        # Create a 10x15 area
        game_map = Area(M=10, N=15, default_value='.')

        # Place objects: Player 'P', Exit 'E', Wall 'X', Water 'W'
        game_map.set_cell(row=2, col=2, value='P') 
        game_map.set_cell(row=8, col=12, value='E') 
        for i in range(5):
            game_map.set_cell(row=i, col=7, value='X')
            game_map.set_cell(row=5, col=i + 4, value='W')
        
        # 🎨 Define the mapping from cell content to colors
        color_map = {
            '.': '#d3d3d3',  # Light Gray (Floor)
            'P': '#3498db',  # Blue (Player)
            'E': '#2ecc71',  # Green (Exit)
            'X': '#34495e',  # Dark Gray (Wall)
            'W': '#5dade2'   # Light Blue (Water)
        }
        
        # Define which tiles the player cannot move into
        non_walkable_tiles = {'X', 'W'}

        # Create and run the game
        game = Game(game_map, color_map, non_walkable_tiles)
        game.run()

    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)