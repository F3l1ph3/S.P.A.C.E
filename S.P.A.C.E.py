import sys
from Configs.instances import *
from Classes import *


# Presets
pygame.display.set_caption("S.P.A.C.E")
pygame.display.set_icon(ICON)

# Reset sprite groups
def reset_sprite_groups():
    sprites.empty()
    players.empty()
    enemies.empty()
    bullets_player.empty()
    bullets_enemy.empty()


# Game
def play(spawn, bg):
    bg.set_speed(5)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Sounds/OST_2.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1, fade_ms=1000)
    Score.reset()

    while True:

        CLOCK.tick(FPS)
        SCREEN.fill((0, 0, 0))
        bg.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for player in players:
            if player.dead:
                player.kill()
                reset_sprite_groups()
                main_menu()
                
        
        sprites.draw(SCREEN)
        spawn.update()
        sprites.update()

        Score.update()
        pygame.display.flip()


# Menu
def main_menu():
    bg = Background([0, 0], [WIDTH, HEIGHT],
                    'Backgrounds/Stars_background.png', 2)
    bg.set_speed(2)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Sounds/OST_1.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1, fade_ms=1000)

    while True:

        CLOCK.tick(FPS)
        SCREEN.fill((0, 0, 0))
        bg.update()
        MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button("Play", FONT_BUTTONS, int(WIDTH/12), [int(
            WIDTH/2), int(HEIGHT/2.2)], "white", "yellow")
        EXIT_BUTTON = Button("Exit", FONT_BUTTONS, int(WIDTH/25), [int(
            WIDTH/2), int(HEIGHT/1.6)], "white", "yellow")

        buttons = [PLAY_BUTTON, EXIT_BUTTON]
        for button in buttons:
            button.hover(MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.hover_check(MOUSE_POS):
                        spawn = Spawn()
                        play(spawn, bg)
                    elif EXIT_BUTTON.hover_check(MOUSE_POS):
                        pygame.quit()
                        sys.exit()

        Score.update()
        pygame.display.flip()


main_menu()
