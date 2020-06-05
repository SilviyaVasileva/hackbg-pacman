import pygame
from ..utils.AnimatedSpriteSheet import AnimatedSpriteSheet


class Player:

    PACMAN = "Pacman/media/3_frame_anims/pacman"  # Works in root only

    # ######################### Setups and Properties #########################
    def __init__(self):
        # =============== Auto-configs ===============
        self.w = 33
        self.h = 33
        self.hitbox = None

        # =============== Automatic Image Loading ===============
        img_up = pygame.image.load(f"{Player.PACMAN}/pacman_up2.png")
        img_right = pygame.image.load(f"{Player.PACMAN}/pacman_right2.png")
        img_down = pygame.image.load(f"{Player.PACMAN}/pacman_down2.png")
        img_left = pygame.image.load(f"{Player.PACMAN}/pacman_left2.png")
        self.img_up = pygame.transform.scale(img_up, (self.w, self.h))
        self.img_right = pygame.transform.scale(img_right, (self.w, self.h))
        self.img_down = pygame.transform.scale(img_down, (self.w, self.h))
        self.img_left = pygame.transform.scale(img_left, (self.w, self.h))

        self.ss_up = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_up_spritesheet.png", 1, 3, self.w, self.h, (self.w, self.h))
        self.ss_right = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_right_spritesheet.png", 1, 3, self.w, self.h, (self.w, self.h))
        self.ss_down = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_down_spritesheet.png", 1, 3, self.w, self.h, (self.w, self.h))
        self.ss_left = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_left_spritesheet.png", 1, 3, self.w, self.h, (self.w, self.h))
        
        self.ss_up_large = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_up_spritesheet.png", 1, 3, 80, 80, (self.w, self.h))
        self.ss_right_large = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_right_spritesheet.png", 1, 3, 80, 80, (self.w, self.h))
        self.ss_down_large = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_down_spritesheet.png", 1, 3, 80, 80, (self.w, self.h))
        self.ss_left_large = AnimatedSpriteSheet(f"{Player.PACMAN}/pacman_left_spritesheet.png", 1, 3, 80, 80, (self.w, self.h))

        # =============== Animation data ===============
        self.current_frame = 0  # current frame to display from the spritesheet
        self.counter = 0
        self.anim_speed = 9  # fps of the animation
        self.frames = 3  # total frames of the animation

        # =============== Movement and Direction ===============
        self.pos = {'x': None, 'y': None}
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.last_move_direction = "right"
        self.velocity = 4

        # =============== Game points ===============
        self.points = 0

        # =============== Debug ===============
        self.draw_collisions = False

    @property
    def x(self):
        return self.pos['x']

    @property
    def y(self):
        return self.pos['y']

    # ######################### Setting and Getting #########################
    @x.setter
    def x(self, val):
        self.pos['x'] = val
        self.update_collision()

    @y.setter
    def y(self, val):
        self.pos['y'] = val
        self.update_collision()

    # ######################### State #########################
    def is_moving(self):
        if self.moving_up or self.moving_right or self.moving_down or self.moving_left:
            return True
        return False

    def update_collision(self):
        self.hitbox = (self.x, self.y, self.w, self.h)

    def render(self, screen):
        if (self.x is not None and self.y is not None):  # Make sure player is spawned

            if self.last_move_direction == "up":
                if self.is_moving():
                    self.ss_up.render(screen, self.x, self.y)
                else:
                    screen.blit(self.img_up, (self.x, self.y))

            elif self.last_move_direction == "right":
                if self.is_moving():
                    self.ss_right.render(screen, self.x, self.y)
                else:
                    screen.blit(self.img_right, (self.x, self.y))

            elif self.last_move_direction == "down":
                if self.is_moving():
                    self.ss_down.render(screen, self.x, self.y)
                else:
                    screen.blit(self.img_down, (self.x, self.y))

            elif self.last_move_direction == "left":
                if self.is_moving():
                    self.ss_left.render(screen, self.x, self.y)
                else:
                    screen.blit(self.img_left, (self.x, self.y))

        if self.draw_collisions:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        self.update_anims()

    def update_anims(self):
        self.ss_up.update()
        self.ss_right.update()
        self.ss_down.update()
        self.ss_left.update()

    # ######################### Setting and Getting #########################
    def enable_collision_rendering(self, val=True):
        self.draw_collisions = val

    # ######################### Updating pints #########################
    def update_points(self, points):
        self.points += points
