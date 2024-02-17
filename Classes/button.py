from Configs.instances import *

class Button:
    def __init__(self, text, font, size, pos, base_color, hover_color) -> None:
        self.font_name = font
        self.font_obj = pygame.font.Font(font, size)
        self.size = size
        self.pos_x, self.pos_y = pos
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = text
        self.text_render = self.font_obj.render(
            self.text, True, self.base_color)
        self.rect = self.text_render.get_rect(center=(self.pos_x, self.pos_y))

    def update(self, screen) -> None:
        screen.blit(self.text_render, self.rect)

    def hover(self, pos) -> None:
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.font_obj = pygame.font.Font(
                self.font_name, int(self.size*1.1))
            self.text_render = self.font_obj.render(
                self.text, True, self.hover_color)
            self.rect = self.text_render.get_rect(
                center=(self.pos_x, self.pos_y))

    def hover_check(self, pos) -> bool:
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False
