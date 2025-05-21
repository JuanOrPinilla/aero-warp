import math
import random
import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion_state import CExplosionState
from src.ecs.components.c_health import CHealth
from src.ecs.components.c_owner import COwner
from src.ecs.components.c_enemy_shooter import CEnemyShooter
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_lifetime import CLifetime
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_boss import CTagBoss
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import  CTagPlayer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.engine.service_locator import ServiceLocator

import random


def create_player(world: esper.World, player_cfg: dict, player_start_cfg: dict):
    surf = ServiceLocator.images_service.get(player_cfg["image"])
    width, height = surf.get_size()
    frame_width = width / 32

    screen_width = 224 
    screen_height = 256

    pos = pygame.Vector2(
        (screen_width / 2) - (frame_width / 2),
        screen_height / 2
    )

    vel = pygame.Vector2(0, 0)
    player_ent = create_sprite(world, pos, vel, surf)
    world.add_component(player_ent, CTagPlayer())
    world.add_component(player_ent, CAnimation(player_cfg["animation"]))
    return player_ent

def create_bullet_square(world: esper.World, player_entity: int, bullet_info: dict, direction: pygame.Vector2):
    p_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    player_size = player_surface.area.size

    # Centro del jugador
    pos = pygame.Vector2(
        p_transform.pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
        p_transform.pos.y + (player_size[1] / 2) - (bullet_size[1] / 2)
    )

    direction = direction.normalize()
    
    offset_straight = 10
    offset_diagonal = 5

    if abs(direction.x) > 0.5 and abs(direction.y) > 0.5:
        # Disparo en diagonal
        pos.x += offset_diagonal if direction.x > 0 else -offset_diagonal
        pos.y += offset_diagonal if direction.y > 0 else -offset_diagonal
    elif abs(direction.x) > abs(direction.y):
        # Movimiento horizontal dominante
        pos.x += offset_straight if direction.x > 0 else -offset_straight
    else:
        # Movimiento vertical dominante
        pos.y += offset_straight if direction.y > 0 else -offset_straight

    vel = direction * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    world.add_component(bullet_entity, COwner(player_entity))
    ServiceLocator.sounds_service.play(bullet_info["sound"])
    return bullet_entity



def create_cloud_mediumA(world: esper.World, level_cfg: dict, player_start_cfg: dict):
    surf = ServiceLocator.images_service.get("assets/img/clouds_medium_A.png")
    screen_width = 224 * 8
    screen_height = 256 * 8

    x = random.uniform(-screen_width/2, screen_width/2)
    y = random.uniform(-screen_height/2, screen_height/2)
    pos = pygame.Vector2(x, y)

    cloud_ent = create_sprite(world, pos, pygame.Vector2(0, 0), surf)
    world.add_component(cloud_ent, CAnimation(level_cfg["animation"]))
    world.add_component(cloud_ent, CTagCloud())
    return cloud_ent

def create_cloud_mediumB(world: esper.World, level_cfg: dict, player_start_cfg: dict):
    surf = ServiceLocator.images_service.get("assets/img/clouds_medium_B.png")
    screen_width = 224 * 10
    screen_height = 256 * 10

    x = random.uniform(-screen_width/2, screen_width/2)
    y = random.uniform(-screen_height/2, screen_height/2)
    pos = pygame.Vector2(x, y)

    cloud_ent = create_sprite(world, pos, pygame.Vector2(0, 0), surf)
    world.add_component(cloud_ent, CAnimation(level_cfg["animation"]))
    world.add_component(cloud_ent, CTagCloud())
    return cloud_ent

def create_cloud_small(world: esper.World, level_cfg: dict, player_start_cfg: dict):
    surf = ServiceLocator.images_service.get("assets/img/clouds_small.png")
    screen_width = 224 * 10
    screen_height = 256 * 10

    x = random.uniform(-screen_width/2, screen_width/2)
    y = random.uniform(-screen_height/2, screen_height/2)
    pos = pygame.Vector2(x, y)

    cloud_ent = create_sprite(world, pos, pygame.Vector2(0, 0), surf)
    world.add_component(cloud_ent, CAnimation(level_cfg["animation"]))
    world.add_component(cloud_ent, CTagCloud())
    return cloud_ent

def create_cloud_large(world: esper.World, level_cfg: dict, player_start_cfg: dict):
    surf = ServiceLocator.images_service.get("assets/img/clouds_large.png")
    width, height = surf.get_size()
    frame_width = width / 32

    screen_width = 224 * 10
    screen_height = 256 * 10

    x = random.uniform(-screen_width/2, screen_width/2)
    y = random.uniform(-screen_height/2, screen_height/2)
    pos = pygame.Vector2(x, y)
    
    cloud_ent = create_sprite(world, pos, None, surf)
    world.add_component(cloud_ent, CAnimation(level_cfg["animation"]))
    world.add_component(cloud_ent, CTagCloud())
    return cloud_ent

