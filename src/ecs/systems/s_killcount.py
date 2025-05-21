
import pygame
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def update_kill_count_text(self):
        texto = f"{self.ecs_world.contador:02}"
        c_surface = self.ecs_world.component_for_entity(self.kill_count, CSurface)
        font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
        c_surface.surf = font.render(texto, True, pygame.Color(255, 255, 255))
        c_surface.area = c_surface.surf.get_rect()

def update_score_text(self):
        texto = f"{self.ecs_world.score:05}"
        c_surface = self.ecs_world.component_for_entity(self.ent_score, CSurface)
        font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
        c_surface.surf = font.render(texto, True, pygame.Color(255, 255, 255))
        c_surface.area = c_surface.surf.get_rect()
