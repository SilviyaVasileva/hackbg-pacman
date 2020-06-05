import pygame
import sys
import time
import random


from pygame.locals import *
from ..characters.Ghost import Ghost


class Maze:

    # ######################### Static Data #########################

    COLLECTIBLES = 'Pacman/media/collectibles'

    # The keywords required for a map to be parsed
    parser_keywords = {
        'dimensions': 0,
        'color': 1,
        'walls': 2,
        'player': 3,
        'total': 4
    }
    parser_keywords_count = len(parser_keywords)
    difficulty = [
        "Easy",
        "Normal",
        "Hard",
        "Swarm"
    ]


    # ######################### Setups and Properties #########################
    def __init__(self, mapfile, player, score=0, difficulty="Normal"):
        # =============== Small Validations ===============
        if difficulty not in Maze.difficulty:
            raise ValueError("Unrecognized difficulty")

        # =============== Timed Events ===============
        self.RELEASE_GHOST = pygame.USEREVENT+1

        # =============== Configs ===============
        self.clock = pygame.time.Clock()
        self._state = "Start"
        self.states = ["Start", "Playing", "Game Over"]
        self.map_scale = (36, 36)
        self.bars_h = 80
        self.difficulty = difficulty
        
        # =============== Automatic Image Loading ===============
        img_dot = pygame.image.load(f"{Maze.COLLECTIBLES}/dots/dot.png")
        self.img_dot = pygame.transform.scale(img_dot, self.map_scale)

        # =============== Positions and Scale ===============
        self.dots_scale = (10, 10)
        self.dots_offset = ((self.map_scale[0]- self.dots_scale[0]) // 2, (self.map_scale[1] - self.dots_scale[1]) // 2)
        self.gate_scale = (self.map_scale[0], self.map_scale[1] // 3)

        # =============== Maze data ===============
        self.collision_map = {
            "walls": [],
            "dots": [],
            "power_dots": [],
            "gates": [],
        }
        self.entities = [
            "dots",
            "power_ups", 
            "ghosts"
        ]

        init_data = self.__class__.parse(mapfile)
        self.dimensions = init_data['dimensions']
        self.color = init_data['color']
        self.wall_color = init_data['walls']
        self.player_start = init_data['player']
        self.maze = init_data['maze']
        self.gate = init_data['gate']
        self.ghosts_start = init_data['ghosts']
        self.player = player
        self.dots_total = init_data['total']

        self.gate_color = (224, 128, 128)

        # =============== Game State ===============
        self.game_points = score
        self.ghosts = []
        self.ghosts_in_box = 3

        # =============== Display Elements ==============
        self.font_20 = pygame.font.Font("freesansbold.ttf", 30)
        self.start_button = self.font_20.render("Start", True, (0, 180, 50))
        self.start_button_rect = self.start_button.get_rect()
        raw_rect = self.start_button.get_rect()
        raw_rect[2] += 100; raw_rect[3] += 30
        self.start_button_frame_rect = raw_rect
        self.start_button_rect.center = (self.map_scale[0] * self.dimensions[1] // 2, self.map_scale[1] * self.dimensions[0] + self.bars_h * 1.5)  # , 70, 40)
        self.start_button_frame_rect.center = (self.map_scale[0] * self.dimensions[1] // 2, self.map_scale[1] * self.dimensions[0] + self.bars_h * 1.5)  # , 70, 40)

        # =============== Auto Init Commands ===============
        self.screen = pygame.display.set_mode(self.win_size(), 0, 32)
        self.build()
        self.init_ghosts()

        # =============== Debug vars ===============
        self.draw_all_collisions = False


    def init_ghosts(self):
        choices = list(Ghost.skins.keys())

        if self.difficulty == 'Normal':
            for i in range(0 , len(choices)):
                skin = random.choice(choices)
                choices.remove(skin)
                self.ghosts.append(Ghost(self, skin, self.player.velocity))

        self.place_ghosts()

    def place_player(self):
        self.player.pos['x'] = self.player_start[0] * self.map_scale[0]
        self.player.pos['y'] = self.player_start[1] * self.map_scale[1] + self.bars_h
        self.player.update_collision()
        self.player.render(self.screen)

    def place_ghosts(self):
        for i in range(3):
            ghost = self.ghosts[i]
            ghost.pos['x'] = self.ghosts_start[i][0] * self.map_scale[0]
            ghost.pos['y'] = self.ghosts_start[i][1] * self.map_scale[1] + self.bars_h
            ghost.update_collision()

    def start(self):
        self.display_points(self.screen)

    def build(self):
        '''
        Builds the 'collision_map' variable.\n
        It contains tuples with raw pygame.Rect data to be used for rendering.
        '''

        for i, row in enumerate(self.maze):
            i *= self.map_scale[1]
            i += self.bars_h
            for j, pos in enumerate(row):
                j *= self.map_scale[0]
                if pos == '#':
                    self.collision_map["walls"].append(tuple(
                        [j, i, self.map_scale[0], self.map_scale[1]]  # creates tuple with raw pygame.Rect data
                    ))

                if pos == 'o':
                    self.collision_map["dots"].append(tuple(
                        [j + self.dots_offset[0], i + self.dots_offset[1], self.dots_scale[0], self.dots_scale[1]]  # creates tuple with raw pygame.Rect data
                    ))
            
                if pos == 'e':
                    self.collision_map["gates"].append(tuple(
                        [j, i, self.gate_scale[0], self.gate_scale[1]]  # creates tuple with raw pygame.Rect data
                    ))




    # ######################### State #########################
    def get_loop(self):
        return self.loop

    def loop(self):
        self.place_player()
        pygame.display.update()

        while True:
            if self.dots_total == 0:
                self._state = "Victory"

            # MOVE PLAYER
            if self.player.moving_right:
                self.player.x += self.player.velocity
                if self.collide(self.player.hitbox, ["walls", "gates"]):
                    self.player.x -= self.player.velocity
                else:
                    self.player.last_move_direction = "right"
            if self.player.moving_left:
                self.player.x -= self.player.velocity
                if self.collide(self.player.hitbox, ["walls", "gates"]):
                    self.player.x += self.player.velocity
                else:
                    self.player.last_move_direction = "left"
            if self.player.moving_up:
                self.player.y -= self.player.velocity
                if self.collide(self.player.hitbox, ["walls", "gates"]):
                    self.player.y += self.player.velocity
                else:
                    self.player.last_move_direction = "up"
            if self.player.moving_down:
                self.player.y += self.player.velocity
                if self.collide(self.player.hitbox, ["walls", "gates"]):
                    self.player.y -= self.player.velocity
                else:
                    self.player.last_move_direction = "down"

            # GET NEXT INPUT AND CATCH EVENTS
            for event in pygame.event.get():
                if event.type == QUIT:  # Check for window quit (when X is pressed)
                    pygame.quit()  # stop pygame
                    sys.exit()  # stop the script
                if event.type == self.RELEASE_GHOST:
                    self.ghost_leave_box()

                if self._state == "Start":
                    mouse_pos = pygame.mouse.get_pos()
                    button_pos = self.start_button_rect
                    if button_pos[0] + button_pos[2] > mouse_pos[0] > button_pos[0] and button_pos[1] + button_pos[3] > mouse_pos[1] > button_pos[3]:
                        mouse_click = pygame.mouse.get_pressed()
                        if mouse_click[0] == 1:
                            self._state = "Playing"
                            pygame.time.set_timer(self.RELEASE_GHOST, 1000)

                elif self._state == "Playing":
                    if event.type == KEYDOWN:  # on key press
                        if event.key == K_RIGHT:
                            self.player.moving_right = True
                        if event.key == K_LEFT:
                            self.player.moving_left = True
                        if event.key == K_UP:
                            self.player.moving_up = True
                        if event.key == K_DOWN:
                            self.player.moving_down = True
                    if event.type == KEYUP:  # on key release
                        if event.key == K_RIGHT:
                            self.player.moving_right = False
                        if event.key == K_LEFT:
                            self.player.moving_left = False
                        if event.key == K_UP:
                            self.player.moving_up = False
                        if event.key == K_DOWN:
                            self.player.moving_down = False

            for ghost in self.ghosts:
                ghost.move()

            self.interractions()
            self.render()
            self.player.render(self.screen)
            pygame.display.update()
            self.clock.tick(60)  # Framerate

    def render(self):
        '''
        Renders the map.\n
        Map is interpreted as follows:

        ' ' = nothing, don't draw a tile\n
        '#' = wall\n
        'g' = ghost (enemy)\n
        'o' = dot (main collectible)\n
        'p' = super dot (let's you eat ghosts)\n
        'e' = ghosts spawn door (entry/exit)\n
        '''

        if self._state == "Victory":
            txt_victory = self.font_20.render("VICTORY", True, (0, 255, 0))
            txt_victory_rect = txt_victory.get_rect()
            txt_victory_rect.center = (self.map_scale[0] * self.dimensions[1] // 2, self.map_scale[1] * self.dimensions[0] // 2 + self.bars_h)
            self.screen.blit(txt_victory, txt_victory_rect)
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        if self._state == "Game Over":
            txt_game_over = self.font_20.render("Game Over", True, (255, 0, 0))
            txt_game_over_rect = txt_game_over.get_rect()
            txt_game_over_rect.center = (self.map_scale[0] * self.dimensions[1] // 2, self.map_scale[1] * self.dimensions[0] // 2 + self.bars_h)
            self.screen.blit(txt_game_over, txt_game_over_rect)
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        self.screen.fill(self.color)

        for wall_rect in self.collision_map['walls']:
            pygame.draw.rect(self.screen, self.wall_color, wall_rect)

        for gate_rect in self.collision_map['gates']:
            pygame.draw.rect(self.screen, self.gate_color, gate_rect)

        for dot in self.collision_map['dots']:
            j, i = dot[0], dot[1]

            jpos = j * self.map_scale[1]
            ipos = i * self.map_scale[0]
            self.screen.blit(self.img_dot, (j - self.dots_offset[1], i - self.dots_offset[0]))

        for ghost in self.ghosts:
            ghost.render(self.screen)

        if self._state == "Start":
            pygame.draw.rect(self.screen, self.wall_color, self.start_button_frame_rect, 4)
            self.screen.blit(self.start_button, self.start_button_rect)

        if self._state == "Playing":
            self.render_points()

        if self.draw_all_collisions:
            for raw_rect in self.collision_map['dots']:
                pygame.draw.rect(self.screen, (0, 0, 255), raw_rect, 2)

    def render_points(self):
        txt_points = self.font_20.render(f"{self.game_points}", True, (0, 180, 50))
        txt_points_rect = txt_points.get_rect()
        txt_points_rect.center = (self.map_scale[0] * self.dimensions[1] // 2, self.bars_h // 2)
        self.screen.blit(txt_points, txt_points_rect)

    def collide(self, box, tile_list):
        '''
        Returns True if box collides with tile.\n
        Parameters:\n
        Box - pygame.Rect\n
        tile - string (key for collision_map)
        '''
        for tile in tile_list:
            for raw_rect in self.collision_map[tile]:
                if pygame.Rect(raw_rect).colliderect(box):
                    return True

    def ghost_leave_box(self):
        if self.ghosts_in_box == 3:
            self.ghosts[1].set_state("Exit Mid")
            self.ghosts_in_box -= 1
        elif self.ghosts_in_box == 2:
            self.ghosts[0].set_state("Exit Left")
            self.ghosts_in_box -= 1
        elif self.ghosts_in_box == 1:
            self.ghosts[2].set_state("Exit Right")
            self.ghosts_in_box -= 1
        else:
            pygame.time.set_timer(self.RELEASE_GHOST, 0)

    # ############################## Entity Interraction ##############################

    def interractions(self):
        for tile_type, tiles in self.collision_map.items():

            if tile_type not in self.entities:
                continue

            for idx, raw_rect in enumerate(self.collision_map[tile_type]):
                if pygame.Rect(raw_rect).colliderect(self.player.hitbox):
                    self.find_and_process_interraction(tile_type, idx)
                    return

            for ghost in self.ghosts:
                prect = pygame.Rect(self.player.hitbox)
                grect = pygame.Rect(ghost.hitbox)
                if prect.colliderect(grect):
                    self._state = "Game Over"

    def find_and_process_interraction(self, tile_type, idx):
        '''
        Finds and calls the proper function to process the interraction
        '''
        if tile_type == "dots":
            self.collect_dot(idx)

    def collect_dot(self, idx):
        self.dots_total -= 1
        self.game_points += 10
        # print(self.game_points)
        del self.collision_map["dots"][idx]

    # ############################## Map Parsing ##############################
    @classmethod
    def parse(cls, mapfile):
        '''
        Parses the map. First parses the expected keywords, then the self.

        Map file general structure:
        keyword=val
        keyword=val
        etc
        maze as matrix of symbols
        '''
        data = dict()
        with open(mapfile, 'r') as f:
            for i in range(cls.parser_keywords_count):
                param, val = f.readline().split('=')
                data[param] = cls.parse_arg(cls.parser_keywords[param], val)

            if len(data) != cls.parser_keywords_count:
                raise ValueError("Parser met duplicating keywords.")

            maze = f.readlines()
            data['maze'], data['gate'], data['ghosts'] = cls.parse_maze(maze)
        return data

    @classmethod
    def parse_arg(cls, param_id, val):
        if param_id == 0:
            return cls.parse_dimensions(val)
        elif param_id == 1:
            return cls.parse_color(val)
        elif param_id == 2:
            return cls.parse_color(val)
        elif param_id == 3:
            return cls.parse_player(val)
        elif param_id == 4:
            return int(val)
        else:
            raise ValueError("param_id did not match any existing sub-parser.")

    @classmethod
    def parse_dimensions(cls, val):
        rows, cols = val.split('x')
        rows.strip()
        cols.strip()
        rows = int(rows)
        cols = int(cols)
        return (rows, cols)

    @classmethod
    def parse_color(cls, val):
        r, g, b = val.split(',')
        r.strip()
        g.strip()
        b.strip()
        r = int(r)
        g = int(g)
        b = int(b)
        return (r, g, b)

    @classmethod
    def parse_player(cls, val):
        player_row, player_col = val.split(',')
        player_row.strip()
        player_col.strip()
        player_row = int(player_row)
        player_col = int(player_col)
        return (player_row, player_col)

    @classmethod
    def parse_maze(cls, matrix):
        gate = None  # x, y of gate
        ghosts = []  # tuple of 3 tuples of x, y
        for idx, line in enumerate(matrix):
            if line == "":
                del matrix[idx]
            else:
                matrix[idx] = list(line.strip())
                if matrix[idx][-1] == '\n':
                    matrix[idx] = matrix[idx][:-1]

        cls.validate_ghost_box(matrix)

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'e':
                    gate = (i, j)
                if matrix[i][j] == 'g':
                    ghosts.append((j, i))

        return (matrix, gate, tuple(ghosts))

    @staticmethod
    def validate_ghost_box(maze):
        gate_occurances = 0
        p = None
        q = None

        for line_idx, line in enumerate(maze):
            for tile_idx, tile in enumerate(line):
                if tile == 'e':
                    gate_occurances += 1
                    p = line_idx
                    q = tile_idx
                    if (gate_occurances > 1):
                        raise ValueError("Multiple gates")

        if p > (len(maze) - 1) - 2:
            raise ValueError("Gate is too low")
        if q < 2 or q > (len(line) - 1) - 2:
            raise ValueError("No horizontal space for the box")
        if maze[p+1][q-1] != 'g' or maze[p+1][q] != 'g' or maze[p+1][q+1] != 'g':
            raise ValueError("3 ghosts beneath gate not found")
        if (
            maze[p][q-2] != '#' or
            maze[p][q-1] != '#' or
            maze[p][q+1] != '#' or
            maze[p][q+2] != '#' or

            maze[p+1][q-2] != '#' or
            maze[p+1][q+2] != '#' or

            maze[p+2][q-2] != '#' or
            maze[p+2][q-1] != '#' or
            maze[p+2][q] != '#' or
            maze[p+2][q+1] != '#' or
            maze[p+2][q+2] != '#'
        ):
            raise ValueError("Box tiling incorrect")






    # ############################## Utility ##############################
    def win_size(self):
        '''
        Returns a tuple with the perfect-fit size for the window that will display the level.

        '''
        return (self.map_scale[0] * self.dimensions[1],
                self.map_scale[1] * self.dimensions[0] + (2 * self.bars_h))




    # ############################## Debug ##############################
    def enable_collision_rendering(self, val=True):
        self.draw_all_collisions = val
        self.player.enable_collision_rendering(val)

