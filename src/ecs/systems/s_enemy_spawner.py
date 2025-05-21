import esper
from src.create.prefab_creator_game import create_enemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def system_enemy_spawner(world: esper.World, enemies_data: dict, delta_time: float):
    for _, spawner in world.get_component(CEnemySpawner):
        for evt in spawner.spawn_event_data:
            evt._time_until_spawn -= delta_time

            if evt._time_until_spawn <= 0:
                create_enemy(
                    world,
                    enemies_data[evt.enemy_type],
                    evt.position,
                    evt.velocity
                )
                print("deberia spawnear porque soy una neaaaa")
                evt._time_until_spawn = evt.spawn_interval
