import random

from Classes.score import Score
from Classes.projectile import Projectile
from Configs.instances import *


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, size, scale, path_idle, path_defeat, frames, spawn) -> None:
        super().__init__()
        self.spawn = spawn
        self.pos_x, self.pos_y = pos
        self.size_width, self.size_height = size
        self.scale = scale
        self.current = 0
        self.idle = [pygame.image.load(f"{path_idle}{num+1}.png")
                     for num in range(frames)]
        self.defeat = [pygame.image.load(f"{path_defeat}{num+1}.png")
                     for num in range(frames)]
        self.image = self.idle[int(self.current)]
        self.image = pygame.transform.scale(
            self.image, (self.size_width*self.scale, self.size_height*self.scale))
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.angle = 0

        self.moving_left = random.choice([True, False])
        if self.moving_left:
            self.moving_right = False
        else:
            self.moving_right = True
    
        self.live = True
        self.moving_up = False
        self.moving_down = True
        self.speed = ENEMY_1_NORMAL_SPEED
        self.reload = 100
        self.life = BOSS_LIFE
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        if self.reload <= 0:
            laser_sound_boss.play()
            projectile_1 = Projectile(
                [self.pos_x, self.pos_y], BULLET_SIZE, 2, "Sprites/Projectile/Ball_2.png", BULLET_SPEED, self.angle, True, True, BULLET_LIFE, BOSS_DAMAGE)
            projectile_2 = Projectile(
                [self.pos_x, self.pos_y], BULLET_SIZE, 2, "Sprites/Projectile/Ball_2.png", BULLET_SPEED, self.angle + 180, True, True, BULLET_LIFE, BOSS_DAMAGE)
            projectile_3 = Projectile(
                [self.pos_x, self.pos_y], BULLET_SIZE, 2, "Sprites/Projectile/Ball_2.png", BULLET_SPEED, self.angle + 90, True, True, BULLET_LIFE, BOSS_DAMAGE)
            projectile_4 = Projectile(
                [self.pos_x, self.pos_y], BULLET_SIZE, 2, "Sprites/Projectile/Ball_2.png", BULLET_SPEED, self.angle + 270, True, True, BULLET_LIFE, BOSS_DAMAGE)

            bullets_enemy.add(projectile_1)
            bullets_enemy.add(projectile_2)
            bullets_enemy.add(projectile_3)
            bullets_enemy.add(projectile_4)

            sprites.add(projectile_1)
            sprites.add(projectile_2)
            sprites.add(projectile_3)
            sprites.add(projectile_4)

            self.reload = BOSS_RELOAD_TIME
        else:
            self.reload -= 1

    def colision(self) -> None:
        enemie = pygame.sprite.Group()
        enemie.add(self)
        for bullet in bullets_player:
            if pygame.sprite.spritecollide(bullet, enemie, False, pygame.sprite.collide_mask):
                if bullet.breakable:
                    bullet.kill()
                self.life -= bullet.damage

    def death(self) -> None:
        if self.life <= 0 and self.live:
            destroy_enemy_sound.play()
            self.live = False
            self.current = 0
            self.spawn.boss_spawned = False
            self.spawn.spaw_time_enemy1 = pygame.time.get_ticks()
            self.spawn.spaw_time_boss = pygame.time.get_ticks()
            for player in players:
                player.enable_ultimate()
            Score.increase_boss_score()

    def move(self) -> None:
        if self.moving_left and not self.moving_down:
            if self.pos_x - (self.size_width*self.scale/2) > 0:
                self.pos_x -= self.speed
            else:
                self.moving_right = True
                self.moving_left = False
        elif self.moving_right and not self.moving_down:
            if self.pos_x + (self.size_width*self.scale/2) < WIDTH:
                self.pos_x += self.speed
            else:
                self.moving_right = False
                self.moving_left = True

        if self.moving_down:
            if self.pos_y + (self.size_height*self.scale/2) < HEIGHT/4:
                self.pos_y += self.speed/2
            else:
                self.moving_down = False

        # ANGLE TO ROTATE
        if self.angle >= 360:
            self.angle = 0
        else:
            self.angle += (360/4/60)

    def animatio(self) -> None:
        if self.live:
            self.current += FRAME_SPEED
            if self.current >= len(self.idle):
                self.current = 0

            self.image = self.idle[int(self.current)]
            self.image = pygame.transform.scale(
                self.image, (self.size_width*self.scale, self.size_height*self.scale))
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.current += FRAME_SPEED
            if self.current >= len(self.defeat):
                self.kill()
            else:
                self.image = self.defeat[int(self.current)]
                self.image = pygame.transform.scale(
                    self.image, (self.size_width*self.scale, self.size_height*self.scale))
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
                self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.animatio()
        self.colision()
        self.move()
        self.shoot()
        self.death()
