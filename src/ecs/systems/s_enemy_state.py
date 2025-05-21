# src/game/systems/system_enemy_state.py
import esper
import pygame

from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_transform import CTransform          # holds .pos : Vector2
from src.ecs.components.c_velocity   import CVelocity          # holds .vx, .vy


def system_enemy_state(world: esper.World, player_ent: int, delta_time: float):
    """
    • `player_ent`  – entity id of the player (so we can grab its position)
    • must be called every frame
    """
    c_player_pos: pygame.Vector2 = world.component_for_entity(player_ent, CTransform).pos

    # iterate every enemy that owns an AI state, a position and a velocity
    for _, (c_state, c_tr, c_vel) in world.get_components(
        CEnemyState, CTransform, CVelocity
    ):
        c_state.update(c_tr.pos, c_player_pos, c_vel, delta_time)
