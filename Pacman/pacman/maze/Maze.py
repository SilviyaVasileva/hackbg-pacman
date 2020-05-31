import pygame
import sys
import time


class Maze:

    # ######################### Static Data #########################
    # The keywords required for a map to be parsed
    parser_keywords = {
        'dimensions': 0,
        'color': 1,
        'walls': 2,
        'player': 3,
        'total': 4
    }
    parser_keywords_count = len(parser_keywords)

    # ######################### Setups and Properties #########################
    def __init__(self, mapfile, player):
        self.collision_map = {
            "walls": [],
            "dots": [],
            "power_dots": [],
            "ghost_gate": [],
            "ghosts": []
        }
        self.clock = pygame.time.Clock()

        self.map_scale = (42, 42)

        init_data = self.__class__.parse(mapfile)
        self.dimensions = init_data['dimensions']
        self.color = init_data['color']
        self.wall_color = init_data['walls']
        self.player_start = init_data['player']
        self.maze = init_data['maze']

        self.build_walls()

    # ######################### Movement and Rendering #########################
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

        for wall_rect in self.collision_map['walls']:
            pygame.draw.rect(screen, self.wall_color, wall_rect)

    def build_walls(self):
        '''
        Builds the maze.\n
        '''

        for i, row in enumerate(self.maze):
            i *= self.map_scale[1]
            for j, pos in enumerate(row):
                j *= self.map_scale[0]
                if pos == '#':
                    self.collision_map['walls'].append(tuple(
                        [j, i, self.map_scale[0], self.map_scale[1]]
                        ))
    
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
            return val
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
                self.map_scale[1] * self.dimensions[0])
