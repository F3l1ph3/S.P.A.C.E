import math

from Classes.projectile import Projectile
from Configs.instances import *

# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, scale, path_idle, path_power, path_defeat, frames) -> None:
        super().__init__()
        # Aimation lists
        self.idle = [pygame.image.load(
            f"{path_idle}{num+1}.png") for num in range(frames)]
        self.power = [pygame.image.load(
            f"{path_power}{num+1}.png") for num in range(frames)]
        self.defeat = [pygame.image.load(
            f"{path_defeat}{num+1}.png") for num in range(frames)]
        # Current index/frame of the animation
        self.current = 0
        # Size of the image
        self.size_width, self.size_height = size
        # Scale of the image
        self.scale = scale
        # Initial position
        self.pos_x, self.pos_y = pos
        # Image that will bem drowned
        self.image = self.idle[self.current]
        # Resize image * scale
        self.image = pygame.transform.scale(
            self.image, (self.size_width*self.scale, self.size_height*self.scale))
        # Get rect of the image
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        # Initial reload
        self.reload = 0
        # Mask (for colision system)
        self.mask = pygame.mask.from_surface(self.image)
        # Active ultimate
        self.ultimate_enable = True
        # Initialize the "ultimate" image to None
        self.ultimate_projectile = None
        # Life Value
        self.life = PLAYER_LIFE
        # if is dead
        self.dead = False
        self.live = True
        # get image of the life sprite
        self.life_image = pygame.image.load('Sprites/Player/Life/life.png')
        # resize life_image * scale
        self.life_image = pygame.transform.scale(
            self.life_image, (LIFE_BAR_SIZE[0]*LIFE_BAR_SCALE, LIFE_BAR_SIZE[1]*LIFE_BAR_SCALE))

    # Move system
    def move(self) -> None:
        # Speed x, y
        speed_x = 0
        speed_y = 0

        # Direction
        if pygame.key.get_pressed()[K_LEFT]:
            speed_x -= MOVE_SPEED
        if pygame.key.get_pressed()[K_RIGHT]:
            speed_x += MOVE_SPEED
        if pygame.key.get_pressed()[K_UP]:
            speed_y -= MOVE_SPEED
        if pygame.key.get_pressed()[K_DOWN]:
            speed_y += MOVE_SPEED

        # Diagonals
        if speed_x != 0 and speed_y != 0:
            speed_x = speed_x / math.sqrt(2)
            speed_y = speed_y / math.sqrt(2)

        # Over width
        if speed_x > 0:
            if self.pos_x + (self.size_width*self.scale)/2 < WIDTH:
                self.pos_x += speed_x
        if speed_x < 0:
            if self.pos_x - (self.size_width*self.scale)/2 > 0:
                self.pos_x += speed_x

        # Over height
        if speed_y > 0:
            if self.pos_y + (self.size_height*self.scale)/2 <= HEIGHT:
                self.pos_y += speed_y
        if speed_y < 0:
            if self.pos_y - (self.size_height*self.scale)/2 >= 0:
                self.pos_y += speed_y

        # Update rect to the new position
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    # Animation
    def animation(self) -> None:
        
        if self.live:
            # With ultimate (glow in the midle)
            if self.ultimate_enable:
                self.current += FRAME_SPEED
                if self.current >= len(self.power):
                    self.current = 0
                self.image = self.power[int(self.current)]
                self.image = pygame.transform.scale(
                    self.image, (self.size_width*self.scale, self.size_height*self.scale))
            else:
                # Without ultimate
                self.current += FRAME_SPEED
                if self.current >= len(self.idle):
                    self.current = 0
                self.image = self.idle[int(self.current)]
                self.image = pygame.transform.scale(
                    self.image, (self.size_width*self.scale, self.size_height*self.scale))
        else:
            self.current += FRAME_SPEED
            if self.current >= len(self.defeat):
                self.dead = True
            else:
                self.image = self.defeat[int(self.current)]
                self.image = pygame.transform.scale(
                    self.image, (self.size_width*self.scale*1.08, self.size_height*self.scale*1.02))
                self.rect = self.image.get_rect(
                    center=(self.pos_x, self.pos_y))
    
    # Shoot system
    def shoot(self) -> None:
        if self.reload <= 0 and self.live:
            if self.life > 1:
                # Play sound effect
                laser_sound_player.play()
                # Create projectiles
                projectile_1 = Projectile(
                    [self.pos_x + PLAYER_BULLET_CORRECTION_X, self.pos_y - PLAYER_BULLET_CORRECTION_Y], BULLET_SIZE, BULLET_SCALE, "Sprites/Projectile/Normal_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE)
                projectile_2 = Projectile(
                    [self.pos_x - PLAYER_BULLET_CORRECTION_X, self.pos_y - PLAYER_BULLET_CORRECTION_Y], BULLET_SIZE, BULLET_SCALE, "Sprites/Projectile/Normal_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE)
                projectile_3 = Projectile(
                    [self.pos_x, self.pos_y - PLAYER_BULLET_CORRECTION_BALL], BULLET_SIZE, 2, "Sprites/Projectile/Normal_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE)

                # Add projectiles to group
                bullets_player.add(projectile_1)
                bullets_player.add(projectile_2)
                bullets_player.add(projectile_3)

                sprites.add(projectile_1)
                sprites.add(projectile_2)
                sprites.add(projectile_3)

                # Set reload time
                self.reload = 30
            else:
                # Play sound effect
                laser_sound_player.play()
                # Create projectiles
                projectile_1 = Projectile(
                    [self.pos_x + PLAYER_BULLET_CORRECTION_X, self.pos_y - PLAYER_BULLET_CORRECTION_Y], BULLET_SIZE, BULLET_SCALE, "Sprites/Projectile/Ball_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE*2)
                projectile_2 = Projectile(
                    [self.pos_x - PLAYER_BULLET_CORRECTION_X, self.pos_y - PLAYER_BULLET_CORRECTION_Y], BULLET_SIZE, BULLET_SCALE, "Sprites/Projectile/Ball_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE*2)
                projectile_3 = Projectile(
                    [self.pos_x, self.pos_y - PLAYER_BULLET_CORRECTION_BALL], BULLET_SIZE, 2, "Sprites/Projectile/Ball_1.png", BULLET_SPEED, 0, True, True, BULLET_LIFE, PLAYER_DAMAGE*2)

                # Add projectiles to group
                bullets_player.add(projectile_1)
                bullets_player.add(projectile_2)
                bullets_player.add(projectile_3)

                sprites.add(projectile_1)
                sprites.add(projectile_2)
                sprites.add(projectile_3)

                # Set reload time
                self.reload = 30
        else:
            # Decrease cooldown
            self.reload -= 1

    # Ultimate
    def ultimate(self) -> None:
        # Space pressed + Able to use ultimate
        if pygame.key.get_pressed()[K_SPACE] and self.ultimate_enable:
            # Play sound effect
            ultimate_sound_player.play()
            # Stop shooting for a while
            self.reload = 150
            # Disable ultimate
            self.ultimate_enable = False
            # Create "ultimate" preojectile
            self.ultimate_projectile = Projectile(
                [self.pos_x - ULTIMATE_CORRECTION_X, self.pos_y - ULTIMATE_CORRECTION_Y], ULTIMATE_BULET_SIZE, BULLET_SCALE, "Sprites/Projectile/Laser_1.png", BULLET_SPEED, 0, False, False, PLAYER_BULLET_ULTIMATE_LIFE, ULTIMATE_DAMAGE)
            # Add sprite to group
            bullets_player.add(self.ultimate_projectile)
            sprites.add(self.ultimate_projectile)

        # Projectile was created
        if self.ultimate_projectile != None:
            projectile = self.ultimate_projectile
            # Ultimete beam follows the player
            projectile.pos_x, projectile.pos_y = [
                self.pos_x - ULTIMATE_CORRECTION_X, self.pos_y - ULTIMATE_CORRECTION_Y]
            projectile.rect = projectile.image.get_rect(
                center=(projectile.pos_x, projectile.pos_y))

    # Turn on ultimate
    def enable_ultimate(self) -> None:
        self.ultimate_enable = True

    # Colision system
    def colision(self) -> None:
        # Get elements of a sprite group (bullets_enemy)
        for bullet in bullets_enemy:
            # verify if mask atribute collides with another group os sprites (players)
            if pygame.sprite.spritecollide(bullet, players, False, pygame.sprite.collide_mask):
                # Play colision sound
                colide_sound_player.play()
                # atribute breakable of the projectiles
                if bullet.breakable:
                    # del sprite
                    bullet.kill()
                    # lose life
                    self.life -= bullet.damage

    # Death system
    def death(self) -> None:
        if self.life <= 0 and self.live:
            self.live = False
            self.current = 0
            destroy_player_sound.play()
            for bullet in bullets_player:
                bullet.kill()
    # Display life bar
    def life_bar(self):
        # Drawn the current amount of life
        for life in range(self.life):
            # Create surface to draw the images
            rect = self.life_image.get_rect(topleft=(
                LIFE_BAR_POS_X + (life * self.life_image.get_width()), LIFE_BAR_POS_Y))
            # Draw image on the surface (rect)
            SCREEN.blit(self.life_image, rect)

    # Call other methods
    def update(self) -> None:
        self.life_bar()
        self.death()
        self.move()
        self.shoot()
        self.ultimate()
        self.colision()
        self.animation()
