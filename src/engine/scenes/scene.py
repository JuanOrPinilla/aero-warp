import pygame
import esper

from src.create.prefab_creator import create_square
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
import src.engine.game_engine


class Scene:
    def __init__(self, game_engine:'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine:src.engine.game_engine.GameEngine = game_engine
        self.screen_rect = self._game_engine.screen.get_rect()
        
        self.overlay_ent = create_square(self.ecs_world, pygame.Vector2(224, 30),
                           pygame.Color(0, 0, 0), pygame.Vector2(0, 0),
                           pygame.Vector2(0, 0))
        
        self.overlay_ent_2 = create_square(self.ecs_world, pygame.Vector2(224, 30),
                           pygame.Color(0, 0, 0), pygame.Vector2(0, 230),
                           pygame.Vector2(0, 0))

    
        
    def do_process_events(self, event:pygame.event):
        system_input(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()
    
    def switch_scene(self, new_scene_name:str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        pass

    def do_update(self, delta_time:float):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_action(self, action:CInputCommand):
        pass
    
    def get_background_color(self) -> pygame.Color:
        return pygame.Color(0, 0, 0)

    def do_clean(self):
        pass
    


