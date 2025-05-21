import random
import pygame
import esper

from src.ecs.components.c_enemy_shooter import CEnemyShooter
from src.ecs.components.c_velocity import CVelocity
from src.create.prefab_creator_game import create_bullet_square

def system_enemy_shoot(world: esper.World, bullet_cfg: dict, delta_time: float):
    for ent, (shooter, vel) in world.get_components(CEnemyShooter, CVelocity):
        shooter.timer -= delta_time
        if shooter.timer <= 0:
            if vel.vel.length_squared() > 0:
                create_bullet_square(world, ent, bullet_cfg, vel.vel.normalize())
            shooter.reset_timer()