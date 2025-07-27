import matplotlib.pyplot as plt

class GreedyAgent:
    """
    Implements the Greedy AI agent for pathfinding.
    """
    def __init__(self, game):
        self.game = game

    def run(self):
        """
        Runs the Greedy AI simulation.

        This AI chooses the neighbor closest to the exit based on Manhattan distance.
        """
        self.game.mode = 'greedy'
        self.game.ax.set_title("Greedy AI")
        is_done = False
        while not is_done and self.game.request == 'CONTINUE':
            while self.game.is_paused: plt.pause(0.1)
            next_move = self._get_best_move_greedy()
            if next_move is None: break
            self.game._move_player_to(next_move)
            if self.game.player_pos == self.game.exit_pos: is_done = True
            plt.pause(self.game.animation_speed)
        if self.game.request == 'CONTINUE': plt.show()

    def _get_best_move_greedy(self) -> tuple | None:
        """
        Calculates the best next move for the Greedy AI.

        The greedy algorithm chooses the neighbor that is closest to the exit
        based on Manhattan distance.

        Returns:
            A tuple (row, col) of the best move, or None if stuck.
        """
        r, c = self.game.player.pos
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        best_move, min_dist = None, float('inf')
        for n_r, n_c in neighbors:
            if (0 <= n_r < self.game.area.rows and 0 <= n_c < self.game.area.cols and
                self.game.area.get_cell(n_r, n_c) not in self.game.non_walkable):
                dist = abs(n_r - self.game.exit_pos[0]) + abs(n_c - self.game.exit_pos[1])
                if dist < min_dist:
                    min_dist, best_move = dist, (n_r, n_c)
        return best_move
