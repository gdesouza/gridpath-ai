# src/config/q_learning_config.py

class QLearningConfig:
    """
    Configuration class for Q-Learning hyperparameters.
    """
    LEARNING_RATE = 0.01
    DISCOUNT_FACTOR = 0.99
    EPSILON = 1.0
    EPSILON_DECAY_RATE = 0.001
    MIN_EPSILON = 0.01
    EPISODES = 1000
    STEPS_PER_EPISODE = 2000
    Q_TABLE_FILEPATH = 'data/q_table.pkl'
