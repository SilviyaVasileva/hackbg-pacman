import pygame


from ..utils.AnimatedSpriteSheet import AnimatedSpriteSheet


class Ghost:

    GHOST = "Pacman/media/2_frame_anims"  # Works in root only

    valid_behaviors = ["Chase", "Wander"]
    skins = {
        "Sakura": {
                "Left": "/sakura ghost/sakura_ghost_left_spritesheet.png",
                "Right": "/sakura ghost/sakura_ghost_right_spritesheet.png",
                "Up": "/sakura ghost/sakura_ghost_up_spritesheet.png",
                "Down": "/sakura ghost/sakura_ghost_down_spritesheet.png"
            },
        "Blue": {
                "Left": "/blue ghost/blue_ghost_left_spritesheet.png",
                "Right": "/blue ghost/blue_ghost_right_spritesheet.png",
                "Up": "/blue ghost/blue_ghost_up_spritesheet.png",
                "Down": "/blue ghost/blue_ghost_down_spritesheet.png"
            },
        "Orange": {
                "Left": "/orange ghost/orange_ghost_left_spritesheet.png",
                "Right": "/orange ghost/orange_ghost_right_spritesheet.png",
                "Up": "/orange ghost/orange_ghost_up_spritesheet.png",
                "Down": "/orange ghost/orange_ghost_down_spritesheet.png"
            },
        "Pink": {
                "Left": "/pink ghost/pink_ghost_left_spritesheet.png",
                "Right": "/pink ghost/pink_ghost_right_spritesheet.png",
                "Up": "/pink ghost/pink_ghost_up_spritesheet.png",
                "Down": "/pink ghost/pink_ghost_down_spritesheet.png"
            },
        "Green": {
                "Left": "/green ghost/green_ghost_left_spritesheet.png",
                "Right": "/green ghost/green_ghost_right_spritesheet.png",
                "Up": "/green ghost/green_ghost_up_spritesheet.png",
                "Down": "/green ghost/green_ghost_down_spritesheet.png"
            }
        }

    def __init__(self, skin, velocity=4, behavior="Wander"):
        # =============== Small Validations ===============
        if skin not in Ghost.skins.keys():
            raise ValueError("Unrecognized skin")
        if behavior not in Ghost.valid_behaviors:
            raise ValueError("Unrecognized behavior")

        # =============== Configs ===============
        self.w = 36
        self.h = 36
        self.behavior = behavior
        self.velocity = velocity

        # =============== Scale and Positioning ===============
        self.pos = {'x': None, 'y': None}
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.hitbox = None

        # =============== Sprites and Images ===============
        self.ss_left = AnimatedSpriteSheet(f"{Ghost.GHOST}{Ghost.skins[skin]['Left']}", 1, 2, self.w, self.h)
        self.ss_right = AnimatedSpriteSheet(f"{Ghost.GHOST}{Ghost.skins[skin]['Right']}", 1, 2, self.w, self.h)
        self.ss_up = AnimatedSpriteSheet(f"{Ghost.GHOST}{Ghost.skins[skin]['Up']}", 1, 2, self.w, self.h)
        self.ss_down = AnimatedSpriteSheet(f"{Ghost.GHOST}{Ghost.skins[skin]['Down']}", 1, 2, self.w, self.h)


    @property
    def x(self):
        return self.pos['x']

    @property
    def y(self):
        return self.pos['y']

    @x.setter
    def x(self, val):
        self.pos['x'] = val
        self.update_collision()

    @y.setter
    def y(self, val):
        self.pos['y'] = val
        self.update_collision()




    # ######################### State #########################

    def update_collision(self):
        self.hitbox = (self.x, self.y, self.w, self.h)

    def render(self, screen):
        if (self.x is not None and self.y is not None):  # Make sure player is spawned

                if self.moving_right:
                    self.ss_right.render(screen, self.x, self.y)

                if self.moving_left:
                    self.ss_left.render(screen, self.x, self.y)

                if self.moving_up:
                    self.ss_up.render(screen, self.x, self.y)

                if self.moving_down:
                    self.ss_down.render(screen, self.x, self.y)

                else:
                    self.ss_right.render(screen, self.x, self.y)

        self.update_anims()

    def update_anims(self):
        self.ss_up.update()
        self.ss_right.update()
        self.ss_down.update()
        self.ss_left.update()
