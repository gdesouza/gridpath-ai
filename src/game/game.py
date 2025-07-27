import heapq
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from src.core.area import Area

class Game:
    """
    Manages the game state, rendering, and all control modes.

    This class is responsible for initializing the game with a given map,
    handling user input, running different AI algorithms, and updating the
    display. It serves as the central controller for the application.

    Attributes:
        area (Area): The game map.
        color_map (dict): A mapping from cell values to display colors.
        non_walkable (set): A set of cell values that are considered obstacles.
        start_pos (tuple): The starting (row, col) of the player.
        exit_pos (tuple): The (row, col) of the exit.
        player_pos (tuple): The current (row, col) of the player.
        mode (str): The current control mode (e.g., 'manual', 'a_star').
        request (str): The current user request (e.g., 'EXIT', 'NEW_MAP').
        is_paused (bool): A flag to indicate if the simulation is paused.
        animation_speed (float): The delay between steps in AI simulations.
        fig, ax: Matplotlib figure and axes for plotting.
        im: The image object for the plot, used for updating the display.
    """
    def __init__(self, area: Area, color_map: dict, non_walkable_tiles: set, headless: bool = False):
        """
        Initializes the Game object.

        Args:
            area (Area): The Area object representing the map.
            color_map (dict): A dictionary mapping cell values to color names.
            non_walkable_tiles (set): A set of characters that are obstacles.
            headless (bool): If True, initializes without a graphical display.
                             This is used for internal checks like map generation.
        """
        self.area = area
        self.color_map = color_map
        self.non_walkable = non_walkable_tiles
        
        self.start_pos = self._find_char('P')
        self.exit_pos = self._find_char('E')
        
        if not headless and (self.start_pos is None or self.exit_pos is None):
            raise ValueError("Map must contain a Player ('P') and an Exit ('E').")
        
        self.player_pos = self.start_pos
        self.mode = 'manual' # Default mode
        
        self.request = 'CONTINUE'
        self.is_paused = False
        self.animation_speed = 0.15

        self.fig, self.ax, self.im = None, None, None
        if not headless:
            self._initialize_plot()

    def _initialize_plot(self):
        """Sets up the initial matplotlib plot for the game board."""
        self.unique_values = sorted(list(self.color_map.keys()))
        self.value_to_int = {val: i for i, val in enumerate(self.unique_values)}
        cmap = matplotlib.colors.ListedColormap([self.color_map.get(val, 'black') for val in self.unique_values])
        
        self.fig, self.ax = plt.subplots(figsize=(self.area.cols / 2.5, self.area.rows / 2.5))
        self.im = self.ax.imshow(self._create_numeric_grid(), cmap=cmap, interpolation='nearest')
        self._format_plot("GridPath AI")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def _find_char(self, char: str) -> tuple | None:
        """
        Finds the first occurrence of a character in the area.

        Args:
            char (str): The character to search for.

        Returns:
            A tuple (row, col) of the character's position, or None if not found.
        """
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                if self.area.get_cell(r, c) == char:
                    return (r, c)
        return None

    def on_key_press(self, event):
        """
        Handles all key press events for the game.

        This includes global controls (exit, new map) and mode-specific
        controls (player movement, AI pause/speed).
        """
        if event.key in 'ernm':
            self.request = {'e': 'EXIT', 'r': 'RESTART', 'n': 'NEW_MAP', 'm': 'MAIN_MENU'}.get(event.key)
            if self.fig: plt.close(self.fig)
            return

        # Manual movement is now handled by the main loop, not directly here
        # This method will primarily handle global controls and pass other events
        # to the active agent if needed.

    def _create_numeric_grid(self) -> np.ndarray:
        """Converts the symbolic grid to a numeric grid for plotting."""
        numeric_grid = np.zeros((self.area.rows, self.area.cols), dtype=int)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                numeric_grid[r, c] = self.value_to_int.get(self.area.get_cell(r, c), -1)
        return numeric_grid

    def _format_plot(self, title: str):
        """Applies standard formatting to the matplotlib plot."""
        self.ax.set_title(title, fontsize=16)
        self.ax.set_xticks(np.arange(-.5, self.area.cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.area.rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=1.5)
        self.ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)

    def update_display(self):
        """Updates the plot with the current state of the grid."""
        self.im.set_data(self._create_numeric_grid())
        self.fig.canvas.draw_idle()

    def _move_player_to(self, new_pos: tuple):
        """
        Moves the player to a new position and updates the display.

        Args:
            new_pos (tuple): The (row, col) to move the player to.
        """
        self.area.set_cell(self.player_pos[0], self.player_pos[1], 'V') # Mark old position as visited
        self.area.set_cell(new_pos[0], new_pos[1], 'P')
        self.player_pos = new_pos
        self.update_display()
