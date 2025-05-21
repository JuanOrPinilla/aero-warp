import pygame

from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command   import CInputCommand
from src.engine.scenes.scene import Scene

class WinScene(Scene):
    def do_create(self):
        # 1) centra y escala fuentes según pantalla
        screen = pygame.display.get_surface()
        screen_w, screen_h = screen.get_size()
        center = pygame.Vector2(screen_w * 0.5, screen_h * 0.5)
        base_height = 256
        base_size = 8
        scale = screen_h / base_height
        title_size = 8
        small_size = max(4, int(base_size * scale))
        line_spacing = small_size * 1.5

        # 2) textos centrados
        create_text(
            self.ecs_world,
            "YOU COMPLETED THE LEVEL!",
            title_size,
            pygame.Color(  0, 200,  50),
            center + pygame.Vector2(0, -line_spacing),
            TextAlignment.CENTER
        )
        create_text(
            self.ecs_world,
            "PRESS Z TO TRY AGAIN",
            small_size,
            pygame.Color(255, 255,   0),
            center + pygame.Vector2(0, 0),
            TextAlignment.CENTER
        )
        create_text(
            self.ecs_world,
            "PRESS ESC TO GO TO MAIN MENU",
            small_size,
            pygame.Color(255, 255,   0),
            center + pygame.Vector2(0, line_spacing),
            TextAlignment.CENTER
        )

        # 3) inputs
        retry = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            retry,
            CInputCommand("RETRY_GAME", pygame.K_z)
        )
        quitm = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            quitm,
            CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE)
        )

    def do_action(self, action: CInputCommand):
        if action.name == "RETRY_GAME":
            self.switch_scene("LEVEL_01")
        elif action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")
