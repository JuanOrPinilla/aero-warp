# src/ecs/components/c_enemy_state.py
from __future__ import annotations
from abc import ABC, abstractmethod
import pygame


class EnemyState(ABC):
    """Interface for every concrete state."""

    @abstractmethod
    def enter(self, enemy_ai: "CEnemyState"):
        ...

    @abstractmethod
    def update(
        self,
        enemy_ai: "CEnemyState",
        enemy_pos: pygame.Vector2,
        player_pos: pygame.Vector2,
        c_vel,               # CVelocity component
        delta_time: float,
    ):
        ...

    @abstractmethod
    def exit(self, enemy_ai: "CEnemyState"):
        ...


# --------------------------------------------------------------------------- #
# Concrete states
# --------------------------------------------------------------------------- #
class IdleState(EnemyState):
    def enter(self, enemy_ai):
        # stop any residual movement
        enemy_ai.idle_velocity *= 0

    def update(self, enemy_ai, enemy_pos, player_pos, c_vel, dt):
        if enemy_pos.distance_to(player_pos) <= enemy_ai.detection_radius:
            enemy_ai.change_state(FollowState())
            return
        # stay still
        c_vel.vx = c_vel.vy = 0

    def exit(self, enemy_ai):
        pass


class FollowState(EnemyState):
    def enter(self, enemy_ai):
        pass  # nothing special

    def update(self, enemy_ai, enemy_pos, player_pos, c_vel, dt):
        # move toward player
        direction = (player_pos - enemy_pos)
        if direction.length_squared() != 0:
            direction = direction.normalize()

        c_vel.vx = direction.x * enemy_ai.follow_speed
        c_vel.vy = direction.y * enemy_ai.follow_speed

        # lost sight?
        if enemy_pos.distance_to(player_pos) > enemy_ai.detection_radius:
            enemy_ai.change_state(IdleState())

    def exit(self, enemy_ai):
        pass


# --------------------------------------------------------------------------- #
# Component that carries the current state and parameters
# --------------------------------------------------------------------------- #
class CEnemyState:
    def __init__(self, detection_radius: float = 200.0, follow_speed: float = 120.0):
        self.detection_radius = detection_radius
        self.follow_speed = follow_speed
        self.state: EnemyState = IdleState()  # start idle

        # helpers so states can tweak velocity without circular imports
        self.idle_velocity = pygame.Vector2(0, 0)

    # ------------- API called by the system ------------- #
    def change_state(self, new_state: EnemyState):
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def update(self, enemy_pos, player_pos, c_vel, dt):
        self.state.update(self, enemy_pos, player_pos, c_vel, dt)
