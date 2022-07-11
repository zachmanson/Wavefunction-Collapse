import pygame as pg
import grid
from grid import Grid

WIDTH = HEIGHT = 512
DIM = grid.DIM
SQ_SIZE = HEIGHT // DIM


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("grey"))

    the_grid = Grid()
    running = True
    c = 0
    while(running):
        c = c + 1
        for event in pg.event.get():
            if event.type == pg.QUIT:   
                running = False

        draw_grid(screen, the_grid)
        if(c <= DIM * DIM - 1):
            the_grid.update_grid()
        pg.display.flip()
        
    
def draw_grid(screen, g):
    for col in range(DIM):
        for row in range(DIM):
            tile_img = g.tile_grid[col][row].get_img()
            if tile_img != None:
                transformed_img = pg.transform.scale(tile_img, (SQ_SIZE, SQ_SIZE))
                screen.blit(transformed_img, pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()