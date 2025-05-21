# src/ecs/systems/s_lifetime.py
import esper
from src.ecs.components.c_lifetime import CLifetime
from src.ecs.components.c_surface  import CSurface

def system_lifetime(world: esper.World, delta_time: float):
    """
    Decrements CLifetime.remaining and, when it hits zero,
    hides the entity’s surface (or you could delete it).
    """
    for ent, (lt, surf) in world.get_components(CLifetime, CSurface):
        lt.remaining -= delta_time
        if lt.remaining <= 0:
            surf.visible = False
