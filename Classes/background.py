from Configs.instances import *

class Background:
    def __init__(self, pos, size, path, speed) -> None:
        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.scroll = 0
        self.speed = speed

    # Sroll background
    def scrolling(self) -> None:
        self.scroll += self.speed
        if self.scroll >= self.height:
            self.scroll = 0
        for i in range(2):
            self.rect = self.image.get_rect(
                topleft=(self.pos_x, self.height * (-i) + self.scroll))
            SCREEN.blit(self.image, self.rect)

    # Change speed of scroll
    def set_speed(self, value) -> None:
        self.speed = value

    def update(self) -> None:
        self.scrolling()
