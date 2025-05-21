from enum import Enum
import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment, duration: float | None = None) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    
    if duration is not None:
        from src.ecs.components.c_lifetime import CLifetime
        world.add_component(text_entity, CLifetime(duration))
        
    return text_entity

def create_logo(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    logo_ent = world.create_entity()
    logo_ent = create_sprite(world, pos, vel, surface) 
    return logo_ent

