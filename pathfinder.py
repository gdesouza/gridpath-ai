import sys
import heapq
import random
import os
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
        if not (0 <= row < self.rows and 0 <= col < self.cols): raise IndexError("Cell out of bounds.")
        return self._grid[row][col]

    @classmethod
    def from_list(cls, grid_list):
        M = len(grid_list)
        N = len(grid_list[0]) if M > 0 else 0
        area = cls(M, N)
        area._grid = grid_list
        return area

# --- NEW: Function to load a map from a file ---
def load_map_from_file(filepath):
    """Loads a map from a text file and returns an Area object."""
    try:
        with open(filepath, 'r') as f:
            lines = [line.rstrip() for line in f.readlines()]
        
        while lines and not lines[-1]:
            lines.pop()

        grid = [line.split() for line in lines]
        
        if not grid: raise ValueError("Map file is empty.")
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

# --- NEW: Random Map Generation ---
def generate_random_map(M: int, N: int, wall_density=0.3):
    """Generates a new random Area object and ensures a path exists between P and E."""
    while True:
        game_map = Area(M, N, default_value='.')
        
        # Place Walls
        for r in range(M):
            for c in range(N):
                if random.random() < wall_density:
                    game_map.set_cell(r, c, 'X')

        # Place Player (P) and Exit (E) on empty cells
        empty_cells = []
        for r in range(M):
            for c in range(N):
                if game_map.get_cell(r, c) == '.':
                    empty_cells.append((r, c))
        
        if len(empty_cells) < 2:
            continue # Not enough space, regenerate

        start_pos, exit_pos = random.sample(empty_cells, 2)
        game_map.set_cell(start_pos[0], start_pos[1], 'P')
        game_map.set_cell(exit_pos[0], exit_pos[1], 'E')

        # Check if a path exists. If not, the loop will continue and regenerate.
        if Game(game_map, {}, {'X'}, headless=True)._a_star_pathfinding() is not None:
            print("Generated a new solvable map.")
            return game_map

