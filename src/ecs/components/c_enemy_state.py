import enum
import pygame

class EnemyState(enum.Enum):
    """Possible AI states for enemies."""
    IDLE = 0
    FOLLOW = 1

class CEnemyState:
    """Data component: holds AI parameters and current state and initial velocity."""
    def __init__(self,
                 detection_radius: float = 200.0,
                 follow_speed: float = 120.0,
                 acceleration: float = 300.0):
        # distance to trigger follow
        self.detection_radius = detection_radius
        # max chase speed
        self.follow_speed = follow_speed
        # maximum change in velocity per second
        self.acceleration = acceleration
        # current AI state
        self.state: EnemyState = EnemyState.IDLE
        # record initial spawn velocity to resume after chase
        self.initial_velocity: pygame.Vector2 | None = None