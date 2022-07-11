from audioop import reverse
import random
from tile import Tile
import numpy as np
import pygame as pg

DIM = 30
TILES_TO_LOAD = [
    Tile('images/0.png', [1, 1, 1, 1], entropy = 0, from_file=True),
    Tile('images/1.png', [1, 0, 0, 0], entropy = 0, from_file=True),
    Tile('images/2.png', [1, 0, 1, 0], entropy = 0, from_file=True),
    Tile('images/3.png', [1, 1, 0, 0], entropy = 0, from_file=True),
    Tile('images/4.png', [0, 0, 0, 0], entropy = 0, from_file=True),
    Tile('images/5.png', [0, 1, 1, 1], entropy = 0, from_file=True),
    Tile('images/6.png', [0, 1, 0, 1], entropy = 0, from_file=True),
    Tile('images/7.png', [0, 0, 1, 1], entropy = 0, from_file=True),
]


# circuit samples, WIP
'''
TILES_TO_LOAD = [
    Tile('images/circuit/bridge.png', [121, 131, 121, 131], entropy = 0, from_file=True),
    Tile('images/circuit/component.png', [444, 444, 444, 444], entropy = 0, from_file=True),
    Tile('images/circuit/connection.png', [121, 114, 444, 114], entropy = 0, from_file=True),
    Tile('images/circuit/corner.png', [111, 411, 114, 111], entropy = 0, from_file=True),
    Tile('images/circuit/dskew.png', [121, 121, 121, 121], entropy = 0, from_file=True),
    Tile('images/circuit/skew.png', [121, 121, 111, 111], entropy = 0, from_file=True),
    Tile('images/circuit/substrate.png', [111, 111, 111, 111], entropy = 0, from_file=True),
    Tile('images/circuit/t.png', [111, 121, 121, 121], entropy = 0, from_file=True),
    Tile('images/circuit/track.png', [121, 111, 121, 111], entropy = 0, from_file=True),
    Tile('images/circuit/transition.png', [131, 111, 121, 111], entropy = 0, from_file=True),
    Tile('images/circuit/turn.png', [121, 121, 111, 111], entropy = 0, from_file=True),
    Tile('images/circuit/viad.png', [111, 121, 111, 121], entropy = 0, from_file=True),
    Tile('images/circuit/vias.png', [131, 111, 111, 111], entropy = 0, from_file=True),
    Tile('images/circuit/wire.png', [111, 131, 111, 131], entropy = 0, from_file=True),
]
'''


def rotate_array(arr, r):
    n = len(arr)
    arr = arr[-r:] + arr[:-r]
    return arr

def reverse_number(n):
    reversed = 0
    while n != 0:
        digit = n % 10
        reversed = reversed * 10 + digit
        n //= 10

    return reversed

