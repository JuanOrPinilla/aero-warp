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
                 follow_speed: float = 120.0):
        self.detection_radius = detection_radius
        self.follow_speed = follow_speed
        self.state: EnemyState = EnemyState.IDLE
        self.initial_velocity: pygame.Vector2 | None = None