import pygame
import esper

from src.ecs.components.c_dead import CDead
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_owner import COwner
from src.create.prefab_creator_game import create_explosion
from src.engine.service_locator import ServiceLocator

def system_bullet_collision(world: esper.World,
                            explosion_cfg: dict):

    players = []
    for ent, (_, tr, surf) in world.get_components(CTagPlayer, CTransform, CSurface):
        rect = pygame.Rect(tr.pos.x, tr.pos.y, surf.area.w, surf.area.h)
        players.append((ent, rect))

    enemies = []
    for ent, (_, tr, surf) in world.get_components(CTagEnemy, CTransform, CSurface):
        rect = pygame.Rect(tr.pos.x, tr.pos.y, surf.area.w, surf.area.h)
        enemies.append((ent, rect))

    for bullet_ent, (_, b_tr, b_surf, owner) in world.get_components(
        CTagBullet, CTransform, CSurface, COwner):

        b_rect = pygame.Rect(
            b_tr.pos.x, b_tr.pos.y,
            b_surf.area.w, b_surf.area.h
        )
        hit_something = False
        for enemy_ent, e_rect in enemies:
            if owner.owner == enemy_ent:
                continue
            if b_rect.colliderect(e_rect):
                # explosion & delete
                center = pygame.Vector2(e_rect.center)
                ServiceLocator.sounds_service.play(explosion_cfg.get("sound", ""))
                create_explosion(world, center, explosion_cfg)
                world.delete_entity(enemy_ent)
                world.delete_entity(bullet_ent)
                world.contador += 1
                world.score   += 100
                hit_something = True
                break

        if hit_something:
            continue

        # if no enemy was hit, try the player
        for player_ent, p_rect in players:
            if owner.owner == player_ent:
                continue
            if b_rect.colliderect(p_rect):
                center = pygame.Vector2(p_rect.center)
                ServiceLocator.sounds_service.play(explosion_cfg.get("sound", ""))
                create_explosion(world, center, explosion_cfg)
                world.delete_entity(bullet_ent)
                # mark player dead
                world.add_component(player_ent, CDead())
                break
    