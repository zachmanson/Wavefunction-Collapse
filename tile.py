import pygame as pg

class Tile:
    def __init__(self, img, connections, entropy, from_file = True):
        if from_file:
            self.img = pg.image.load(img)
        else:
            self.img = img
            
        self.connections = connections
        self.collapsed = False
        self.entropy = entropy
        self.options = None

    def get_img(self):
        return self.img

    def get_connections(self):
        return self.connections

    '''
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    '''

    def get_connections(self):
        return self.connections

    def get_collapsed(self):
        return self.collapsed

    def get_entropy(self):
        return self.entropy

    def get_options(self):
        return self.options

    def set_img_from_file(self, img):
        self.img = pg.image.load(img)

    def set_img(self, img):
        self.img = img

    '''
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
    '''

    def set_connections(self, connections):
        self.connections = connections

    def set_collapsed(self, collapsed):
        self.collapsed = collapsed

    def set_entropy(self, entropy):
        self.entropy = entropy

    def set_options(self, options):
        self.options = options

    def __repr__(self) -> str:
        return "{}".format(self.connections)