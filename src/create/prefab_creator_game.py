import math
import random
import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import  CTagPlayer
from src.engine.service_locator import ServiceLocator

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
    print(pos)

    vel = pygame.Vector2(0, 0)
    player_ent = create_sprite(world, pos, vel, surf)
    world.add_component(player_ent, CTagPlayer())
    world.add_component(player_ent, CAnimation(player_cfg["animation"]))
    return player_ent


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
    