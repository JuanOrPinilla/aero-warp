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

        
