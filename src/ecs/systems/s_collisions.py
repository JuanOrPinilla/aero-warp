import pygame
import esper

from src.ecs.components.c_dead import CDead
from src.ecs.components.c_health import CHealth
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_boss import CTagBoss
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
    
    bosses = []
    for ent, (_tag, tr, surf, health) in world.get_components(
        CTagBoss, CTransform, CSurface, CHealth
    ):
        bosses.append((ent,
                       pygame.Rect(tr.pos.x, tr.pos.y,
                                   surf.area.w, surf.area.h),
                       health))

    for bullet_ent, (_, b_tr, b_surf, owner) in world.get_components(
        CTagBullet, CTransform, CSurface, COwner):

        b_rect = pygame.Rect(
            b_tr.pos.x, b_tr.pos.y,
            b_surf.area.w, b_surf.area.h
        )

        hit_boss = False
        for boss_ent, boss_rect, health in bosses:
            if owner.owner == boss_ent:
                continue
            if b_rect.colliderect(boss_rect):
                hit_boss = True
                # descontar vida
                health.hits_remaining -= 1
                # siempre borramos la bala
                world.delete_entity(bullet_ent)

                if health.hits_remaining <= 0:
                    # explota y muere el boss
                    create_explosion(world,
                                     pygame.Vector2(boss_rect.center),
                                     explosion_cfg)
                    world.delete_entity(boss_ent)
                break
        
        if hit_boss:
            continue

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

        for player_ent, p_rect in players:
            if owner.owner == player_ent:
                continue
            if b_rect.colliderect(p_rect):
                center = pygame.Vector2(p_rect.center)
                ServiceLocator.sounds_service.play(explosion_cfg.get("sound", ""))
                create_explosion(world, center, explosion_cfg)
                world.delete_entity(bullet_ent)
                world.add_component(player_ent, CDead())
                break
    