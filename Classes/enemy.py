import random

from Classes.score import Score
from Classes.projectile import Projectile
from Configs.instances import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, scale, path_idle, path_defeat, frames) -> None:
        super().__init__()
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
        self.spawn_time = pygame.time.get_ticks()

        self.moving_left = random.choice([True, False])
        if self.moving_left:
            self.moving_right = False
        else:
            self.moving_right = True

        self.live = True
        self.moving_up = False
        self.moving_down = True
        self.speed = ENEMY_1_NORMAL_SPEED
        self.reload = 80
        self.life = ENEMY_1_LIFE
        self.mask = pygame.mask.from_surface(self.image)

    def move(self) -> None:
        if self.moving_left:
            if self.pos_x - (self.size_width*self.scale/2) > -100:
                self.pos_x -= self.speed
            else:
                self.moving_right = True
                self.moving_left = False
        elif self.moving_right:
            if self.pos_x + (self.size_width*self.scale/2) < WIDTH + 100:
                self.pos_x += self.speed
            else:
                self.moving_right = False
                self.moving_left = True

        if self.moving_up:
            if self.pos_y - (self.size_height*self.scale/2) > 0:
                self.pos_y -= self.speed/2
            else:
                self.moving_up = False
                self.moving_down = True
        elif self.moving_down:
            if self.pos_y + (self.size_height*self.scale/2) < HEIGHT/3:
                self.pos_y += self.speed/2
            else:
                self.moving_up = True
                self.moving_down = False

        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def shoot(self) -> None:
        if self.reload <= 0 and self.live:
            laser_sound_enemy.play()
            projectile_1 = Projectile(
                [self.pos_x + 2.5, self.pos_y + 50], BULLET_SIZE, BULLET_SCALE, "Sprites/Projectile/Normal_2.png", BULLET_SPEED, 180, True, True, BULLET_LIFE, ENEMY_DAMAGE)
            bullets_enemy.add(projectile_1)
            sprites.add(projectile_1)
            self.reload = ENEMY_1_RELOAD_TIME
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
            self.live = False
            self.current = 0
            destroy_enemy_sound.play()
            Score.increase_normal_enemy_score()

    def animation(self) -> None:
        if self.live:
            self.current += FRAME_SPEED
            if self.current >= len(self.idle):
                self.current = 0

            self.image = self.idle[int(self.current)]
            self.image = pygame.transform.scale(
                self.image, (self.size_width*self.scale, self.size_height*self.scale))
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        else:
            self.current += FRAME_SPEED
            if self.current >= len(self.defeat):
                self.kill()
            else:
                self.image = self.defeat[int(self.current)]
                self.image = pygame.transform.scale(
                    self.image, (self.size_width*self.scale*1.16, self.size_height*self.scale*1.01))
                self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
                    
    def update(self) -> None:
        self.animation()
        self.shoot()
        self.colision()
        self.move()
        self.death()
