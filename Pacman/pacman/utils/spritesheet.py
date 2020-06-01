import pygame

class SpriteSheet:
    def __init__(self, filename, rows, cols, w, h):
        self.sheet = pygame.image.load(filename)
        self.rows = rows
        self.cols = cols
        self.frame_count = rows*cols
        self.sheet = pygame.transform.smoothscale(self.sheet, (w*cols, h*rows))
        self.rect = self.sheet.get_rect()
        self.frame_width = self.rect.width / cols
        self.frame_height = self.rect.height / rows

        w = self.frame_width
        h = self.frame_height
        self.frames = list([(index % cols * w, index % rows * h, w, h) for index in range(self.frame_count)])

    def render(self, screen, frame_index, x, y):
        screen.blit(self.sheet, (x, y), self.frames[frame_index])
