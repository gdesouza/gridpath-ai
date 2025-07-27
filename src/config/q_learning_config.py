# src/config/q_learning_config.py

class QLearningConfig:
    """
    Configuration class for Q-Learning hyperparameters.
    """
    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.99
    EPSILON = 1.0
    EPSILON_DECAY_RATE = 0.001
    MIN_EPSILON = 0.01
    EPISODES = 500
    STEPS_PER_EPISODE = 200
    Q_TABLE_FILEPATH = 'data/q_table.pkl'
