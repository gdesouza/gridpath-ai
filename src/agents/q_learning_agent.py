import numpy as np
import random
import os
import pickle

class QLearningAgent:
    """
    Implements a Q-Learning agent for reinforcement learning.

    Attributes:
        q_table (dict): Stores Q-values for state-action pairs.
        learning_rate (float): The step size for updating Q-values.
        discount_factor (float): The factor by which future rewards are discounted.
        epsilon (float): The probability of choosing a random action (exploration).
        epsilon_decay_rate (float): The rate at which epsilon decays over episodes.
        min_epsilon (float): The minimum value epsilon can reach.
        actions (list): A list of possible actions the agent can take.
        q_table_filepath (str): The file path to save/load the Q-table.
    """
    def __init__(self, actions: list, q_table_filepath='q_table.pkl'):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.epsilon = 1.0
        self.epsilon_decay_rate = 0.001
        self.min_epsilon = 0.01
        self.actions = actions
        self.q_table_filepath = q_table_filepath

    def get_q_value(self, state, action):
        """Retrieves the Q-value for a given state-action pair."""
        return self.q_table.get((state, action), 0.0)

    def get_action(self, state):
        """
        Selects an action based on the epsilon-greedy policy.

        Args:
            state: The current state of the environment.

        Returns:
            An action chosen by the agent.
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions) # Explore
        else:
            # Exploit: choose action with the highest Q-value
            q_values = [self.get_q_value(state, action) for action in self.actions]
            max_q = max(q_values)
            # Handle ties by choosing randomly among actions with max Q-value
            best_actions = [self.actions[i] for i, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state):
        """
        Updates the Q-value for a state-action pair using the Q-Learning formula.

        Args:
            state: The current state.
            action: The action taken.
            reward: The reward received.
            next_state: The state after taking the action.
        """
        current_q = self.get_q_value(state, action)
        
        # Max Q-value for the next state
        next_q_values = [self.get_q_value(next_state, a) for a in self.actions]
        max_next_q = max(next_q_values) if next_q_values else 0.0

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def decay_epsilon(self):
        """Decays the epsilon value to reduce exploration over time."""
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay_rate)

    def save_q_table(self):
        """Saves the Q-table to a file."""
        os.makedirs(os.path.dirname(self.q_table_filepath), exist_ok=True)
        with open(self.q_table_filepath, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Q-table saved to {self.q_table_filepath}")

    def load_q_table(self):
        """Loads the Q-table from a file."""
        if os.path.exists(self.q_table_filepath):
            with open(self.q_table_filepath, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Q-table loaded from {self.q_table_filepath}")
        else:
            raise FileNotFoundError(f"Q-table file not found at {self.q_table_filepath}")
