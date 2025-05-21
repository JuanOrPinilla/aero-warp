import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator

class GameOverScene(Scene):
    def do_create(self):
        ServiceLocator.sounds_service.play("assets\snd\player_die.ogg")
        # Obtener tamaño de pantalla actual
        screen = pygame.display.get_surface()
        screen_w, screen_h = screen.get_size()
        center = pygame.Vector2(screen_w * 0.5, screen_h * 0.5)
        base_height = 256
        base_size = 8
        scale = screen_h / base_height
        title_size = max(6, int(base_size * scale * 1.5))
        small_size = max(4, int(base_size * scale))
        third_size = max(2, int(small_size * 0.75))

        create_text(
            self.ecs_world,
            "GAME OVER",
            title_size,
            pygame.Color(255, 0, 0),
            center + pygame.Vector2(0, -small_size * 2),
            TextAlignment.CENTER
        )
        create_text(
            self.ecs_world,
            "PRESS K TO TRY AGAIN",
            small_size,
            pygame.Color(255, 255, 0),
            center + pygame.Vector2(0, 0),
            TextAlignment.CENTER
        )
        create_text(
            self.ecs_world,
            "PRESS ESC TO GO TO THE MAIN MENU",
            third_size,
            pygame.Color(255, 255, 0),
            center + pygame.Vector2(0, small_size * 2),
            TextAlignment.CENTER
        )


        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            start_game_action,
            CInputCommand("RETRY_GAME", pygame.K_k)
        )
        quit_to_menu_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            quit_to_menu_action,
            CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE)
        )

    def do_action(self, action: CInputCommand):
        if action.name == "RETRY_GAME":
            self.switch_scene("LEVEL_01")
        elif action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")