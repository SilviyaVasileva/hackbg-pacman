import pygame
import random


from ..utils.AnimatedSpriteSheet import AnimatedSpriteSheet


class Ghost:

    GHOST = "Pacman/media/2_frame_anims"  # Works in root only

    behaviors = ["Chase", "Patrol", "Random"]

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

    def __init__(self, maze, skin, velocity=4, behavior="Random"):
        # =============== Small Validations ===============
        if behavior not in Ghost.behaviors:
            raise ValueError("Unrecognized behavior")
        if skin not in Ghost.skins.keys():
            raise ValueError("Unrecognized skin")

        # =============== Configs ===============
        self.states = ["Suspended", "Boxed", "Exit Right", "Exit Mid", "Exit Left", "Free Move"]
        self._state = "Boxed"

        self.exit_direction = None
        self.exit_count = 0

        self.default_behavior = behavior
        self.behavior = behavior
        self.w = 36
        self.h = 36
        self.velocity = velocity
        self.maze = maze

        # =============== Scale and Positioning ===============
        self.pos = {'x': None, 'y': None}
        self.hitbox = (0, 0, 0, 0)
        self.direction = "Right"
        self.turn_direction = None

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

    def set_state(self, state):
        if state == "Boxed":
            self._state = "Boxed"

        elif state == "Suspended":
            self._state = "Suspended"

        elif state == "Exit Left":
            self.exit_direction = "Right"
            self.exit_count = self.maze.map_scale[0]
            self._state = "Exit Left"

        elif state == "Exit Right":
            self.exit_direction = "Left"
            self.exit_count = self.maze.map_scale[0]
            self._state = "Exit Right"

        elif state == "Exit Mid":
            self.exit_direction = "Up"
            self.exit_count = self.maze.map_scale[1] * 2
            self._state = "Exit Mid"

        elif state == "Free Move":
            self._state = "Free Move"

        else:
            raise ValueError("Unrecognized state")

    def update_collision(self):
        self.hitbox = (self.x, self.y, self.w, self.h)

    def render(self, screen):
        if (self.x is not None and self.y is not None):  # Make sure player is spawned

                if self.direction == "Right":
                    self.ss_right.render(screen, self.x, self.y)

                if self.direction == "Left":
                    self.ss_left.render(screen, self.x, self.y)

                if self.direction == "Up":
                    self.ss_up.render(screen, self.x, self.y)

                if self.direction == "Down":
                    self.ss_down.render(screen, self.x, self.y)

                else:
                    self.ss_right.render(screen, self.x, self.y)

        self.update_anims()

    def update_anims(self):
        self.ss_up.update()
        self.ss_right.update()
        self.ss_down.update()
        self.ss_left.update()




    # ######################### Movement #########################

    def move(self, exclude=None):
        if self._state == "Exit Right" and self.exit_count > 0:
            self.x -= self.velocity
            self.exit_count -= self.velocity
            if self.exit_count <= 0:
                self.set_state("Exit Mid")

        elif self._state == "Exit Left" and self.exit_count > 0:
            self.x += self.velocity
            self.exit_count -= self.velocity
            if self.exit_count <= 0:
                self.set_state("Exit Mid")

        elif self._state == "Exit Mid" and self.exit_count > 0:
            self.y -= self.velocity
            self.exit_count -= self.velocity
        
            if self.exit_count <= 0:
                self.set_state("Free Move")

        # =============== Free Move Code Below ===============
        elif self._state == "Free Move":
            if exclude is None:
                exclude = []

            if self.direction == "Right":
                self.x += self.velocity
                if self.maze.collide(self.hitbox, ["walls", "gates"]):
                    self.x -= self.velocity
                    exclude.append("Right")
                    self.set_move(exclude)
                    self.move(exclude)

            elif self.direction == "Left":
                self.x -= self.velocity
                if self.maze.collide(self.hitbox, ["walls", "gates"]):
                    self.x += self.velocity
                    exclude.append("Left")
                    self.set_move(exclude)

            elif self.direction == "Up":
                self.y -= self.velocity
                if self.maze.collide(self.hitbox, ["walls", "gates"]):
                    self.y += self.velocity
                    exclude.append("Up")
                    self.set_move(exclude)
                    self.move(exclude)

            elif self.direction == "Down":
                self.y += self.velocity
                if self.maze.collide(self.hitbox, ["walls", "gates"]):
                    self.y -= self.velocity
                    exclude.append("Down")
                    self.set_move(exclude)
                    self.move(exclude)

    def set_move(self, exclude=None):
        if self.maze._state == "Playing":
            if self.behavior == "Random":
                self.random(exclude)

    def random(self, exclude):
        choices = [opt for opt in ["Right", "Left", "Up", "Down"] if opt not in exclude]
        self.direction = random.choice(choices)
