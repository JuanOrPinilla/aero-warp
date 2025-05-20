import pygame
import json
import random

class CEnemySpawner:
    def __init__(self, spawn_events_data:dict, info_pantalla:dict) -> None:
        self.current_time:float = 0
        self.spawn_event_data:list[SpawnEventData] = []
        for single_event in spawn_events_data:
            self.spawn_event_data.append(SpawnEventData(single_event, info_pantalla))

class SpawnEventData:
    def __init__(self, event_data:dict, info_pantalla:dict) -> None:
        self.time:float = event_data["time"]
        self.enemy_type:str = event_data["enemy_type"]

        # Posicion random dentro de la pantalla
        screen_width, screen_height = info_pantalla["w"], info_pantalla["h"]
        self.position: pygame.Vector2 = pygame.Vector2(
            random.randint(0, screen_width),
            random.randint(0, screen_height)
        )

        self.triggered = False