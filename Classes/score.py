from Configs.instances import *

# Score system
class Score:
    score_time = pygame.time.get_ticks()
    pos_x, pos_y = SCORE_POSITION
    score_normal_enemy = 0
    score_boss = 0
    score_total = score_normal_enemy + score_boss
    font_obj = pygame.font.Font(FONT_SCORE, SCORE_FONT_SIZE)
    color = "white"
    text = f"Score: {score_total}"
    text_render = font_obj.render(text, True, color)
    rect = text_render.get_rect(topleft=(pos_x, pos_y))

    @staticmethod
    def increase_normal_enemy_score() -> None:
        Score.score_time = pygame.time.get_ticks()
        Score.score_normal_enemy += 100
        Score.score_total = Score.score_normal_enemy + Score.score_boss

    @staticmethod
    def increase_boss_score() -> None:
        Score.score_time = pygame.time.get_ticks()
        Score.score_boss += 1000
        Score.score_total = Score.score_normal_enemy + Score.score_boss

    @staticmethod
    def update() -> None:
        Score.text = f"Score: {Score.score_total}"
        Score.text_render = Score.font_obj.render(
            Score.text, True, Score.color)
        Score.rect = Score.text_render.get_rect(
            topleft=(Score.pos_x, Score.pos_y))
        SCREEN.blit(Score.text_render, Score.rect)

    @staticmethod
    def reset() -> None:
        Score.score_normal_enemy = 0
        Score.score_boss = 0
        Score.score_total = Score.score_normal_enemy + Score.score_boss
