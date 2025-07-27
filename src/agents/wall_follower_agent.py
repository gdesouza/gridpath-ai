import matplotlib.pyplot as plt

class WallFollowerAgent:
    """
    Implements the Wall Follower AI agent.
    """
    def __init__(self, game):
        self.game = game
        self.game.visited_cells = {self.game.player_pos}
        self.game.player_direction = 2 # 0:N, 1:E, 2:S, 3:W

    def run(self):
        """
        Runs the Wall Follower AI simulation.

        This AI uses the left-hand rule to navigate the maze, primarily for
        area coverage or finding an exit in a connected maze.
        """
        self.game.mode = 'wall_follower'
        self.game.ax.set_title("Wall Follower AI")
        no_new_cells_count = 0
        while self.game.request == 'CONTINUE':
            while self.game.is_paused: plt.pause(0.1)
            if self.game.request != 'CONTINUE': break

            prev_visited_count = len(self.game.visited_cells)
            self._wall_follower_step()
            if len(self.game.visited_cells) == prev_visited_count:
                no_new_cells_count += 1
            else:
                no_new_cells_count = 0
            
            if no_new_cells_count > self.game.area.rows * self.game.area.cols: # Heuristic to detect full coverage
                print("Wall Follower has covered all reachable area."); break
            
            plt.pause(self.game.animation_speed)
        if self.game.request == 'CONTINUE': plt.show()

    def _wall_follower_step(self):
        """
        Executes one move using the left-hand rule for the Wall Follower AI.

        The AI prioritizes turning left, then moving forward, then turning right,
        and finally turning around if no other moves are possible.
        """
        r, c = self.game.player_pos
        # Relative directions: N, E, S, W
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Order to check: Left, Forward, Right, Back
        # (current_dir - 1)%4 = Left, current_dir = Fwd, (current_dir + 1)%4 = Right
        for i in range(-1, 2):
            check_dir = (self.game.player_direction + i + 4) % 4
            n_r, n_c = r + moves[check_dir][0], c + moves[check_dir][1]

            if (0 <= n_r < self.game.area.rows and 0 <= n_c < self.game.area.cols and
                self.game.area.get_cell(n_r, n_c) not in self.game.non_walkable):
                self.game.player_direction = check_dir
                self.game._move_player_to((n_r, n_c))
                return
        
        # If all else fails, turn around
        self.game.player_direction = (self.game.player_direction + 2) % 4
