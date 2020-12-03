import random
import sys
import pygame as pg

from tilemap import (tilemap,
                     Explodable,
                     Solid,
                     Grass,
                     Bomb,
                     Flame,
                     Portal)
from tilemap import SCREEN_HEIGHT, SCREEN_WIDTH
from objects import Bomberman, Creep

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

clock = pg.time.Clock()


def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Bomberman")
    font = pg.font.SysFont("Comic Sans MS", 50)

    # Load bomberman, creep
    bomberman = Bomberman()
    creep = Creep()
    portal = Portal()

    def build_tiles():

        indexX = 0
        indexY = 0
        grass = Grass()
        for row in tilemap:
            indexX = 0
            for column in row:
                column.update(indexX, indexY)
                screen.blit(grass.image, column.rect)
                screen.blit(column.image, column.rect)
                if isinstance(column, (Portal)):
                    portal.rect = column.rect
                indexX += 64
            indexY += 64

    def check_exist_explodables():
        for row in tilemap:
            for column in row:
                if isinstance(column, (Explodable)):
                    return True

    # Fill background in case of game over or victory
    s = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    s.set_alpha(128)
    s.fill((BLACK))

    #Build tiles
    build_tiles()

    # Move creep to initial position
    creep.control(650, 510)
    creep.update()

    # Initial set up
    screen.blit(bomberman.image, bomberman.rect)
    screen.blit(creep.image, creep.rect)
    pg.display.flip()

    """
        step: distance characters move
        cycle: how many steps creep will move
        randon_keys: creep moves up, down, right or left randomically
    """
    step, cycle = 4, 0
    is_running, is_game_over, is_game_win, is_key_down = True, False, False, False
    randon_keys = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]
    bombs, flames = [], []
    while(is_running):

        # Check if any bomb is on map
        for i, bomb in enumerate(bombs):
            screen.blit(bomb.image, bomb.rect)
            bombs[i].count_down = bomb.count_down - 1
            # count_down is the time bombs will exist
            if bomb.count_down == 0:
                # Replace a bomb by a flame
                flame = Flame()
                flame.update(bomb.rect.x, bomb.rect.y)
                flames.append(flame)
                bombs.pop(i)
                # Replace an explodable block by a flame if the bomb explode it
                for explodables in bomb.explodables:
                    flame = Flame()
                    flame.update(tilemap[explodables["row"]][explodables["column"]].rect.x,
                                 tilemap[explodables["row"]][explodables["column"]].rect.y)
                    tilemap[explodables["row"]
                            ][explodables["column"]] = Grass()
                    flames.append(flame)

        # Check flames
        for i, flm in enumerate(flames):
            screen.blit(flm.image, flm.rect)
            flames[i].count_down = flm.count_down - 1
            flm.animate()
            # count_down is the time flames will exist
            if flm.count_down == 0:
                flames.pop(i)

        if cycle == 0:
            # direc is the direction where creep will move
            direc = random.choice(randon_keys)
            cycle = 20
            x, y = 0, 0

        if direc == pg.K_LEFT:
            x = -step
        elif direc == pg.K_RIGHT:
            x = step
        elif direc == pg.K_DOWN:
            y = step
        else:
            y = -step

        cycle -= 1
        creep.control(y=y, x=x, direction=direc)
        # creep does not check collisions
        #creep.update(objects=tilemap)
        creep.update()
        screen.blit(creep.image, creep.rect)
        screen.blit(bomberman.image, bomberman.rect)
        pg.display.flip()
        build_tiles()

        # Game over if creep collides with bomberman
        if creep.collide_with_bomberman(bomberman) or is_game_over:
            if not is_game_win:
                label = font.render("GAME OVER", 1, YELLOW)
                screen.blit(label, (230, 230))
                screen.blit(s, (0, 0))
                is_game_over = True
                is_key_down = False

        # Victory if bomberman touches portal and all explodables do not exist
        if bomberman.collide_with_portal(portal):
            if not check_exist_explodables():
                label = font.render("VICTORY !!!", 1, YELLOW)
                screen.blit(label, (230, 230))
                screen.blit(s, (0, 0))
                is_game_win = True
                is_key_down = False

        # Game over if collision with flame
        if bomberman.collide_with_flame(flames):
            if not is_game_win:
                label = font.render("GAME OVER", 1, YELLOW)
                screen.blit(label, (230, 230))
                screen.blit(s, (0, 0))
                is_game_over = True
                is_key_down = False

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                is_running = False
                sys.exit(0)

            if event.type == pg.KEYUP:
                is_key_down = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    is_running = False
                    sys.exit(0)

                if not is_game_over and not is_game_win:

                    if event.key == pg.K_RIGHT:
                        is_key_down = True
                        bomberman.control(x=step, direction=pg.K_RIGHT)

                    if event.key == pg.K_LEFT:
                        is_key_down = True
                        bomberman.control(x=-step, direction=pg.K_LEFT)

                    if event.key == pg.K_DOWN:
                        is_key_down = True
                        bomberman.control(y=step, direction=pg.K_DOWN)

                    if event.key == pg.K_UP:
                        is_key_down = True
                        bomberman.control(y=-step, direction=pg.K_UP)

                    if event.key == pg.K_x:
                        # Create new bomb
                        bomb = Bomb()
                        obj = bomberman.find_position_bomb(objects=tilemap)
                        bomb.update(obj.rect.x, obj.rect.y)
                        bomb.find_position_explodable(objects=tilemap)
                        bombs.append(bomb)

        clock.tick(30)  # FPS
        if is_key_down:
            bomberman.update(objects=tilemap)
            screen.blit(creep.image, creep.rect)
            screen.blit(bomberman.image, bomberman.rect)


if __name__ == "__main__":
    main()