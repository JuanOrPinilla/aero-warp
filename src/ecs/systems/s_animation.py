import math
import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)
    for _, (c_s, c_a) in components:
        # Dimsinuir el valor de curr_time de la nimacion
        c_a.curr_anim_time -= delta_time
        # Cuando curr_imte <= 0
        if c_a.curr_anim_time <= 0:
            # RESTAURAR EL TIEMPO
            c_a.curr_frame += 1
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            # Limitar el frame con sus propiedad de start y end
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
            # Calcular la nueva subarea del rectangulo de sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame
            
def get_animation_by_angle(vel_x, vel_y):
    if vel_x == 0 and vel_y == 0:
        return "IDLE"

    angle = math.degrees(math.atan2(-vel_y, vel_x)) 
    if angle < 0:
        angle += 360

    directions = [
        ("MOVE_RIGHT", 0),
        ("MOVE_UP_RIGHT", 45),
        ("MOVE_UP", 90),
        ("MOVE_UP_LEFT", 135),
        ("MOVE_LEFT", 180),
        ("MOVE_DOWN_LEFT", 225),
        ("MOVE_DOWN", 270),
        ("MOVE_DOWN_RIGHT", 315),
    ]

    # Encuentra la animación con el ángulo más cercano
    closest_anim = None
    closest_diff = 360
    for anim_name, anim_angle in directions:
        diff = abs(angle - anim_angle)
        diff = min(diff, 360 - diff)  # diferencia mínima en círculo
        if diff < closest_diff:
            closest_diff = diff
            closest_anim = anim_name

    return closest_anim
