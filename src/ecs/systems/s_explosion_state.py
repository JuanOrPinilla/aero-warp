import pygame
import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_explosion_state import CExplosionState, ExplosionState

def system_explosion_state(world: esper.World, delta_time: float):
    components = world.get_components(CSurface, CAnimation, CExplosionState, CTagExplosion)

    for entity, (c_s, c_a, c_es, _) in components:
        if c_es.state == ExplosionState.EXPLODE:
            _do_explode(entity, c_s, c_a, c_es,world, delta_time)

def _do_explode(entity: int, c_s: CSurface, c_a: CAnimation, 
                c_es: CExplosionState, world: esper.World, delta_time: float):

    c_a.curr_anim_time -= delta_time
    if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
            world.delete_entity(entity)