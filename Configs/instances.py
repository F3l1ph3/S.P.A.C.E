from Configs.settings import *
from pygame.locals import *

# Groups of sprites
sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets_player = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()

# Sounds
laser_sound_player = pygame.mixer.Sound('Sounds/Sound2.mp3')
laser_sound_enemy = pygame.mixer.Sound('Sounds/Sound1.mp3')
laser_sound_boss = pygame.mixer.Sound('Sounds/Sound1.mp3')
ultimate_sound_player = pygame.mixer.Sound('Sounds/sound3.mp3')
colide_sound_player = pygame.mixer.Sound('Sounds/sound4.mp3')
destroy_enemy_sound = pygame.mixer.Sound('Sounds/sound5.mp3')
destroy_player_sound = pygame.mixer.Sound('Sounds/sound6.mp3')

laser_sound_player.set_volume(0.02)
ultimate_sound_player.set_volume(0.04)
laser_sound_enemy.set_volume(0.03)
laser_sound_boss.set_volume(0.02)
colide_sound_player.set_volume(0.1)
destroy_enemy_sound.set_volume(0.05)
destroy_player_sound.set_volume(0.3)
