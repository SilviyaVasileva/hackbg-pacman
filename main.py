import pygame
from pygame.locals import *
import sys
from Pacman.pacman.maze.Maze import Maze
from Pacman.pacman.characters.Player import Player

def game_loop(loop):
    loop()

def pacman_game(mapfile):
    pygame.init()  # Initialize pygame
    pygame.display.set_caption("Pacman baby <3")  # Window title

    player = Player()
    maze = Maze(mapfile, player)
    game_loop(maze.get_loop())

if __name__ == '__main__':
    pacman_game('./Pacman/maps/yellow.txt')