class Grid:
    def __init__(self):
        self.possible_tiles = self.get_possible_tiles(TILES_TO_LOAD)
        self.tile_grid = [[Tile(None, None, entropy = len(self.possible_tiles), from_file = False) for x in range(DIM)] for y in range(DIM)]

        # pick a starting tile randomly
        ini_row, ini_col, ini_tile = self.pick_start_tile(self.possible_tiles)
        self.tile_grid[ini_row][ini_col] = self.possible_tiles[ini_tile]
        self.tile_grid[ini_row][ini_col].collapsed = True

    def pick_start_tile(self, pt):
        
        start_row = random.randint(0, DIM - 1)
        start_col = random.randint(0, DIM - 1)
        start_tile = random.randint(0, len(pt) - 1)
        return start_row, start_col, start_tile

    def get_possible_tiles(self, tile_arr):
        rot_tiles = []
        for t in tile_arr:
            curr_img = t.get_img()
            curr_connections = t.get_connections()
            for i in range(1, 4):
                new_img = pg.transform.rotate(curr_img, -90 * i)
                
                if i > 2:
                    new_connections = [reverse_number(x) for x in rotate_array(curr_connections, i)]
                else:
                    new_connections = rotate_array(curr_connections, i)
                

                rot_tiles.append(Tile(new_img, new_connections, entropy = 0, from_file=False))
        
        return tile_arr + rot_tiles

    def test_images(self, index):
        t = TILES_TO_LOAD[index]
        self.tile_grid[0][0] = t
        print(self.tile_grid[0][0].get_connections()) 

    def print_entropy(self):
        print([[self.tile_grid[col][row].get_entropy() for col in range(DIM)] for row in range(DIM)])

    def print_collapsed(self):
        print([[self.tile_grid[col][row].get_collapsed() for col in range(DIM)] for row in range(DIM)])

    def neighbours(self, c, r):
        pn = [(c, r-1), (c, r + 1), (c-1, r), (c+1, r)]
        for i, t in enumerate(pn):
            if t[0] < 0 or t[1] < 0 or t[0] >= DIM or t[1] >= DIM:
                pn[i] = None
        return [c for c in pn if c is not None]

    def get_valid_neighbours(self, c, r):
        n = self.neighbours(c, r)
        return [(x, y) for x, y in n if not self.tile_grid[x][y].get_collapsed()]

    def calculate_entropy(self):
        #find all tiles that are next to collapsed ones
        candidates = []
        for c in range(DIM):
            for r in range(DIM):
                if not self.tile_grid[c][r].get_collapsed() and any(self.tile_grid[xc][xr].get_collapsed() for xc, xr in self.neighbours(c, r)):
                    candidates += [(c, r)]


        for cx, cy in candidates:
            options = []
            collapsed_nbrs = [(tx, ty) for tx, ty in self.neighbours(cx, cy) if self.tile_grid[tx][ty].get_collapsed()]
            for ix, iy in collapsed_nbrs:
                temp = self.calculate_options((cx, cy), (ix, iy))
                if len(options) == 0:
                    options += temp
                else:
                    options = [x for x in options if x in temp]
            
            if len(options) == 0:
                self.restart()

            self.tile_grid[cx][cy].set_entropy(len(options))
            self.tile_grid[cx][cy].set_options(options)


    def calculate_options(self, curr_pos, nbrs_pos):
        # if neighbour is up
        if nbrs_pos[0] == curr_pos[0] and nbrs_pos[1] < curr_pos[1]:
            nbx, nby = nbrs_pos
            return [t for t in self.possible_tiles if t.get_connections()[0] == reverse_number(self.tile_grid[nbx][nby].get_connections()[2])]
        # if neighbour is right
        if nbrs_pos[0] > curr_pos[0] and nbrs_pos[1] == curr_pos[1]:
            nbx, nby = nbrs_pos
            return [t for t in self.possible_tiles if t.get_connections()[1] == reverse_number(self.tile_grid[nbx][nby].get_connections()[3])]
        # if neighbour is down
        if nbrs_pos[0] == curr_pos[0] and nbrs_pos[1] > curr_pos[1]:
            nbx, nby = nbrs_pos
            return [t for t in self.possible_tiles if t.get_connections()[2] == reverse_number(self.tile_grid[nbx][nby].get_connections()[0])]
        #if neighbour is left
        if nbrs_pos[0] < curr_pos[0] and nbrs_pos[1] == curr_pos[1]:
            nbx, nby = nbrs_pos
            return [t for t in self.possible_tiles if t.get_connections()[3] == reverse_number(self.tile_grid[nbx][nby].get_connections()[1])]


    def find_lowest_entropy(self):
        e = 1000
        for c in range(DIM):
            for r in range(DIM):
                temp = self.tile_grid[c][r].get_entropy()
                if temp < e and not self.tile_grid[c][r].get_collapsed():
                    e = temp
        return e

    def update_grid(self):
        self.calculate_entropy()
        #first find the lowest entropy in the gird
        lowest_ent = self.find_lowest_entropy()
        lowest_ent_tiles = []
        grid_copy = self.tile_grid
        for c in range(DIM):
            for r in range(DIM):
                if grid_copy[c][r].get_entropy() == lowest_ent and not grid_copy[c][r].get_collapsed():
                    lowest_ent_tiles.append((c, r))

        tile_to_update = random.choice(lowest_ent_tiles)
        uc, ur = tile_to_update
        
        new_tile = random.choice(self.tile_grid[uc][ur].get_options())
        self.tile_grid[uc][ur] = new_tile
        self.tile_grid[uc][ur].collapsed = True

    def restart(self):
        self.tile_grid = [[Tile(None, None, entropy = len(self.possible_tiles), from_file = False) for x in range(DIM)] for y in range(DIM)]

        # pick a starting tile randomly
        ini_row, ini_col, ini_tile = self.pick_start_tile(self.possible_tiles)
        self.tile_grid[ini_row][ini_col] = self.possible_tiles[ini_tile]
        self.tile_grid[ini_row][ini_col].collapsed = True
