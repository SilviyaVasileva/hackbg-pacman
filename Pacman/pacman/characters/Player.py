import pygame
from ..utils.spritesheet import SpriteSheet


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

        self.spritesheet_up = SpriteSheet(f"{Player.PACMAN}/pacman_up_spritesheet.png", 1, 3, 35, 35)
        self.spritesheet_right = SpriteSheet(f"{Player.PACMAN}/pacman_right_spritesheet.png", 1, 3, 35, 35)
        self.spritesheet_down = SpriteSheet(f"{Player.PACMAN}/pacman_down_spritesheet.png", 1, 3, 35, 35)
        self.spritesheet_left = SpriteSheet(f"{Player.PACMAN}/pacman_left_spritesheet.png", 1, 3, 35, 35)
        
        # =============== Animation data ===============
        self.current_frame = 0  # current frame to display from the spritesheet
        self.counter = 0
        self.anim_speed = 9  # fps of the animation
        self.frames = 3  # total frames of the animation

        # =============== Movement and Direction ===============
        self.pos = {'x': None, 'y': None}
        self.moving = {
            "up": False,
            "right": False,
            "down": False,
            "left": False
        }
        self.last_move_direction = "right"
        self.velocity = 4

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

    def set_direction(self, direction, state):
        for direc in self.moving:
            if direc == direction:
                self.moving[direc] = state

    # ######################### State #########################
    def is_moving(self):
        for direc in self.moving:
            if self.moving[direc] == True:
                return True
        return False

    def update_collision(self):
        self.hitbox = (self.x, self.y, self.w, self.h)

    def render(self, screen):
        if (self.x is not None and self.y is not None):  # Make sure player is spawned
            
            if self.last_move_direction == "up":
                if self.is_moving():
                    self.spritesheet_up.render(screen, self.current_frame, self.x, self.y)
                else:
                    screen.blit(self.img_up, (self.x, self.y))

            elif self.last_move_direction == "right":
                if self.is_moving():
                    self.spritesheet_right.render(screen, self.current_frame, self.x, self.y)
                else:
                    screen.blit(self.img_right, (self.x, self.y))
    
            elif self.last_move_direction == "down":
                if self.is_moving():
                    self.spritesheet_down.render(screen, self.current_frame, self.x, self.y)
                else:
                    screen.blit(self.img_down, (self.x, self.y))
    
            elif self.last_move_direction == "left":
                if self.is_moving():
                    self.spritesheet_left.render(screen, self.current_frame, self.x, self.y)
                else:
                    screen.blit(self.img_left, (self.x, self.y))

        if self.draw_collisions:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        self.update_anims()

    def update_anims(self):
        loops_in_60_fps = 60 // self.anim_speed

        if self.counter == self.frames * loops_in_60_fps:
            self.counter = 0

        self.current_frame = self.counter  // loops_in_60_fps
        self.counter += 1

    # ######################### Setting and Getting #########################
    def enable_collision_rendering(self, val=True):
        self.draw_collisions = val