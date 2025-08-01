import matplotlib.pyplot as plt
import heapq

class FrontierAgent:
    """
    Implements the Frontier Exploration AI agent.
    """
    def __init__(self, game):
        self.game = game
        self.game.visited_cells = {self.game.player_pos}

    def run(self):
        """
        Runs the Frontier Exploration AI simulation.

        This AI explores the map by moving towards the closest unvisited, walkable cell.
        """
        self.game.mode = 'frontier_exploration'
        self.game.ax.set_title("Frontier Exploration AI")
        while self.game.request == 'CONTINUE':
            while self.game.is_paused: plt.pause(0.1)
            if self.game.request != 'CONTINUE': break

            frontier = self._find_frontier()
            if not frontier:
                print("Frontier AI has covered all reachable area."); break

            closest_frontier_cell = min(frontier, key=lambda cell: self._heuristic_distance(self.game.player_pos, cell))
            path_to_frontier = self._a_star_pathfinding(self.game.player_pos, closest_frontier_cell, include_start=False)

            if not path_to_frontier:
                print("Could not find path to frontier, exploration complete."); break

            for move in path_to_frontier:
                self.game._move_player_to(move)
                plt.pause(self.game.animation_speed)
                if self.game.request != 'CONTINUE': return
        
        if self.game.request == 'CONTINUE': plt.show()

    def _find_frontier(self) -> set:
        """
        Finds all visited cells adjacent to unvisited, walkable cells.

        Returns:
            A set of (row, col) tuples representing frontier cells.
        """
        frontier = set()
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for r_v, c_v in self.game.visited_cells:
            for dr, dc in moves:
                n_r, n_c = r_v + dr, c_v + dc
                if (0 <= n_r < self.game.area.rows and 0 <= n_c < self.game.area.cols and
                    (n_r, n_c) not in self.game.visited_cells and
                    self.game.area.get_cell(n_r, n_c) not in self.game.non_walkable):
                    frontier.add((n_r, n_c))
        return frontier

    def _heuristic_distance(self, pos1: tuple, pos2: tuple) -> int:
        """
        Calculates the Manhattan distance between two positions.

        Args:
            pos1 (tuple): The first position (row, col).
            pos2 (tuple): The second position (row, col).

        Returns:
            The Manhattan distance as an integer.
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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
        open_set = [(self._heuristic_distance(start, goal), start)]
        came_from, g_score = {}, {start: 0}
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return self._reconstruct_path(came_from, current, include_start)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if not (0 <= neighbor[0] < self.game.area.rows and 0 <= neighbor[1] < self.game.area.cols and
                        self.game.area.get_cell(neighbor[0], neighbor[1]) not in self.game.non_walkable):
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self._heuristic_distance(neighbor, goal)
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
