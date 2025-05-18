import pygame
import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_screen_player(world: esper.World, screen_rect: pygame.Rect):
    components = world.get_components(CTransform, CSurface, CTagPlayer, CAnimation)
    for _, (c_t, c_s, _, c_a) in components:
        total_width, total_height = c_s.surf.get_size()
        
        frame_width = total_width / c_a.number_frames 
        frame_height = total_height 
        
        c_s.area.w = frame_width
        c_s.area.h = frame_height
        c_s.area.x = frame_width * c_a.curr_frame
        c_s.area.y = 0 
        
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        if not screen_rect.contains(player_rect):
            player_rect.clamp_ip(screen_rect)
            c_t.pos.x = player_rect.x
            c_t.pos.y = player_rect.y
