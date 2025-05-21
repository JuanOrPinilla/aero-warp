import esper
import pygame
from typing import Dict

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
class IEnemyState:
    def enter(self, ent, c_state: CEnemyState, c_tr: CTransform, c_vel: CVelocity):
        pass
    def execute(self,
                ent,
                c_state: CEnemyState,
                c_tr: CTransform,
                c_vel: CVelocity,
                player_pos: pygame.Vector2,
                dt: float):
        pass
    def exit(self, ent, c_state: CEnemyState, c_tr: CTransform, c_vel: CVelocity):
        pass
class IdleState(IEnemyState):
    def enter(self, ent, c_state, c_tr, c_vel):
        pass
    def execute(self, ent, c_state, c_tr, c_vel, player_pos, dt):
        if c_tr.pos.distance_to(player_pos) <= c_state.detection_radius:
            c_state.state = EnemyState.FOLLOW
    def exit(self, ent, c_state, c_tr, c_vel):
        pass
class FollowState(IEnemyState):
    def enter(self, ent, c_state, c_tr, c_vel):
        if c_state.initial_velocity is None:
            c_state.initial_velocity = c_vel.vel.copy()
    def execute(self, ent, c_state, c_tr, c_vel, player_pos, dt):
        dist = c_tr.pos.distance_to(player_pos)
        if dist > c_state.detection_radius:
            c_state.state = EnemyState.IDLE
            return
        
        direction = (player_pos - c_tr.pos)
        if direction.length_squared() != 0:
            direction = direction.normalize()
        target_vel = direction * c_state.follow_speed
        
        delta_vel = target_vel - c_vel.vel
        max_change = c_state.acceleration * dt
        
        if delta_vel.length() > max_change:
            delta_vel = delta_vel.normalize() * max_change
        c_vel.vel += delta_vel
    def exit(self, ent, c_state, c_tr, c_vel):
        
        if c_state.initial_velocity is not None:
            c_vel.vel = c_state.initial_velocity.copy()

# mapping states
_STATE_IMPL: Dict[EnemyState, IEnemyState] = {
    EnemyState.IDLE: IdleState(),
    EnemyState.FOLLOW: FollowState(),
}
_prev_states: Dict[int, EnemyState] = {}

# system
def system_enemy_state(world: esper.World, delta_time: float):
    player_pos = None
    for _, (c_tr, _) in world.get_components(CTransform, CTagPlayer):
        player_pos = c_tr.pos
        break
    if player_pos is None:
        return

    for ent, (c_state, c_tr, c_vel) in world.get_components(CEnemyState, CTransform, CVelocity):
        if c_state.initial_velocity is None:
            c_state.initial_velocity = c_vel.vel.copy()

        prev = _prev_states.get(ent)
        curr = c_state.state
        if prev != curr:
            if prev is not None:
                _STATE_IMPL[prev].exit(ent, c_state, c_tr, c_vel)
            _STATE_IMPL[curr].enter(ent, c_state, c_tr, c_vel)
            _prev_states[ent] = curr
        _STATE_IMPL[curr].execute(ent, c_state, c_tr, c_vel, player_pos, delta_time)
