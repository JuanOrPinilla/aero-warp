import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text, create_logo
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator 

class MenuScene(Scene):
    
    def do_create(self):
        create_text(self.ecs_world, "H1-SCORE", 8, 
                    pygame.Color(255,0,0), pygame.Vector2(112, 5), TextAlignment.CENTER)
        
        create_text(self.ecs_world, "PLAY", 8, 
                    pygame.Color(253, 201, 6), pygame.Vector2(112, 70), TextAlignment.CENTER)
        
        create_logo(self.ecs_world
            , pygame.Vector2(40, 80),
            pygame.Vector2(0,0),
            ServiceLocator.images_service.get("assets/img/game_logo.png"))

        create_text(self.ecs_world, "PRESS 'Z' TO START GAME", 8, 
                    pygame.Color(253, 201, 6), pygame.Vector2(112, 120), TextAlignment.CENTER)
        
        create_text(self.ecs_world, "TRY THIS GAME", 8, 
                    pygame.Color(255, 0, 0), pygame.Vector2(112, 135), TextAlignment.CENTER)
        
        create_text(self.ecs_world, "AERO WARP TEAM", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(112, 240), TextAlignment.CENTER)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
        
