import enum
import pygame

class EnemyState(enum.Enum):
    IDLE = 0
    FOLLOW = 1

class CEnemyState:
    def __init__(self,
                 detection_radius: float = 100.0,
                 follow_speed: float = 70.0,
                 acceleration: float = 150.0):
        self.detection_radius = detection_radius
        self.follow_speed = follow_speed
        self.acceleration = acceleration
        self.state: EnemyState = EnemyState.IDLE
        self.initial_velocity: pygame.Vector2 | None = None