import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np

class Area:
    """
    Represents an M x N area using a list of lists. (Unchanged from before)

    Attributes:
        rows (int): The number of rows (M) in the area.
        cols (int): The number of columns (N) in the area.
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

# --- NEW: Function to display the area graphically ---
def display_graphically(area: Area, color_mapping: dict, title="Area Representation"):
    """
    Displays the Area object as a colored grid using matplotlib.

    Args:
        area (Area): The Area object to display.
        color_mapping (dict): A dictionary mapping cell values to color names.
                              e.g., {'.': 'white', 'X': 'red'}
        title (str): The title for the plot window.
    """
    # 1. Create a mapping from your symbolic values ('.', 'P', etc.) to integers
    # This is necessary because imshow works with numerical data.
    unique_values = sorted(list(color_mapping.keys()))
    value_to_int = {val: i for i, val in enumerate(unique_values)}

    # 2. Create a numerical grid based on the mapping
    numeric_grid = np.zeros((area.rows, area.cols), dtype=int)
    for r in range(area.rows):
        for c in range(area.cols):
            value = area.get_cell(r, c)
            # Use .get() to avoid errors if a value in the grid isn't in the color map
            numeric_grid[r, c] = value_to_int.get(value)

    # 3. Create a custom colormap from your color mapping
    cmap_colors = [color_mapping[val] for val in unique_values]
    cmap = matplotlib.colors.ListedColormap(cmap_colors)

    # 4. Plot the data
    fig, ax = plt.subplots(figsize=(area.cols / 2, area.rows / 2))
    ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')

    # 5. Format the plot for a clean grid look
    ax.set_xticks(np.arange(-.5, area.cols, 1), minor=True)
    ax.set_yticks(np.arange(-.5, area.rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1.5)
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=16)
    
    plt.show()

# --- Main execution block to demonstrate usage ---
if __name__ == "__main__":
    try:
        # Create a 10x15 area
        game_map = Area(M=10, N=15, default_value='.')

        # Modify the area by placing objects
        game_map.set_cell(row=2, col=2, value='P') # Player
        game_map.set_cell(row=8, col=12, value='E') # Exit
        for i in range(5):
            game_map.set_cell(row=i, col=7, value='X') # Wall
            game_map.set_cell(row=5, col=i + 4, value='W') # Water
        
        # Print the text representation to the console
        print("## Text Representation ##")
        print(game_map)

        # 🎨 Define the mapping from cell content to colors
        color_map = {
            '.': 'lightgray',
            'P': '#3498db',  # Blue
            'E': '#2ecc71',  # Green
            'X': '#34495e',  # Dark Gray
            'W': '#5dade2'   # Light Blue
        }

        # Display the graphical representation in a new window
        print("\nDisplaying graphical representation...")
        display_graphically(game_map, color_map, title="My Game Map")

    except (ValueError, IndexError, ImportError) as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        if isinstance(e, ImportError):
            print("Please ensure 'matplotlib' and 'numpy' are installed (`pip install matplotlib numpy`)", file=sys.stderr)