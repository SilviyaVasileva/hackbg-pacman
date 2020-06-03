import pygame
from pygame.locals import *
import sys
from Pacman.pacman.maze.Maze import Maze
from Pacman.pacman.characters.Player import Player


def pacman_game(mapfile):
    pygame.init()  # Initialize pygame
    pygame.display.set_caption("Pacman baby <3")  # Window title

    player = Player()
    maze = Maze(mapfile, player)
    screen = pygame.display.set_mode(maze.win_size(), 0, 32) # Initialize window



    maze.place_player(screen)
    pygame.display.update()

    while True:
        # Check if the game is started
        if maze.start_game:
        # PLAYER MOVEMENT
            if player.moving["up"]:
                player.y -= player.velocity
                if maze.collide(maze.player.hitbox, "walls"): # If move results in collision
                    maze.player.y += player.velocity  # revert to last valid position
                else:  # If move does not result in collision
                    maze.player.last_move_direction = "up"  # Pacman will face this movement direction
        
            if player.moving["right"]:  
                maze.player.x += player.velocity
                if maze.collide(maze.player.hitbox, "walls"):  # If move results in collision
                    maze.player.x -= player.velocity  # revert to last valid position
                else:  # If move does not result in collision
                    maze.player.last_move_direction = "right" # revert to last valid position

            if player.moving["down"]:
                player.y += player.velocity
                if maze.collide(maze.player.hitbox, "walls"):  # If move results in collision
                    player.y -= player.velocity  # revert to last valid position
                else:  # If move does not result in collision
                    maze.player.last_move_direction = "down"  # revert to last valid position
        
            if player.moving["left"]:
                player.x -= player.velocity
                if maze.collide(maze.player.hitbox, "walls"):  # If move results in collision
                    player.x += player.velocity  # revert to last valid position
                else:  # If move does not result in collision
                    maze.player.last_move_direction = "left"  # revert to last valid position

        # USER INPUT
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:  # on key press
                if event.key == K_UP:
                    maze.player.set_direction("up", True)
                if event.key == K_RIGHT:
                    maze.player.set_direction("right", True)
                if event.key == K_DOWN:
                    maze.player.set_direction("down", True)
                if event.key == K_LEFT:
                    maze.player.set_direction("left", True)
            if event.type == KEYUP:  # on key release
                if event.key == K_UP:
                    maze.player.set_direction("up", False)
                if event.key == K_RIGHT:
                    maze.player.set_direction("right", False)
                if event.key == K_DOWN:
                    maze.player.set_direction("down", False)
                if event.key == K_LEFT:
                    maze.player.set_direction("left", False)


        maze.interractions()
        maze.render(screen)
        maze.player.render(screen)
        pygame.display.update()
        maze.clock.tick(60)  # Framerate


if __name__ == '__main__':
    pacman_game('./Pacman/maps/yellow.txt')