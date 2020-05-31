import pygame
from pygame.locals import *
import sys
from Pacman.pacman.maze.Maze import Maze
from Pacman.pacman.characters.Player import Player


def pacman_game(mapfile):
    pygame.init()  # Initialize pygame
    pygame.display.set_caption("Pacman baby <3")  # Window title

    dummy = Player()
    maze = Maze(mapfile, dummy)
    screen = pygame.display.set_mode(maze.win_size(), 0, 32) # Initialize window
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # Check for window quit (when X is pressed)
                pygame.quit()  # stop pygame
                sys.exit()  # stop the script

        maze.render(screen)
        pygame.display.update()
        maze.clock.tick(60)  # Framerate


if __name__ == '__main__':
    pacman_game('./Pacman/maps/yellow.txt')