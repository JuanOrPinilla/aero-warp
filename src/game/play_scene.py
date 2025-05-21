import json
import random
import pygame

from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import get_animation_by_angle, system_animation
from src.ecs.systems.s_collisions import system_bullet_collision
from src.ecs.systems.s_enemy_animation import system_enemy_animation
from src.ecs.systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.s_explosion_state import system_explosion_state
from src.ecs.systems.s_killcount import update_kill_count_text, update_score_text
from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_bullet_square, create_cloud_large, create_cloud_mediumA, create_cloud_mediumB, create_cloud_small, create_enemy_spawner, create_player, create_game_input, create_enemy
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement_bullet import system_movement_bullet
from src.ecs.systems.s_movement_enemy import system_movement_enemy
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_lifetime import system_lifetime
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open('assets/cfg/bullet.json','r') as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open('assets/cfg/explosion.json','r') as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
            
        color = self.level_cfg["bg_color"]
        self._bg_color = pygame.Color(color["r"], color["g"], color["b"])
        self._move_dir = pygame.Vector2(0, -1) 
        self._move_speed = 100
        
        self._dir_keys = {
            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False
        }
        
        self._shoot_timer = 0.0
        self._shoot_interval = 0.2 

        self._player_ent = -1
        self._paused = False

        self._pause_blink_timer = 0.0
        self._pause_blink_interval = 0.2
        self._paused_entities = []
        self.ecs_world.contador = 0
        self.ecs_world.score = 0

    def do_create(self):
        create_text(self.ecs_world, "Press ESC to go back", 8, 
                    pygame.Color(50, 255, 50), pygame.Vector2(320, 20), 
                    TextAlignment.CENTER)
    
        
        
        create_text(self.ecs_world, "PLAYER 1", 8, 
                    pygame.Color(3,53,0), pygame.Vector2(110, 115), TextAlignment.CENTER, 2)
        
        create_text(self.ecs_world, "A.D. 1999", 8, 
                    pygame.Color(3,53,0), pygame.Vector2(110, 150), TextAlignment.CENTER, 2)
        
        player_ent = create_player(self.ecs_world, 
                                   self.player_cfg, 
                                   self.level_cfg["player_start"])
        self._player_ent = player_ent
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
        
        self._cloud_ents = []
        for _ in range(200):
            ent = create_cloud_large(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
            
        for _ in range(150): 
            ent = create_cloud_mediumA(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        for _ in range(150):
            ent = create_cloud_mediumB(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        for _ in range(100):
            ent = create_cloud_small(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        self._cloud_transforms = [
            self.ecs_world.component_for_entity(e, CTransform)
            for e in self._cloud_ents
            if self.ecs_world.has_component(e, CTagCloud)
            ]
                    
        paused_text_ent = create_text(self.ecs_world, "PAUSE", 12, 
                                 pygame.Color(255, 50, 50), pygame.Vector2(112, 120), 
                                 TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = False 
        self._paused = False    
        
        bg = self.level_cfg.get("bg_color")
        bg_color = pygame.Color(bg["r"], bg["g"], bg["b"])
        create_enemy_spawner(self.ecs_world, self.level_cfg, self.window_cfg)
        create_game_input(self.ecs_world)
        

        
        self.overlay_ent = create_square(self.ecs_world, pygame.Vector2(224, 30),
                           pygame.Color(0, 0, 0), pygame.Vector2(0, 0),
                           pygame.Vector2(0, 0))
        
        self.overlay_ent_2 = create_square(self.ecs_world, pygame.Vector2(224, 30),
                           pygame.Color(0, 0, 0), pygame.Vector2(0, 230),
                           pygame.Vector2(0, 0))


        self.kill_count = create_text(self.ecs_world, "00", 8,
                            pygame.Color(255, 255, 255), pygame.Vector2(30, 238),
                            TextAlignment.CENTER)
        
        self.ent_text = create_text(self.ecs_world, "H1-SCORE", 8,
                            pygame.Color(255, 0, 0), pygame.Vector2(112, 5),
                            TextAlignment.CENTER)
        
        self.ent_score = create_text(self.ecs_world, "00000", 8,
                            pygame.Color(255, 255, 255), pygame.Vector2(112, 15),
                            TextAlignment.CENTER)
        
        
    
    
    def do_update(self, delta_time: float):
        if self._paused:
            self._pause_blink_timer += delta_time
            if self._pause_blink_timer >= self._pause_blink_interval:
                self.p_txt_s.visible = not self.p_txt_s.visible
                self._pause_blink_timer = 0.0
            return

        dir_x = (-1 if self._dir_keys["LEFT"] else 0) + (1 if self._dir_keys["RIGHT"] else 0)
        dir_y = (-1 if self._dir_keys["UP"] else 0) + (1 if self._dir_keys["DOWN"] else 0)
        new_dir = pygame.Vector2(dir_x, dir_y)

        if new_dir.length_squared() > 0:
            self._move_dir = new_dir.normalize()

            players = self.ecs_world.get_component(CTagPlayer)
            for ent, _ in players:
                anim = self.ecs_world.component_for_entity(ent, CAnimation)
                anim_name = get_animation_by_angle(self._move_dir.x, self._move_dir.y)
                break

        self._p_v.vel = self._move_dir * self._move_speed
        delta_pos = -self._p_v.vel * delta_time

        for transform in self._cloud_transforms:
            transform.pos += delta_pos

        system_enemy_spawner(self.ecs_world, self.enemies_cfg, delta_time)
        system_bullet_collision(self.ecs_world, self.explosion_cfg)
        system_explosion_state(self.ecs_world, delta_time)
        system_screen_player(self.ecs_world, self.screen_rect)

        system_animation(self.ecs_world, delta_time)

        system_enemy_animation(self.ecs_world, delta_time)
        
        enemies = self.ecs_world.get_component(CTagEnemy)
        for ent, _ in enemies:
            if self.ecs_world.has_component(ent, CTransform):
                transform = self.ecs_world.component_for_entity(ent, CTransform)
                transform.pos += delta_pos
        
        bullets = self.ecs_world.get_component(CTagBullet)
        
        for ent, _ in bullets:
            if self.ecs_world.has_component(ent, CTransform):
                transform = self.ecs_world.component_for_entity(ent, CTransform)
                transform.pos += delta_pos
        explosions = self.ecs_world.get_component(CTagExplosion)
        
        for ent, _ in explosions:
            if self.ecs_world.has_component(ent, CTransform):
                transform = self.ecs_world.component_for_entity(ent, CTransform)
                transform.pos += delta_pos
        
        self._shoot_timer += delta_time
        if self._shoot_timer >= self._shoot_interval:
            self._shoot_timer = 0.0
            active_bullets = len(self.ecs_world.get_components(CTagBullet))
            if self._move_dir.length_squared() > 0:
                create_bullet_square(self.ecs_world, self._player_ent, self.bullet_cfg, self._move_dir)
        system_movement_bullet(self.ecs_world, delta_time)
        system_movement_enemy(self.ecs_world, delta_time)
        system_enemy_state(self.ecs_world, delta_time)
        system_enemy_shoot(self.ecs_world, self.bullet_cfg, delta_time)
        system_lifetime(self.ecs_world, delta_time)
        update_kill_count_text(self)
        update_score_text(self)

    

    def do_clean(self):
        self._paused = False

    def _set_entities_visibility(self, visible: bool):
        """Oculta o muestra todos los CSurface excepto el botón de pausa"""
        self._paused_entities = []
        for ent, surface in self.ecs_world.get_component(CSurface):
            if surface is not self.p_txt_s:
                surface.visible = visible
                if not visible:
                    self._paused_entities.append(ent)
            
    def do_action(self, action: CInputCommand):
        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
            self._set_entities_visibility(not self._paused)
            return
        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")
            return

        if action.name in self._dir_keys:
            if action.phase == CommandPhase.START:
                self._dir_keys[action.name] = True
            elif action.phase == CommandPhase.END:
                self._dir_keys[action.name] = False
                
    def get_background_color(self) -> pygame.Color:
        return self._bg_color
    