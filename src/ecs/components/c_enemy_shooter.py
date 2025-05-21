import random

class CEnemyShooter:
    """Gives an enemy a random‐interval fire timer."""
    def __init__(self, min_interval: float = 1.0, max_interval: float = 3.0):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.timer = random.uniform(self.min_interval, self.max_interval)

    def reset_timer(self):
        self.timer = random.uniform(self.min_interval, self.max_interval)