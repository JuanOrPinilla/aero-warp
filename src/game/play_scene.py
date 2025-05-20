import json
import random
import pygame

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import get_animation_by_angle, system_animation
from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_cloud_large, create_cloud_mediumA, create_cloud_mediumB, create_cloud_small, create_player, create_game_input
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
        
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
            
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
        
        self._player_ent = -1
        self._paused = False

        self._pause_blink_timer = 0.0
        self._pause_blink_interval = 0.2
        self._paused_entities = []

    def do_create(self):
        create_text(self.ecs_world, "Press ESC to go back", 8, 
                    pygame.Color(50, 255, 50), pygame.Vector2(320, 20), 
                    TextAlignment.CENTER)
        
        player_ent = create_player(self.ecs_world, 
                                   self.player_cfg, 
                                   self.level_cfg["player_start"])
        self._player_ent = player_ent
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
        
        self._cloud_ents = []
        for _ in range(50):  # 5 nubes grandes
            ent = create_cloud_large(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
            
        for _ in range(50):  # 5 nubes medianas A
            ent = create_cloud_mediumA(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        for _ in range(50):  # 5 nubes medianas B
            ent = create_cloud_mediumB(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        for _ in range(50):  # 5 nubes pequeñas
            ent = create_cloud_small(self.ecs_world, self.level_cfg, self.level_cfg["player_start"])
            self._cloud_ents.append(ent)
        
        # Si quieres guardar los CTransform para cada nube, puedes hacer algo así:
        self._cloud_transforms = [self.ecs_world.component_for_entity(e, CTransform) for e in self._cloud_ents]
                    
        paused_text_ent = create_text(self.ecs_world, "PAUSE", 12, 
                                 pygame.Color(255, 50, 50), pygame.Vector2(112, 120), 
                                 TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = False 
        self._paused = False    
        
        bg = self.level_cfg.get("bg_color")
        bg_color = pygame.Color(bg["r"], bg["g"], bg["b"])
        create_game_input(self.ecs_world)
    
    
    def do_update(self, delta_time: float):
        if self._paused:
            self._pause_blink_timer += delta_time
            if self._pause_blink_timer >= self._pause_blink_interval:
                self.p_txt_s.visible = not self.p_txt_s.visible
                self._pause_blink_timer = 0.0
            return

        # Capturar la dirección del movimiento según input
        dir_x = (-1 if self._dir_keys["LEFT"] else 0) + (1 if self._dir_keys["RIGHT"] else 0)
        dir_y = (-1 if self._dir_keys["UP"] else 0) + (1 if self._dir_keys["DOWN"] else 0)
        new_dir = pygame.Vector2(dir_x, dir_y)

        if new_dir.length_squared() > 0:
            self._move_dir = new_dir.normalize()

            # Actualizar animación del jugador según dirección
            players = self.ecs_world.get_component(CTagPlayer)
            for ent, _ in players:
                anim = self.ecs_world.component_for_entity(ent, CAnimation)
                anim_name = get_animation_by_angle(self._move_dir.x, self._move_dir.y)
                set_animation(anim, anim_name)
                break

        self._p_v.vel = self._move_dir * self._move_speed

        delta_pos = -self._p_v.vel * delta_time

        # Mover nubes
        for transform in self._cloud_transforms:
            transform.pos += delta_pos

        # Mover otros objetos del mundo 
        system_screen_player(self.ecs_world, self.screen_rect)

        # Actualizar animaciones normalmente
        system_animation(self.ecs_world, delta_time)



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

    def _generate_clouds_around_player(self):
        buffer_distance = 300 
        current_pos = self._p_t.pos

        for _ in range(5):  
            offset_x = random.uniform(-buffer_distance, buffer_distance)
            offset_y = random.uniform(-buffer_distance, buffer_distance)
            new_pos = current_pos + pygame.Vector2(offset_x, offset_y)

            if random.random() < 0.25:
                ent = create_cloud_large(self.ecs_world, self.level_cfg, {"x": new_pos.x, "y": new_pos.y})
            elif random.random() < 0.5:
                ent = create_cloud_mediumA(self.ecs_world, self.level_cfg, {"x": new_pos.x, "y": new_pos.y})
            elif random.random() < 0.75:
                ent = create_cloud_mediumB(self.ecs_world, self.level_cfg, {"x": new_pos.x, "y": new_pos.y})
            else:
                ent = create_cloud_small(self.ecs_world, self.level_cfg, {"x": new_pos.x, "y": new_pos.y})
            
            transform = self.ecs_world.component_for_entity(ent, CTransform)
            transform.pos = new_pos
            self._cloud_ents.append(ent)
            self._cloud_transforms.append(transform)

            
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
