import sys
import heapq
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
    """ Manages game state, rendering, and all control modes. """
    def __init__(self, area: Area, color_map: dict, non_walkable_tiles: set):
        self.area = area
        self.color_map = color_map
        self.non_walkable = non_walkable_tiles
        
        self.start_pos = self._find_char('P')
        self.exit_pos = self._find_char('E')
        
        if self.start_pos is None: raise ValueError("Player 'P' not found.")
        if self.exit_pos is None: raise ValueError("Exit 'E' not found.")
        
        self.player_pos = self.start_pos

        # --- Matplotlib Setup ---
        self.unique_values = sorted(list(self.color_map.keys()))
        self.value_to_int = {val: i for i, val in enumerate(self.unique_values)}
        cmap_colors = [self.color_map[val] for val in self.unique_values]
        cmap = matplotlib.colors.ListedColormap(cmap_colors)
        self.fig, self.ax = plt.subplots(figsize=(self.area.cols / 2.5, self.area.rows / 2.5))
        numeric_grid = self._create_numeric_grid()
        self.im = self.ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')
        self._format_plot("Game Board")

    def _find_char(self, char: str):
        # ... (code is identical to before)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                if self.area.get_cell(r, c) == char:
                    return (r, c)
        return None

    ## Manual Control Mode
    def run_manual(self):
        self.ax.set_title("Manual Control Mode")
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        print("Controls enabled. Use arrow keys to move. Close the window to exit.")
        plt.show()

    def on_key_press(self, event):
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
    
    ## Greedy AI Mode
    def run_greedy_ai(self):
        self.ax.set_title("Greedy AI Mode")
        print("Starting Greedy AI simulation...")
        is_done = False
        while not is_done:
            is_done = self._greedy_ai_step()
            plt.pause(0.15)
        plt.show()

    def _greedy_ai_step(self):
        next_move = self._get_best_move_greedy()
        if next_move is None:
            print("Greedy AI is stuck!")
            return True

        self.area.set_cell(self.player_pos[0], self.player_pos[1], 'V')
        self.area.set_cell(next_move[0], next_move[1], 'P')
        self.player_pos = next_move
        self.update_display()

        if self.player_pos == self.exit_pos:
            print("Greedy AI has reached the exit.")
            return True
        return False

    def _get_best_move_greedy(self):
        r, c = self.player_pos
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        best_move, min_dist = None, float('inf')
        for n_r, n_c in neighbors:
            if (0 <= n_r < self.area.rows and 0 <= n_c < self.area.cols and
                self.area.get_cell(n_r, n_c) not in self.non_walkable):
                dist = self._heuristic_distance((n_r, n_c), self.exit_pos)
                if dist < min_dist:
                    min_dist, best_move = dist, (n_r, n_c)
        return best_move

    ## A* AI Mode 
    def run_a_star_ai(self):
        self.ax.set_title("A* AI Mode")
        print("Calculating optimal path with A*...")
        path = self._a_star_pathfinding()

        if path is None:
            print("A* AI could not find a path to the exit.")
            plt.show()
            return

        print(f"Path found! Animating {len(path)-1} moves...")
        for move in path:
            self.area.set_cell(self.player_pos[0], self.player_pos[1], 'V')
            self.area.set_cell(move[0], move[1], 'P')
            self.player_pos = move
            self.update_display()
            plt.pause(0.15)
        
        self.area.set_cell(self.player_pos[0], self.player_pos[1], 'P') # Ensure player is 'P' at the end
        self.update_display()
        print("A* AI has reached the exit.")
        plt.show()

    def _heuristic_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path[1:] # Exclude the starting position

    def _a_star_pathfinding(self):
        open_set = [(self._heuristic_distance(self.start_pos, self.exit_pos), self.start_pos)]
        came_from = {}
        g_score = { (r,c): float('inf') for r in range(self.area.rows) for c in range(self.area.cols) }
        g_score[self.start_pos] = 0

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == self.exit_pos:
                return self._reconstruct_path(came_from, current)

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
                        f_score = tentative_g_score + self._heuristic_distance(neighbor, self.exit_pos)
                        heapq.heappush(open_set, (f_score, neighbor))
        return None # No path found

    ## Common Display Functions
    def _create_numeric_grid(self):
        # ... (code is identical to before)
        numeric_grid = np.zeros((self.area.rows, self.area.cols), dtype=int)
        for r in range(self.area.rows):
            for c in range(self.area.cols):
                numeric_grid[r, c] = self.value_to_int.get(self.area.get_cell(r, c))
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
    game_map = Area(M=10, N=15, default_value='.')
    
    # A map with a U-shaped obstacle to show the difference between Greedy and A*
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

    try:
        # --- User Mode Selection ---
        print("+" + "-"*27 + "+")
        print("| Select a Control Mode     |")
        print("+" + "-"*27 + "+")
        print("| 1: Manual Control         |")
        print("| 2: Greedy AI (Can get stuck)|")
        print("| 3: A* AI (Optimal path)     |")
        print("+" + "-"*27 + "+")
        choice = input("Enter choice (1/2/3): ")

        game = Game(game_map, color_map, non_walkable_tiles)

        if choice == '1':
            game.run_manual()
        elif choice == '2':
            game.run_greedy_ai()
        elif choice == '3':
            game.run_a_star_ai()
        else:
            print("Invalid choice. Exiting.")

    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)