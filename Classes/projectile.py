import math
from Configs.instances import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, size, scale, path, speed, angle, can_move, breakable, life, damage) -> None:
        super().__init__()
        self.can_move = can_move
        self.breakable = breakable
        self.size_width, self.size_height = size
        self.scale = scale
        self.speed = speed
        self.angle = angle
        self.pos_x, self.pos_y = pos
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(
            self.image, (self.size_width*self.scale, self.size_height*self.scale))
        self.image = pygame.transform.rotate(
            self.image, self.angle)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.life_time = life
        self.spawn_time = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = damage

    def move(self):
        if self.can_move:
            dx = math.sin(self.angle*math.pi/180) * self.speed
            dy = math.cos(self.angle*math.pi/180) * self.speed
            self.pos_y += dy
            self.pos_x += dx
            self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        if pygame.time.get_ticks() - self.spawn_time > self.life_time:
            self.kill()

    def update(self) -> None:
        self.move()
