import pygame
import random

class CEnemySpawner:
    def __init__(self, spawn_events_data: dict, info_pantalla: dict) -> None:
        self.current_time: float = 0
        self.spawn_event_data: list[SpawnEventData] = []
        for single_event in spawn_events_data:
            self.spawn_event_data.append(SpawnEventData(single_event, info_pantalla))

class SpawnEventData:
    def __init__(self, event_data: dict, info_pantalla: dict) -> None:
        self.spawn_interval: float = event_data["time"]
        self._time_until_spawn: float = self.spawn_interval
        self.enemy_type: str = event_data["enemy_type"]

        screen_width = info_pantalla["w"]
        screen_height = info_pantalla["h"]
        margin = 50  # pixels; adjust as needed

        while True:
            x = random.uniform(-margin, screen_width + margin)
            y = random.uniform(-margin, screen_height + margin)
            if x < 0 or x > screen_width or y < 0 or y > screen_height:
                break
        #TODO:NIGGER
        self.position = pygame.Vector2(0, 0)

        target_x = random.uniform(0, screen_width)
        target_y = random.uniform(0, screen_height)
        direction = pygame.Vector2(target_x - x, target_y - y)
        if direction.length() != 0:
            direction = direction.normalize()

        min_speed = 5
        max_speed = 20
        speed = random.uniform(min_speed, max_speed)

        self.velocity = direction * speed
