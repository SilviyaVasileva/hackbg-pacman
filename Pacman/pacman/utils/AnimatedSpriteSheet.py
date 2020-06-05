import pygame


class AnimatedSpriteSheet:
    '''
    THE SPRITESHEET IMAGES MUST BE PROPORTIONALLY DISTANCED AND OF THE SAME SIZE.
    THE SPRITESHEET IMAGE SHOULD BE ARRANGED AS A MATRIX.

    Load a sprite sheet image and it will be parsed to a list of every frame.\n
    If one of the 2 dimensional parameters (w or h) is set to -1,\n
    the other will be auto-calculated to be proportional to the first.\n

    Call the animation_update() method to move the animations along.\n
    Call the render() method to render the appropriate frame automatically.\n
    '''

    def __init__(self, filename, rows, cols, w, h, center_dimensions=None, animation_speed=10, game_fps=60):
        '''
        Parameters:\n
        filename - spritesheet image path\n
        rows, cols - gives information on how to cut up the matrix (spritesheet)
        w, h - desired sizes for each frame
        animation_fps - what fps does the animation consist of
        game_fps - (default 60), what fps the game the spritesheet will be rendered in use
        '''

        # =============== Frame Data ===============
        original = pygame.image.load(filename)
        sz = original.get_size()
        self.rows = rows
        self.cols = cols
        self.frame_count = rows * cols

        if w < -1 or h < -1:
            raise ValueError("Either both dimensions are negative or one is less than -1.")
        else:
            w *= cols
            h *= rows

        self.sheet = pygame.transform.scale(original, (w, h))

        self.rect = self.sheet.get_rect()
        self.frame_width = self.rect.width / cols
        self.frame_height = self.rect.height / rows
        self.offset_x = 0
        self.offset_y = 0

        self.frames = list([(index % cols * self.frame_width, index % rows * self.frame_height, self.frame_width, self.frame_height)
                            for index in range(self.frame_count)])

        if center_dimensions is not None:
            x, y = center_dimensions
            self.offset_x = (self.frame_width - x) // 2
            self.offset_y = (self.frame_height - x) // 2

        # =============== Animation ===============
        self.anim_speed = animation_speed
        self.anim_current_frame = 0
        self.anim_count = 0
        self.game_fps = game_fps
        self.loops = self.game_fps // self.anim_speed


    def render(self, screen, x, y):
        screen.blit(self.sheet, (x - self.offset_x, y - self.offset_y), self.frames[self.anim_current_frame])

    def update(self):
        if self.anim_count == self.frame_count * self.loops:
            self.anim_count = 0

        self.anim_current_frame = self.anim_count // self.loops
        self.anim_count += 1
