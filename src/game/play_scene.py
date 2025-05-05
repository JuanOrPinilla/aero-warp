import json
import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_ball, create_game_input, create_paddle, create_play_field
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_ball import system_screen_ball
from src.ecs.systems.s_screen_paddle import system_screen_paddle
from src.ecs.systems.s_collision_ball_block import system_collision_ball_block
from src.ecs.systems.s_collision_paddle_ball import system_collision_paddle_ball
from src.ecs.systems.s_block_count import system_block_count
import src.engine.game_engine

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/paddle.json") as paddle_file:
            self.paddle_cfg = json.load(paddle_file)
        with open("assets/cfg/ball.json") as ball_file:
            self.ball_cfg = json.load(ball_file)
        with open("assets/cfg/blocks.json") as blocks_file:
            self.blocks_cfg = json.load(blocks_file)
        
        self._paddle_ent = -1
        self._paused = False

    def do_create(self):
        create_text(self.ecs_world, "Press ESC to go back", 8, 
                    pygame.Color(50, 255, 50), pygame.Vector2(320, 20), 
                    TextAlignment.CENTER)
        
        ball_ent = create_ball(self.ecs_world, 
                               self.ball_cfg, 
                               self.level_cfg["ball_start"])
        self._b_t = self.ecs_world.component_for_entity(ball_ent, CTransform)

        create_play_field(self.ecs_world, 
                          self.level_cfg["blocks_field"], 
                          self.blocks_cfg)
        
        paddle_ent = create_paddle(self.ecs_world, 
                                   self.paddle_cfg, 
                                   self.level_cfg["paddle_start"])
        self._p_v = self.ecs_world.component_for_entity(paddle_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(paddle_ent, CTransform)
                
        paused_text_ent = create_text(self.ecs_world, "PAUSED", 16, 
                    pygame.Color(255, 50, 50), pygame.Vector2(320, 180), 
                    TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused

        self._paused = False
        create_game_input(self.ecs_world)
    
    def do_update(self, delta_time: float):
        system_screen_paddle(self.ecs_world, self.screen_rect)
        system_screen_ball(self.ecs_world, self.screen_rect, self)
        system_block_count(self.ecs_world, self)
        
        if not self._paused:
            system_movement(self.ecs_world, delta_time)
            system_collision_ball_block(self.ecs_world, delta_time)
            system_collision_paddle_ball(self.ecs_world, self.ball_cfg["velocity"])

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if action.name == "LEFT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x -= self.paddle_cfg["input_velocity"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x += self.paddle_cfg["input_velocity"]
        elif action.name == "RIGHT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x += self.paddle_cfg["input_velocity"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x -= self.paddle_cfg["input_velocity"]

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")

        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
