import heapq
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from area import Area

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
        self.mode = 'manual'
        
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

        if self.mode != 'manual':
            if event.key == 'p': self.is_paused = not self.is_paused
            elif event.key == 's': self.animation_speed = min(1.0, self.animation_speed + 0.05)
            elif event.key == 'f': self.animation_speed = max(0.01, self.animation_speed - 0.05)
            return

        old_r, old_c = self.player_pos
        new_r, new_c = old_r, old_c
        if event.key == 'up': new_r -= 1
        elif event.key == 'down': new_r += 1
        elif event.key == 'left': new_c -= 1
        elif event.key == 'right': new_c += 1
        else: return

        if (0 <= new_r < self.area.rows and 0 <= new_c < self.area.cols and
            self.area.get_cell(new_r, new_c) not in self.non_walkable):
            self._move_player_to((new_r, new_c))

    def run_manual(self):
        """Runs the game in manual control mode."""
        self.mode = 'manual'
        self.ax.set_title("Manual Control")
        plt.show()

    def run_greedy_ai(self):
        """Runs the Greedy AI simulation."""
        self.mode = 'greedy'
        self.ax.set_title("Greedy AI")
        is_done = False
        while not is_done and self.request == 'CONTINUE':
            while self.is_paused: plt.pause(0.1)
            next_move = self._get_best_move_greedy()
            if next_move is None: break
            self._move_player_to(next_move)
            if self.player_pos == self.exit_pos: is_done = True
            plt.pause(self.animation_speed)
        if self.request == 'CONTINUE': plt.show()

    def run_a_star_ai(self):
        """Runs the A* pathfinding AI simulation."""
        self.mode = 'a_star'
        self.ax.set_title("A* AI")
        path = self._a_star_pathfinding(self.start_pos, self.exit_pos)
        if path:
            for move in path:
                while self.is_paused: plt.pause(0.1)
                self._move_player_to(move)
                plt.pause(self.animation_speed)
        if self.request == 'CONTINUE': plt.show()

    def _get_best_move_greedy(self) -> tuple | None:
        """
        Calculates the best next move for the Greedy AI.

        The greedy algorithm chooses the neighbor that is closest to the exit
        based on Manhattan distance.

        Returns:
            A tuple (row, col) of the best move, or None if stuck.
        """
        r, c = self.player_pos
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        best_move, min_dist = None, float('inf')
        for n_r, n_c in neighbors:
            if (0 <= n_r < self.area.rows and 0 <= n_c < self.area.cols and
                self.area.get_cell(n_r, n_c) not in self.non_walkable):
                dist = abs(n_r - self.exit_pos[0]) + abs(n_c - self.exit_pos[1])
                if dist < min_dist:
                    min_dist, best_move = dist, (n_r, n_c)
        return best_move

    def _a_star_pathfinding(self, start: tuple, goal: tuple, include_start: bool = False) -> list | None:
        """
        Finds the shortest path from a start to a goal using the A* algorithm.

        Args:
            start (tuple): The starting (row, col) position.
            goal (tuple): The goal (row, col) position.
            include_start (bool): If True, the path includes the start node.

        Returns:
            A list of (row, col) tuples representing the path, or None if no path is found.
        """
        open_set = [(abs(start[0] - goal[0]) + abs(start[1] - goal[1]), start)]
        came_from, g_score = {}, {start: 0}
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return self._reconstruct_path(came_from, current, include_start)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if not (0 <= neighbor[0] < self.area.rows and 0 <= neighbor[1] < self.area.cols and
                        self.area.get_cell(neighbor[0], neighbor[1]) not in self.non_walkable):
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    heapq.heappush(open_set, (f_score, neighbor))
        return None

    def _reconstruct_path(self, came_from: dict, current: tuple, include_start: bool) -> list:
        """
        Reconstructs the path from the came_from map generated by A*.

        Args:
            came_from (dict): A map of nodes pointing to their predecessors.
            current (tuple): The goal node to start reconstruction from.
            include_start (bool): Whether to include the start node in the path.

        Returns:
            A list of (row, col) tuples representing the path.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path if include_start else path[1:]

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
