import random

from Classes.enemy import Enemy
from Classes.boss import Boss
from Classes.player import Player
from Classes.score import Score
from Configs.instances import *


# Spawn system
class Spawn:
    def __init__(self) -> None:
        self.player_spawned = False
        self.boss_spawned = False
        self.spawn_cooldown_enemy = 3000
        self.spawn_cooldown_boss = 30000
        self.spaw_time_enemy1 = pygame.time.get_ticks()
        self.spaw_time_boss = pygame.time.get_ticks()
        self.spawned_enemies = []

    def spawn_enemies_type_1(self) -> None:
        if pygame.time.get_ticks() - self.spaw_time_enemy1 > self.spawn_cooldown_enemy and self.boss_spawned == False and len(self.spawned_enemies) < 10:
            enemy = Enemy([random.randint(0, WIDTH), ENEMY_1_START_POSITION_Y], ENEMY_1_SIZE, ENEMY_1_SCALE,
                          "Sprites/Enemies/Type_1/Idle/Idle_", "Sprites/Enemies/Type_1/Die/Die_", 6)
            self.spaw_time_enemy1 = pygame.time.get_ticks()
            self.spawned_enemies.append(enemy)
            enemies.add(enemy)
            sprites.add(enemy)

    def spawn_boss(self) -> None:
        if pygame.time.get_ticks() - self.spaw_time_boss > self.spawn_cooldown_boss and self.boss_spawned == False and Score.score_normal_enemy > 0 and Score.score_normal_enemy % 1000 == 0:
            self.boss_spawned = True
            boss = Boss(BOSS_START_POSITION, BOSS_SIZE, BOSS_SCALE,
                        "Sprites/Enemies/Boss/Idle/Idle_", "Sprites/Enemies/Boss/Die/Die_", 8, self)
            self.spawned_enemies = []
            enemies.add(boss)
            sprites.add(boss)

    def spawn_player(self) -> None:
        if self.player_spawned == False:
            self.player_spawned = True
            player = Player(PLAYER_START_POSITION, PLAYER_SIZE,
                            PLAYER_SCALE, "Sprites/Player/Idle/Idle_", "Sprites/Player/Power/Power_", "Sprites/Player/Die/Die_", 8)
            players.add(player)
            sprites.add(player)

    def update(self) -> None:
        self.spawn_player()
        self.spawn_enemies_type_1()
        self.spawn_boss()
