"""
Based on Paul Vincent Craven code
http://simpson.edu/author/pcraven-2/
"""

import pygame
import argparse
import numpy as np

from objects import Base, Mine, Wall
from player import Player

"""
Global constants
"""

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED	     = (   255,   0, 0)
GREEN    = (   0,   255, 0)
YELLOW   = ( 255,   255, 0)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

# Arguments
parser = argparse.ArgumentParser()

parser.add_argument("-r","--robots", type=int, default=1,
                    help="Number of robots that there will be in the game (default: 1).")

parser.add_argument("-rs","--robotstrategy", choices=[1,2,3,4], default=1,
                    help="Define robot strategy (default: 1).")

parser.add_argument("-m","--mines", type=int, default=8,
                    help="Number of mines that there will be in the game (default: 8).")

args = parser.parse_args()

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('Test')

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

# Left
wall = Wall(0, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

# Right
wall = Wall(790, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)

# Top
wall = Wall(10, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# Botton
wall = Wall(10, 590, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# wall = Wall(10, 200, 100, 10)
# wall_list.add(wall)
# all_sprite_list.add(wall)

# Base
base_x = np.random.randint(10,SCREEN_WIDTH-60)
base_y = np.random.randint(10,SCREEN_HEIGHT-60)

base = Base(base_x, base_y, 50, 50, RED)
all_sprite_list.add(base)

mines = []

# Minas
for i in range(args.mines):
    mina_x = np.random.randint(10,SCREEN_WIDTH-35)
    mina_y = np.random.randint(10,SCREEN_HEIGHT-35)

    while (not (mina_x < base_x or mina_x > (base_x+50))):
        mina_x = np.random.randint(10,SCREEN_WIDTH-35)

    while (not (mina_y < base_y or mina_y > (base_y+50))):
        mina_y = np.random.randint(10,SCREEN_HEIGHT-35)

    gold = np.random.randint(0,100)
    mina = Mine(i, mina_x, mina_y, 25, 25, gold, YELLOW)
    print 'mine', i, mina_x, mina_y, gold

    mines.append(mina)

    all_sprite_list.add(mina)
print len(mines), "mines created"

# Create players objects
players = []

for i in range(args.robots):
    player = Player(i, 10, 10, base, mines)
    player.walls = wall_list
    all_sprite_list.add(player)
    players.append(player)

clock = pygame.time.Clock()

done = False

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        # elif event.type == pygame.KEYDOWN:

        #     if event.key == pygame.K_LEFT:
        #         player.changespeed(-3, 0)
        #     elif event.key == pygame.K_RIGHT:
        #         player.changespeed(3, 0)
        #     elif event.key == pygame.K_UP:
        #         player.changespeed(0, -3)
        #     elif event.key == pygame.K_DOWN:
        #         player.changespeed(0, 3)

        # elif event.type == pygame.KEYUP:

        #     if event.key == pygame.K_LEFT:
        #         player.changespeed(3, 0)
        #     elif event.key == pygame.K_RIGHT:
        #         player.changespeed(-3, 0)
        #     elif event.key == pygame.K_UP:
        #         player.changespeed(0, 3)
        #     elif event.key == pygame.K_DOWN:
        #         player.changespeed(0, -3)
        
    # print player.rect.x, player.rect.y

    possibility = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

    if (player.rect.x <= 10 or player.rect.x < 0):
        try:
            possibility.remove((-1,-1))
        except:
            pass
        try:
            possibility.remove((-1,0))
        except:
            pass
        try:
            possibility.remove((-1,1))
        except:
            pass
    elif (player.rect.x >= SCREEN_WIDTH-30):
        try:
            possibility.remove((1,-1))
        except:
            pass
        try:
            possibility.remove((1,0))
        except:
            pass
        try:
            possibility.remove((1,1))
        except:
            pass
    if (player.rect.y <= 10 or player.rect.y < 0):
        try:
            possibility.remove((-1,-1))
        except:
            pass
        try:
            possibility.remove((0,-1))
        except:
            pass
        try:
            possibility.remove((1,-1))
        except:
            pass
    elif (player.rect.y >= SCREEN_HEIGHT-30):
        try:
            possibility.remove((-1,1))
        except:
            pass
        try:
            possibility.remove((0,1))
        except:
            pass
        try:
            possibility.remove((1,1))
        except:
            pass

    # print len(possibility)
    op = np.random.randint(len(possibility))
    player.changespeed(possibility[op][0],possibility[op][1])


    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
