import esper
import pygame

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world: esper.World, screen: pygame.Surface, overlay_ent: int, text_ent: int, text_score: int,overlay_ent_2: int, kill_count:int):
    components = world.get_components(CTransform, CSurface)

    for ent, (c_t, c_s) in components:
        if ent in (overlay_ent, text_ent) or not c_s.visible:
            continue
        if world.has_component(ent, CChangingText):
            c_txt = world.component_for_entity(ent, CChangingText)
            c_s.surf = c_txt.font.render(c_txt.text, True, c_s.color)
        screen.blit(c_s.surf, c_t.pos, area=c_s.area)

    if world.entity_exists(overlay_ent):
        c_t = world.component_for_entity(overlay_ent, CTransform)
        c_s = world.component_for_entity(overlay_ent, CSurface)
        if c_s.visible:
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
            
    if world.entity_exists(overlay_ent_2):
        c_t = world.component_for_entity(overlay_ent_2, CTransform)
        c_s = world.component_for_entity(overlay_ent_2, CSurface)
        if c_s.visible:
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)

    if world.entity_exists(text_ent):
        c_t = world.component_for_entity(text_ent, CTransform)
        c_s = world.component_for_entity(text_ent, CSurface)
        if c_s.visible:
            if world.has_component(text_ent, CChangingText):
                c_txt = world.component_for_entity(text_ent, CChangingText)
                c_s.surf = c_txt.font.render(c_txt.text, True, c_s.color)
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
    
    if world.entity_exists(kill_count):
        c_t = world.component_for_entity(kill_count, CTransform)
        c_s = world.component_for_entity(kill_count, CSurface)
        if c_s.visible:
            if world.has_component(kill_count, CChangingText):
                c_txt = world.component_for_entity(kill_count, CChangingText)
                c_s.surf = c_txt.font.render(c_txt.text, True, c_s.color)
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
    
    if world.entity_exists(text_score):
        c_t = world.component_for_entity(text_score, CTransform)
        c_s = world.component_for_entity(text_score, CSurface)
        if c_s.visible:
            if world.has_component(text_score, CChangingText):
                c_txt = world.component_for_entity(text_score, CChangingText)
                c_s.surf = c_txt.font.render(c_txt.text, True, c_s.color)
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
