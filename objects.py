from tilemap import Explodable , Solid , Grass , SCREEN_WIDTH , SCREEN_HEIGHT

import pygame as pg

from os.path import join 

path_bomberman = join("assets" , "Bomberman")
path_creep = join("assets" , "Creep")

class Character(pg.sprite.Sprite):

    def __init__(self , materials):
        pg.sprite.Sprite.__init__(self)
        self.materials = materials
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.position = 0
        self.images = []
        self.direction = pg.K_DOWN # Default position
        self.set_up()
        self.rect  = self.image.get_rect()
    
    def set_up(self):
        self.images = []
        """
        x: 0 = K_DOWN
        x: 1 = K_UP
        x: 2 = RIGHT
        x: 3 = LEFT
        """
        if self.direction == pg.K_DOWN:
               self.images = self.materials[0]
        elif self.direction == pg.K_UP:
               self.images = self.materials[1]
        elif self.direction == pg.K_RIGHT:
               self.images = self.materials[2]
        elif self.direction == pg.K_LEFT:
               self.images = self.materials[3]

        self.image = self.images[self.position]

    def collide(self , other_sprites):

        for rows in other_sprites:
            for column in rows:
                col = self.rect.colliderect(column)
                if col:
                    if isinstance(column , (Explodable , Solid)):
                        return column

    def control(self , x=0 , y=0 , direction=pg.K_DOWN):
        self.direction = direction
        self.set_up()
        self.movex = x
        self.movey = y
        
        
    def update(self , objects=[[]]):
        # Check collision only for explodables and solid
        col = self.collide(objects)

        # Decide direction where character can move
        if col:
            if self.movex != 0:
                if col.rect.x > self.rect.x:
                    if self.movex < 0:
                        self.rect.x += self.movex
                if col.rect.x < self.rect.x:
                    if self.movex > 0:
                        self.rect.x += self.movex
            elif self.movey != 0:
                if col.rect.y > self.rect.y:
                    if self.movey < 0:
                        self.rect.y += self.movey
                if col.rect.y < self.rect.y:
                    if self.movey > 0:
                        self.rect.y += self.movey
        else:
            self.rect.x += self.movex
            self.rect.y += self.movey

        # Check if character is out of screen bounds
        if self.rect.x > SCREEN_WIDTH + 5:
            self.rect.x = -50
        elif self.rect.x < -50:
            self.rect.x = SCREEN_WIDTH - 5  

        if self.rect.y > SCREEN_HEIGHT - 20:
            self.rect.y = -50
        elif self.rect.y < -50:
            self.rect.y = SCREEN_HEIGHT - 20

        if self.movex > 0:
            self.frame += 10
            if self.frame > 10:
                self.frame = 0

        if self.position == len(self.images) - 1:
            self.position = 0
    
        self.image = self.images[self.position]
        self.position += 1

class Bomberman(Character):

    def __init__(self):
        """
        x: 0 = K_DOWN
        x: 1 = K_UP
        x: 2 = RIGHT
        x: 3 = LEFT
        """
        materials = [[None for i in range(8)] for j in range(4)]
        for x , row in enumerate(materials):
            for i , column in enumerate(row):
                if x == 0:
                    column = pg.image.load( join(path_bomberman , "Front" , "Bman_F_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (40,40))
                elif x == 1:
                    column = pg.image.load( join(path_bomberman , "Back" , "Bman_B_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (40,40))
                elif x == 2:
                    column = pg.image.load( join(path_bomberman , "Side" , "Bman_F_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (40,40))
                elif x == 3:
                    column = pg.image.load( join(path_bomberman , "Side" , "Bman_F_f0" + str(i) + ".png")).convert_alpha()
                    column = pg.transform.scale(column , (40,40))
                    materials[x][i] = pg.transform.flip(column , True , False)

        Character.__init__(self , materials)
        
    def find_position_bomb(self , objects):
        for row in objects:
            for column in row:
                col = self.rect.colliderect(column)
                if col:
                    if isinstance(column , (Grass)):
                        return column

    def collide_with_portal(self , portal):
        if self.rect.colliderect(portal):
            return True

    def collide_with_flame(self , flames):
        for flame in flames:
            if self.rect.colliderect(flame):
                return True

class Creep(Character):

    def __init__(self):
        """
        x: 0 = K_DOWN
        x: 1 = K_UP
        x: 2 = RIGHT
        x: 3 = LEFT
        """
        materials = [[None for i in range(6)] for j in range(4)]
        for x , row in enumerate(materials):
            for i , column in enumerate(row):
                if x == 0:
                    column = pg.image.load( join(path_creep , "Front" , "Creep_F_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (55,55))
                elif x == 1:
                    column = pg.image.load( join(path_creep , "Back" , "Creep_B_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (55,55))
                elif x == 2:
                    column = pg.image.load( join(path_creep , "Side" , "Creep_S_f0" + str(i) + ".png")).convert_alpha()
                    materials[x][i] = pg.transform.scale(column , (55,55))
                elif x == 3:
                    column = pg.image.load( join(path_creep , "Side" , "Creep_S_f0" + str(i) + ".png")).convert_alpha()
                    column = pg.transform.scale(column , (55,55))
                    materials[x][i] = pg.transform.flip(column , True , False)

        Character.__init__(self , materials)
        
    def collide_with_bomberman(self , bomberman):
        if self.rect.colliderect(bomberman):
            return True   
