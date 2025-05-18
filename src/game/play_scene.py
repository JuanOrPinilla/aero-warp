import json
import pygame

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import get_animation_by_angle, system_animation
from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_player, create_game_input
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_player import system_screen_player
import src.engine.game_engine

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._move_dir = pygame.Vector2(1, 0) 
        self._move_speed = 100
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        
        self._player_ent = -1
        self._paused = False

    def do_create(self):
        create_text(self.ecs_world, "Press ESC to go back", 8, 
                    pygame.Color(50, 255, 50), pygame.Vector2(320, 20), 
                    TextAlignment.CENTER)
        
        player_ent = create_player(self.ecs_world, 
                                   self.player_cfg, 
                                   self.level_cfg["player_start"])
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
                
        paused_text_ent = create_text(self.ecs_world, "PAUSE", 12, 
                                 pygame.Color(255, 50, 50), pygame.Vector2(112, 120), 
                                 TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = False 
        self._paused = False

        create_game_input(self.ecs_world)
    
    def do_update(self, delta_time: float):
        if not self._paused:
            self._p_v.vel = self._move_dir * self._move_speed
            system_screen_player(self.ecs_world, self.screen_rect)
            system_movement(self.ecs_world, delta_time)
            system_animation(self.ecs_world, delta_time)


    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        players = self.ecs_world.get_component(CTagPlayer)
        player_entity = None
        for ent, tag in players:
            player_entity = ent
            break

        if player_entity is None:
            return
        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
            return
        
        if self._paused:
            return

        if action.phase == CommandPhase.START:
            if action.name == "LEFT":
                self._move_dir = pygame.Vector2(-1, 0)
            elif action.name == "RIGHT":
                self._move_dir = pygame.Vector2(1, 0)
            elif action.name == "UP":
                self._move_dir = pygame.Vector2(0, -1)
            elif action.name == "DOWN":
                self._move_dir = pygame.Vector2(0, 1)

            # Cambiar animación según la nueva dirección
            anim = self.ecs_world.component_for_entity(player_entity, CAnimation)
            anim_name = get_animation_by_angle(self._move_dir.x, self._move_dir.y)
            set_animation(anim, anim_name)

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")