def create_game_input(world:esper.World):
    quit_to_menu_action = world.create_entity()
    world.add_component(quit_to_menu_action,
                        CInputCommand("QUIT_TO_MENU", 
                                      pygame.K_ESCAPE))
    left_action = world.create_entity()
    world.add_component(left_action,
                        CInputCommand("LEFT", 
                                      pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action,
                        CInputCommand("RIGHT", 
                                      pygame.K_RIGHT))
    
    up_action = world.create_entity()
    world.add_component(up_action,
                        CInputCommand("UP", 
                                      pygame.K_UP))
    
    down_action = world.create_entity()
    world.add_component(down_action,
                        CInputCommand("DOWN", 
                                      pygame.K_DOWN))
    
    pause_action = world.create_entity()
    world.add_component(pause_action,
                        CInputCommand("PAUSE", 
                                      pygame.K_p))

def create_enemy(world: esper.World, enemy_cfg: dict):
    surf = ServiceLocator.images_service.get(enemy_cfg["image"])    

    screen_width = 224
    screen_height = 256
    margin = 50  

    while True:
        x = random.uniform(-margin, screen_width + margin)
        y = random.uniform(-margin, screen_height + margin)
        if x < 0 or x > screen_width or y < 0 or y > screen_height:
            break
    position = pygame.Vector2(x, y)

    target_x = random.uniform(0, screen_width)
    target_y = random.uniform(0, screen_height)
    direction = pygame.Vector2(target_x - x, target_y - y)
    if direction.length() != 0:
        direction = direction.normalize()

    min_speed = -100
    max_speed = 100
    speed = random.uniform(min_speed, max_speed)

    velocity = direction * speed

    enemy_ent = create_sprite(world, position, velocity, surf)
    world.add_component(enemy_ent, CAnimation(enemy_cfg["animation"]))
    world.add_component(enemy_ent, CTagEnemy())
    world.add_component(enemy_ent, CEnemyState(
        detection_radius=180,
        follow_speed=140,))
    world.add_component(enemy_ent, CEnemyShooter(min_interval=1.0,max_interval=3.0,))

    return enemy_ent

def create_explosion_boss(world: esper.World,
                      pos: pygame.Vector2,
                      explosion_info: dict):
     explosion_surface = ServiceLocator.images_service.get("assets\img\explosion_bullets_space_05.png")
     vel = pygame.Vector2(0, 0)

     explosion_entity = create_sprite(world, pos, vel, explosion_surface)
     world.add_component(explosion_entity, CTagExplosion())
     world.add_component(explosion_entity,
                         CAnimation(explosion_info["animations"]))
     world.add_component(explosion_entity, CExplosionState())
     return explosion_entity
 
def create_explosion(world: esper.World,
                      pos: pygame.Vector2,
                      explosion_info: dict):
     explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
     vel = pygame.Vector2(0, 0)

     explosion_entity = create_sprite(world, pos, vel, explosion_surface)
     world.add_component(explosion_entity, CTagExplosion())
     world.add_component(explosion_entity,
                         CAnimation(explosion_info["animations"]))
     world.add_component(explosion_entity, CExplosionState())
     return explosion_entity

def create_enemy_spawner(world: esper.World, level_data: dict, window_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"], window_data["size"]))
    
def create_boss(world: esper.World,
                boss_cfg: dict,
                window_size: dict) -> int:
    surf = ServiceLocator.images_service.get(boss_cfg["image"])
    w, h = surf.get_size()

    win_w, win_h = window_size["w"], window_size["h"]
    pos = pygame.Vector2((win_w - w) / 2, (win_h - h) / 2)

    boss_ent = create_sprite(world, pos, pygame.Vector2(0, 0), surf)

    world.add_component(boss_ent, CAnimation(boss_cfg["animation"]))
    world.add_component(boss_ent, CTagBoss())
    world.add_component(boss_ent, CTagEnemy())

    world.add_component(boss_ent, CHealth(boss_cfg["max_hits"]))
    world.add_component(boss_ent, CEnemyState(
         detection_radius=boss_cfg["detection_radius"],
         follow_speed    =boss_cfg["follow_speed"],
         acceleration    =boss_cfg["acceleration"],
     ))
    world.add_component(boss_ent, CEnemyShooter(
         min_interval=boss_cfg["shoot_interval"]["min"],
         max_interval=boss_cfg["shoot_interval"]["max"],))
     

    return boss_ent