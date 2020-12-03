import pygame as pg

from os.path import join

path_blocks = join("assets", "Blocks")
path_flames = join("assets", "Flame")
path_bombs = join("assets", "Bomb")


class Tile(pg.sprite.Sprite):

    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Grass(Tile):

    def __init__(self):
        Tile.__init__(self, pg.image.load(
            join(path_blocks, "BackgroundTile.png")))


class Explodable(Tile):

    def __init__(self):
        Tile.__init__(self, pg.image.load(
            join(path_blocks, "ExplodableBlock.png")))


class Solid(Tile):

    def __init__(self):
        Tile.__init__(self, pg.image.load(join(path_blocks, "SolidBlock.png")))


class Portal(Tile):

    def __init__(self):
        Tile.__init__(self, pg.image.load(join(path_blocks, "Portal.png")))


class Flame(Tile):

    def __init__(self):
        self.images = []
        self.position = 0
        self.count_down = 100
        for i in range(5):
            self.images.append(pg.image.load(
                join(path_flames, "Flame_f0" + str(i) + ".png")))

        Tile.__init__(self, self.images[self.position])

    def animate(self):

        # Change image in order to generate animations
        if self.position == len(self.images) - 1:
           self.position = 0

        self.image = self.images[self.position]
        self.position += 1


class Bomb(Tile):

    def __init__(self):
        Tile.__init__(self, pg.image.load(join(path_bombs, "Bomb_f01.png")))
        self.count_down = 100
        self.explodables = []

    def find_position_explodable(self, objects):
        for x, row in enumerate(objects):
            for i, column in enumerate(row):
                if isinstance(column, (Explodable)):
                    """
                        Move the bomb around and check
                        if there is a collision on explodables

                        change self.rect.y and self.rect.x, check collision
                        and return it to the original position
                    """
                    self.rect.y -= 10
                    if column.rect.colliderect(self):
                        self.explodables.append({"row": x, "column": i})

                    self.rect.y += 50
                    if column.rect.colliderect(self):
                        self.explodables.append({"row": x, "column": i})

                    # Original position self.rect.y -= 40
                    self.rect.y -= 40
                    self.rect.x -= 10
                    if column.rect.colliderect(self):
                        self.explodables.append({"row": x, "column": i})

                    self.rect.x += 30
                    if column.rect.colliderect(self):
                        self.explodables.append({"row": x, "column": i})

                    # Original position self.rect.x -= 20
                    self.rect.x -= 20

SCREEN_WIDTH = 765
SCREEN_HEIGHT = 570

tilemap = [
    [Grass(), Explodable(), Explodable(), Explodable(), Explodable(), Explodable(), Explodable(), Solid()     , Solid()     , Solid()     , Solid()     , Solid()],
    [Grass(), Grass()     , Grass()     , Grass()     , Grass()     , Grass()     , Grass()     , Explodable(), Grass()     , Grass()     , Grass()     , Solid()],
    [Grass(), Grass()     , Solid()     , Explodable(), Explodable(), Explodable(), Explodable(), Solid()     , Grass()     , Grass()     , Grass()     , Solid()],
    [Solid(), Grass()     , Solid()     , Grass()     , Grass()     , Grass()     , Grass()     , Solid()     , Explodable(), Explodable(), Explodable(), Solid()],
    [Solid(), Grass()     , Solid()     , Grass()     , Grass()     , Grass()     , Grass()     , Explodable(), Grass()     , Grass()     , Grass()     , Solid()],
    [Solid(), Grass()     , Explodable(), Solid()     , Solid()     , Solid()     , Solid()     , Solid()     , Solid()     , Explodable(), Explodable(), Solid()],
    [Solid(), Grass()     , Explodable(), Grass()     , Grass()     , Explodable(), Grass()     , Grass()     , Solid()     , Grass()     , Grass()     , Grass()],
    [Solid(), Grass()     , Explodable(), Grass()     , Grass()     , Grass()     , Explodable(), Grass()     , Explodable(), Grass()     , Grass()     , Grass()],
    [Solid(), Grass()     , Explodable(), Grass()     , Grass()     , Grass()     , Grass()     , Explodable(), Grass()     , Grass()     , Grass()     , Portal()]]
