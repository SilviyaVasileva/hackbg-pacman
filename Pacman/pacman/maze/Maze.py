import pygame
import sys
import time


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

    # =============== Top and bottom scale offset ===============
    TOP_BOTTOM_OFFSET = 60

    # ######################### Setups and Properties #########################
    def __init__(self, mapfile, player):
        # =============== Configs ===============
        self.clock = pygame.time.Clock()
        self.map_scale = (36, 36)
        
        # =============== Automatic Image Loading ===============
        img_dot = pygame.image.load(f"{Maze.COLLECTIBLES}/dots/dot.png")
        self.img_dot = pygame.transform.scale(img_dot, self.map_scale)

        # =============== Entity Custom Scale ===============
        self.dots_scale = (10, 10)
        self.dots_offset = ((self.map_scale[0]- self.dots_scale[0]) // 2, (self.map_scale[1] - self.dots_scale[1]) // 2)

        # =============== Matrix ===============
        self.collision_map = {
            "walls": [],
            "dots": [],
            "power_dots": [],
            "ghost_gate": [],
            "ghosts": []
        }
        self.entities = [
            "dots",
            "power_ups",
            "ghost_gate", 
            "ghosts"
        ]

        # =============== Maze data ===============
        init_data = self.__class__.parse(mapfile)
        self.dimensions = init_data['dimensions']
        self.color = init_data['color']
        self.wall_color = init_data['walls']
        self.player_start = init_data['player']
        self.maze = init_data['maze']
        self.player = player
        self.dots_total = init_data['total']

        # =============== Auto Init Commands ===============
        self.build()

        # =============== Debug vars ===============
        self.draw_all_collisions = False

        # =============== Start game ===============
        self.start_game = False

        # =============== Game points ===============
        self.game_points = 0

    def place_player(self, screen):
        self.player.pos['x'] = self.player_start[0]*self.map_scale[0]
        self.player.pos['y'] = self.player_start[1]*self.map_scale[1] + 60
        self.player.update_collision()
        self.player.render(screen)

    def start(self, screen):
        self.display_points(screen)

    # ######################### State #########################
    def render(self, screen):
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

        screen.fill(self.color)

        button_coord = (self.map_scale[0] * self.dimensions[1] // 2 - 35,
                self.map_scale[1] * self.dimensions[0] +  70,
                70, 40)
        self.start_button(screen, (188, 188, 188), button_coord)

        for wall_rect in self.collision_map['walls']:
            pygame.draw.rect(screen, self.wall_color, wall_rect)

        for dot in self.collision_map['dots']:
            j, i = dot[0], dot[1]

            jpos = j * self.map_scale[1]
            ipos = i * self.map_scale[0]
            screen.blit(self.img_dot, (j - self.dots_offset[1], i - self.dots_offset[0]))

        if self.draw_all_collisions:
            for raw_rect in self.collision_map['dots']:
                pygame.draw.rect(screen, (0, 0, 255), raw_rect, 2)

    def build(self):
        '''
        Builds the 'collision_map' variable.\n
        It contains tuples with raw pygame.Rect data to be used for rendering.
        '''

        for i, row in enumerate(self.maze):
            i *= self.map_scale[1]
            i += 60   # TOP_BOTTOM_OFFSET
            for j, pos in enumerate(row):
                j *= self.map_scale[0]
                if pos == '#':
                    self.collision_map['walls'].append(tuple(
                        [j, i, self.map_scale[0], self.map_scale[1]]  # creates tuple with raw pygame.Rect data
                        ))
                if pos == 'o':
                    self.collision_map["dots"].append(tuple(
                        [j + self.dots_offset[0], i + self.dots_offset[1], self.dots_scale[0], self.dots_scale[1]]  # creates tuple with raw pygame.Rect data
                    ))

    def collide(self, box, tile):
        '''
        Returns True if box collides with tile.\n
        Parameters:\n
        Box - pygame.Rect\n
        tile - string (key for collision_map)
        '''
        for raw_rect in self.collision_map[tile]:
            if pygame.Rect(raw_rect).colliderect(box):
                return True

    # ############################## Entity Interraction ##############################
    def interractions(self):
        for tile_type, tiles in self.collision_map.items():

            if tile_type not in self.entities:
                continue

            for idx, raw_rect in enumerate(self.collision_map[tile_type]):
                if pygame.Rect(raw_rect).colliderect(self.player.hitbox):
                    self.find_and_process_interraction(tile_type, idx)
                    return

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
        Parses the map. First parses the expected keywords, then the dungeon.

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
            data['maze'] = cls.parse_maze(maze)
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
        for idx, line in enumerate(matrix):
            if line == "":
                del matrix[idx]
            else:
                matrix[idx] = list(line.strip())
                if matrix[idx][-1] == '\n':
                    matrix[idx] = matrix[idx][:-1]
        return matrix

    # ############################## Utility ##############################
    def win_size(self):
        '''
        Returns a tuple with the perfect-fit size for the window that will display the level.

        '''
        return (self.map_scale[0] * self.dimensions[1],
                self.map_scale[1] * self.dimensions[0] + 2 * 60) #  TOP_BOTTOM_OFFSET)

    # ############################## Debug ##############################
    def enable_collision_rendering(self, val=True):
        self.draw_all_collisions = val
        self.player.enable_collision_rendering(val)

    # ############################## Draw button ##############################
    def start_button(self, screen, button_color, coord):
        pygame.draw.rect(screen, button_color, coord)
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects("GO!", smallText)
        textRect.center = ((coord[0] + (coord[2] // 2)), (coord[1] + (coord[3] // 2)))
        screen.blit(textSurf, textRect)
        if not self.start_game:
            self.start_game = self.button_click(coord)
        else:
            self.start(screen)
        # pygame.display.update()

    # ############################## Draw button text ##############################
    def button_click(self, coord):
        # mouse movement
        mouse_coord = pygame.mouse.get_pos()

        if coord[0] + coord[2] > mouse_coord[0] > coord[0] and coord[1] + coord[3] > mouse_coord[1] > coord[3]:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                return True
            # print(mouse_click)
        # print(mouse_coord)
        return False

    # ############################## Draw button text ##############################
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 180, 50))
        return textSurface, textSurface.get_rect()

    # ############################## Display points ##############################
    def display_points(self, screen):
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(str(self.game_points), smallText)
        textRect.center = (30, 30)
        screen.blit(textSurf, textRect)
        # print(str(self.game_points))

    # ############################## Print lifes ##############################
    def hearts(self):
        pass
