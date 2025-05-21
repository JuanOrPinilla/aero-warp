import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import get_animation_by_angle

def system_enemy_animation(world: esper.World, delta_time: float):
    for ent, (surf_c, anim_c, vel_c) in world.get_components(CSurface, CAnimation, CVelocity):
        desired_anim = get_animation_by_angle(vel_c.vel.x, vel_c.vel.y)
        idx = next(
            (i for i, a in enumerate(anim_c.animations_list) if a.name == desired_anim),
            None
        )
        if idx is None:
            continue

        if anim_c.curr_anim != idx:
            anim_c.curr_anim      = idx
            anim_data              = anim_c.animations_list[idx]
            anim_c.curr_frame     = anim_data.start
            anim_c.curr_anim_time = anim_data.framerate

        anim_c.curr_anim_time -= delta_time
        if anim_c.curr_anim_time <= 0:
            anim_data = anim_c.animations_list[anim_c.curr_anim]
            anim_c.curr_frame += 1
            if anim_c.curr_frame > anim_data.end:
                anim_c.curr_frame = anim_data.start
            anim_c.curr_anim_time += anim_data.framerate

        full_rect    = surf_c.surf.get_rect()
        frame_width  = full_rect.w / anim_c.number_frames
        surf_c.area.w = frame_width
        surf_c.area.x = frame_width * anim_c.curr_frame
