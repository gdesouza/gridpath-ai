import matplotlib.pyplot as plt
import numpy as np
from src.agents.q_learning_agent import QLearningAgent
from src.config.q_learning_config import QLearningConfig

class QLearningRunner:
    """
    Manages the Q-Learning simulation, including training and testing phases.
    """
    def __init__(self, game):
        self.game = game
        self.agent = QLearningAgent(actions=[0, 1, 2, 3]) # Actions are 0:N, 1:E, 2:S, 3:W

    def run(self, training_mode=True):
        """
        Runs the Q-Learning agent in either training or testing mode.

        Args:
            training_mode (bool): If True, the agent will train; otherwise, it will test.
        """
        self.game.mode = 'q_learning'
        title_prefix = "Q-Learning (Training)" if training_mode else "Q-Learning (Trained)"
        self.game.ax.set_title(title_prefix)

        if not training_mode:
            try:
                self.agent.load_q_table()
            except FileNotFoundError:
                print("No trained Q-table found. Please run training mode first.")
                return

        episodes = QLearningConfig.EPISODES
        steps_per_episode = QLearningConfig.STEPS_PER_EPISODE
        
        for episode in range(episodes if training_mode else 1):
            self.game.player_pos = self.game.start_pos
            self.game.visited_cells = {self.game.player_pos}
            self.game.update_display() # Full redraw
            total_reward = 0

            for step in range(steps_per_episode):
                if self.game.request != 'CONTINUE': break
                while self.game.is_paused: plt.pause(0.1)

                state = (self.game.player_pos, frozenset(self.game.visited_cells))
                action = self.agent.get_action(state)

                moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                r, c = self.game.player_pos
                n_r, n_c = r + moves[action][0], c + moves[action][1]
                
                reward = 0.0
                if not (0 <= n_r < self.game.area.rows and 0 <= n_c < self.game.area.cols and
                        self.game.area.get_cell(n_r, n_c) not in self.game.non_walkable):
                    reward = -5.0 # Penalty for hitting a wall
                    next_player_pos = self.game.player_pos # Stay in place
                else:
                    if (n_r, n_c) == self.game.exit_pos:
                        reward = 10.0 # Reward for reaching exit
                    elif (n_r, n_c) in self.game.visited_cells:
                        reward = -0.2 # Small penalty for re-visiting
                    else:
                        reward = 1.0 # Reward for exploring new cells
                    next_player_pos = (n_r, n_c)
                
                total_reward += reward
                
                next_visited = self.game.visited_cells.union({next_player_pos})
                next_state = (next_player_pos, frozenset(next_visited))
                
                if training_mode:
                    self.agent.update(state, action, reward, next_state)

                self.game._move_player_to(next_player_pos)
                
                if episode > episodes - 5 or not training_mode:
                    plt.pause(self.game.animation_speed)

                if next_player_pos == self.game.exit_pos: # Episode ends if exit is reached
                    break

            if training_mode:
                self.agent.decay_epsilon()
                if (episode + 1) % 10 == 0:
                    print(f"Episode {episode + 1}/{episodes} - Reward: {total_reward:.2f} - Epsilon: {self.agent.epsilon:.3f}")
            
            if self.game.request != 'CONTINUE': break
        
        if training_mode:
            self.agent.save_q_table()
            print("Training complete. Run again in 'Trained Agent' mode to see the result.")

        if self.game.request == 'CONTINUE': plt.show()