class Game:
    """ Manages game state, rendering, and all control modes. """
    def __init__(self, area: Area, color_map: dict, non_walkable_tiles: set, headless: bool = False):
        self.area = area
        self.color_map = color_map
        self.non_walkable = non_walkable_tiles
        
        self.start_pos = self._find_char('P')
        self.exit_pos = self._find_char('E')
        
        if self.start_pos is None or self.exit_pos is None:
            raise ValueError("Map must contain a Player ('P') and an Exit ('E').")
        
        self.player_pos = self.start_pos
        self.mode = 'manual' # Default mode
        
        # --- NEW: Control Attributes ---
        self.request = 'CONTINUE' # Can be RESTART, NEW_MAP, MAIN_MENU, EXIT
        self.is_paused = False
        self.animation_speed = 0.15

        # Matplotlib Setup (only if not in headless mode)
        self.fig, self.ax, self.im = None, None, None
        if not headless:
            self.unique_values = sorted(list(self.color_map.keys()))
            self.value_to_int = {val: i for i, val in enumerate(self.unique_values)}
            cmap = matplotlib.colors.ListedColormap([self.color_map[val] for val in self.unique_values])
            self.fig, self.ax = plt.subplots(figsize=(self.area.cols / 2.5, self.area.rows / 2.5))
            self.im = self.ax.imshow(self._create_numeric_grid(), cmap=cmap, interpolation='nearest')
            self._format_plot("Game Board")

    def _find_char(self, char: str):
        # ... (implementation is identical to before)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                if self.area.get_cell(r, c) == char:
                    return (r, c)
        return None

    # --- NEW: Master Key Press Handler ---
    def on_key_press(self, event):
        """Handles all key presses for global commands and player movement."""
        # Global Controls
        if event.key == 'e': self.request = 'EXIT'
        elif event.key == 'r': self.request = 'RESTART'
        elif event.key == 'n': self.request = 'NEW_MAP'
        elif event.key == 'm': self.request = 'MAIN_MENU'
        
        if self.request != 'CONTINUE':
            plt.close(self.fig)
            return

        # AI-Specific Controls
        if self.mode != 'manual':
            if event.key == 'p':
                self.is_paused = not self.is_paused
                title = self.ax.get_title()
                if self.is_paused and "(Paused)" not in title:
                    self.ax.set_title(title + " (Paused)")
                elif not self.is_paused:
                    self.ax.set_title(title.replace(" (Paused)", ""))
                self.fig.canvas.draw_idle()
            elif event.key == 's': # Slower
                self.animation_speed = min(1.0, self.animation_speed + 0.05)
            elif event.key == 'f': # Faster
                self.animation_speed = max(0.01, self.animation_speed - 0.05)
            return # Don't process movement keys in AI mode

        # Manual Movement
        # ... (implementation is identical to before)
        old_r, old_c = self.player_pos
        new_r, new_c = old_r, old_c
        if event.key == 'up': new_r -= 1
        elif event.key == 'down': new_r += 1
        elif event.key == 'left': new_c -= 1
        elif event.key == 'right': new_c += 1
        else: return
        if (0 <= new_r < self.area.rows and 0 <= new_c < self.area.cols and
            self.area.get_cell(new_r, new_c) not in self.non_walkable):
            self.area.set_cell(old_r, old_c, 'V')
            self.area.set_cell(new_r, new_c, 'P')
            self.player_pos = (new_r, new_c)
            self.update_display()
            
    # --- Run Methods (now with pause and speed logic) ---
    def run_manual(self):
        self.mode = 'manual'
        self.ax.set_title("Manual Control")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        plt.show()

    def run_greedy_ai(self):
        self.mode = 'greedy'
        self.ax.set_title("Greedy AI")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        print("Starting Greedy AI... (p)ause, (s)lower, (f)aster")
        # ... (rest of implementation is identical to before, but with pause/speed)
        is_done = False
        while not is_done and self.request == 'CONTINUE':
            while self.is_paused and self.request == 'CONTINUE':
                plt.pause(0.1)
            if self.request != 'CONTINUE': break
            
            # ... (Greedy step logic)
            next_move = self._get_best_move_greedy()
            if next_move is None:
                print("Greedy AI is stuck!"); break
            self.area.set_cell(self.player_pos[0], self.player_pos[1], 'V')
            self.area.set_cell(next_move[0], next_move[1], 'P')
            self.player_pos = next_move
            self.update_display()
            if self.player_pos == self.exit_pos:
                print("Greedy AI reached the exit."); is_done = True
            
            plt.pause(self.animation_speed)
        
        if self.request == 'CONTINUE': plt.show() # Keep window open if not closed by a key command

    def run_a_star_ai(self):
        self.mode = 'a_star'
        self.ax.set_title("A* AI")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        print("Calculating A* path... (p)ause, (s)lower, (f)aster")
        path = self._a_star_pathfinding()
        
        if path is None:
            print("A* AI could not find a path.")
        else:
            print(f"Path found! Animating {len(path)-1} moves...")
            for move in path:
                while self.is_paused and self.request == 'CONTINUE':
                    plt.pause(0.1)
                if self.request != 'CONTINUE': break

                self.area.set_cell(self.player_pos[0], self.player_pos[1], 'V')
                self.area.set_cell(move[0], move[1], 'P')
                self.player_pos = move
                self.update_display()
                plt.pause(self.animation_speed)

            if not self.is_paused: print("A* AI has reached the exit.")
        
        if self.request == 'CONTINUE': plt.show()
    
    # --- Backend logic (A*, greedy move, display updates) is identical to before ---
    def _get_best_move_greedy(self):
        # ...
        r, c = self.player_pos
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        best_move, min_dist = None, float('inf')
        for n_r, n_c in neighbors:
            if (0 <= n_r < self.area.rows and 0 <= n_c < self.area.cols and
                self.area.get_cell(n_r, n_c) not in self.non_walkable):
                dist = abs(n_r-self.exit_pos[0]) + abs(n_c-self.exit_pos[1])
                if dist < min_dist: min_dist, best_move = dist, (n_r, n_c)
        return best_move
    def _a_star_pathfinding(self):
        # ...
        open_set = [(abs(self.start_pos[0]-self.exit_pos[0]) + abs(self.start_pos[1]-self.exit_pos[1]), self.start_pos)]
        came_from = {}
        g_score = { (r,c): float('inf') for r in range(self.area.rows) for c in range(self.area.cols) }
        g_score[self.start_pos] = 0
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.exit_pos: return [current] if current not in came_from else self._reconstruct_path(came_from, current)
            r, c = current
            neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            for n_r, n_c in neighbors:
                if (0 <= n_r < self.area.rows and 0 <= n_c < self.area.cols and
                    self.area.get_cell(n_r, n_c) not in self.non_walkable):
                    neighbor = (n_r, n_c)
                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + abs(n_r-self.exit_pos[0]) + abs(n_c-self.exit_pos[1])
                        heapq.heappush(open_set, (f_score, neighbor))
        return None
    def _reconstruct_path(self, came_from, current):
        # ...
        path = [current]
        while current in came_from: current = came_from[current]; path.insert(0, current)
        return path[1:]
    def _create_numeric_grid(self):
        # ...
        numeric_grid = np.zeros((self.area.rows, self.area.cols), dtype=int)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                numeric_grid[r, c] = self.value_to_int.get(self.area.get_cell(r, c))
        return numeric_grid
    def _format_plot(self, title: str):
        # ...
        self.ax.set_xticks(np.arange(-.5, self.area.cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.area.rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=1.5)
        self.ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
        self.ax.set_title(title, fontsize=16)
    def update_display(self):
        # ...
        new_numeric_grid = self._create_numeric_grid()
        self.im.set_data(new_numeric_grid)
        self.fig.canvas.draw_idle()

    @classmethod
    def from_list(cls, grid_list):
        M = len(grid_list)
        N = len(grid_list[0]) if M > 0 else 0
        area = cls(M, N)
        area._grid = grid_list
        return area

def load_map_from_file(filepath):
    """Loads a map from a text file and returns an Area object."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        grid = [line.strip().split() for line in lines]
        
        # Validation
        if not grid: raise ValueError("Map file is empty.")
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



# --- Main Execution Block (Now a master loop) ---
if __name__ == "__main__":
    color_map = {
        '.': '#d3d3d3', 'V': '#fef08a', 'P': '#3498db',
        'E': '#2ecc71', 'X': '#34495e'
    }
    non_walkable_tiles = {'X'}
    active_map = generate_random_map(15, 25)

    while True:
        print("\n" + "+"+"-"*43+"+")
        print("| GridPath AI Control Menu                  |")
        print("+"+"-"*43+"+")
        print("| 1: Manual Control                 |")
        print("| 2: Greedy AI                      |")
        print("| 3: A* AI (Optimal)                |")
        print("|-------------------------------------------|")
        print("| Map Options:                              |")
        print("|  (l)oad map, (n)ew random map, (e)xit     |")
        print("+"+"-"*43+"+")
        choice = input("Enter your choice: ").lower()

        if choice == 'e':
            print("Exiting program."); break
        
        if choice == 'n':
            active_map = generate_random_map(15, 25); continue

        if choice == 'l':
            filepath = input("Enter the path to the map file: ")
            loaded_map = load_map_from_file(filepath)
            if loaded_map:
                active_map = loaded_map
            else:
                print("Returning to menu.")
            continue

        if choice not in ['1', '2', '3']:
            print("Invalid choice, please try again."); continue

        # Create a game instance with the current active map
        game = Game(active_map, color_map, non_walkable_tiles)

        if choice == '1': game.run_manual()
        elif choice == '2': game.run_greedy_ai()
        elif choice == '3': game.run_a_star_ai()
        
        # After a simulation ends (or is interrupted), handle the request
        if game.request == 'EXIT': break
        if game.request == 'NEW_MAP': active_map = generate_random_map(15, 25)
        # For RESTART or MAIN_MENU, the loop will simply continue, showing the menu again.