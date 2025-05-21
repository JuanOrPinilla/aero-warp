import pygame
from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# STATE INTERFACE
# ---------------------------------------------------------------------------
class EnemyState(ABC):
    """Abstract base for every concrete enemy state."""

    @abstractmethod
    def enter(self, ctx: "CEnemyState", c_vel: "CVelocity"):
        ...

    @abstractmethod
    def update(self,
               ctx: "CEnemyState",
               enemy_pos: pygame.Vector2,
               player_pos: pygame.Vector2,
               c_vel: "CVelocity",
               dt: float):
        ...

    @abstractmethod
    def exit(self, ctx: "CEnemyState", c_vel: "CVelocity"):
        ...

# ---------------------------------------------------------------------------
# CONCRETE STATES
# ---------------------------------------------------------------------------
class IdleState(EnemyState):
    """Enemy stands still."""

    def enter(self, ctx, c_vel):
        c_vel.vel.update(0, 0)

    def update(self, ctx, enemy_pos, player_pos, c_vel, dt):
        if enemy_pos.distance_to(player_pos) <= ctx.detection_radius:
            ctx.change_state(FollowState(), c_vel)
        # keep velocity zero
        c_vel.vel.update(0, 0)

    def exit(self, ctx, c_vel):
        pass


class FollowState(EnemyState):
    """Enemy moves toward the player."""

    def enter(self, ctx, c_vel):
        pass

    def update(self, ctx, enemy_pos, player_pos, c_vel, dt):
        # direction toward player
        direction = player_pos - enemy_pos
        if direction.length_squared():
            direction = direction.normalize()
        c_vel.vel = direction * ctx.follow_speed

        if enemy_pos.distance_to(player_pos) > ctx.detection_radius:
            ctx.change_state(IdleState(), c_vel)

    def exit(self, ctx, c_vel):
        pass

# ---------------------------------------------------------------------------
# COMPONENT THAT CARRIES THE CURRENT STATE
# ---------------------------------------------------------------------------
class CEnemyState:
    """Attach to an enemy entity; handles its finite state machine."""

    def __init__(self, detection_radius: float = 180.0, follow_speed: float = 140.0):
        self.detection_radius = detection_radius
        self.follow_speed = follow_speed
        self.state: EnemyState = IdleState()  # initial

    # --------------------------------------------------
    # API used by system
    # --------------------------------------------------
    def change_state(self, new_state: EnemyState, c_vel):
        self.state.exit(self, c_vel)
        self.state = new_state
        self.state.enter(self, c_vel)

    def update(self, enemy_pos, player_pos, c_vel, dt):
        self.state.update(self, enemy_pos, player_pos, c_vel, dt)
