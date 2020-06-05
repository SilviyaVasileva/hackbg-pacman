import pygame
from pygame.locals import *
import sys
import os
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
    maps_path = "./Pacman/maps/"
    maps = [m for m in os.listdir(maps_path) if os.path.isfile(maps_path + m)]
    if len(sys.argv) == 1:
        print("\n====================================================")
        print("Select map to play by typing: ")
        print("\"python main.py <map name>.txt\"")
        print("\nCurrently available maps:")
        for m in maps:
            print(m)
        print("====================================================")

    if len(sys.argv) > 2:
        print("\n====================================================")
        print("For now, level selection is done through command line :(\nType \"python main.py\" for help.")
        print("====================================================")

    if len(sys.argv) == 2:
        if sys.argv[1] not in maps:
            print("\n====================================================")
            print("We didn't manage to find this map :(\nType \"python main.py\" for help.")
            print("====================================================")
        else:
            pacman_game(maps_path + sys.argv[1])
