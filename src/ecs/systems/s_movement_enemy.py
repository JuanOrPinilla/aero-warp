import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_movement_enemy(world:esper.World, delta_time:float):
    components = world.get_components(CTransform, CVelocity, CTagEnemy)
    for _, (c_t, c_v, c_b) in components:
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time