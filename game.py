"""
Based on Paul Vincent Craven code
http://simpson.edu/author/pcraven-2/
"""

import pygame, math, sys
import argparse
import numpy as np

from time import time

from objects import Base, Mine, Wall
from player import Player1, Player2, Player3, Player4

from collections import defaultdict

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

def inside(player, obj):

    inside_x = (obj.rect.x <= player.rect.x and obj.rect.x+obj.rect.width >= player.rect.x)
    inside_y = (obj.rect.y <= player.rect.y and obj.rect.y+obj.rect.height >= player.rect.y)

    return (inside_x and inside_y)

# Arguments
parser = argparse.ArgumentParser()

parser.add_argument("-r","--robots", type=int, default=1,
                    help="Number of robots that there will be in the game (default: 1).")

parser.add_argument("-rs","--robotstrategy", choices=['1','2','3','4'], default=1,
                    help="Define robot strategy (default: 1).")

parser.add_argument("-m","--mines", type=int, default=8,
                    help="Number of mines that there will be in the game (default: 8).")

args = parser.parse_args()

print 'Robots game'
print '\t'+str(args.robots)+' Robots, Strategy '+str(args.robotstrategy)+', '+str(args.mines)+' Mines.'
print

t0 = time()

# Gradient Initialization
gradient_mine = []
for i in range(args.mines):
    gradient_mine.append(0)

gradient = []

for i in range(SCREEN_WIDTH):
    gradient_aux = []
    for j in range(SCREEN_HEIGHT):
        # aux = defaultdict(base=0, mines=gradient_mine)
        aux = defaultdict(int)
        aux['base'] = 0
        aux['mines'] = 0
        gradient_aux.append(aux)
    gradient.append(gradient_aux)

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

# Base
base_x = np.random.randint(10,SCREEN_WIDTH-60)
base_y = np.random.randint(10,SCREEN_HEIGHT-60)

base = Base(base_x, base_y, 50, 50, RED)
all_sprite_list.add(base)

# gradient = spread_base(gradient, base_x, base_y)
for i in range(SCREEN_WIDTH):
    for j in range(SCREEN_HEIGHT):
        gradient[i][j]['base'] = math.sqrt(math.pow((base_x-i),2) + math.pow((base_y-j),2))

mines = []

# Minas
for i in range(args.mines):
    mina_x = np.random.randint(10,SCREEN_WIDTH-35)
    mina_y = np.random.randint(10,SCREEN_HEIGHT-35)

    while (not (mina_x < base_x or mina_x > (base_x+50))):
        mina_x = np.random.randint(10,SCREEN_WIDTH-35)

    while (not (mina_y < base_y or mina_y > (base_y+50))):
        mina_y = np.random.randint(10,SCREEN_HEIGHT-35)

    gold = np.random.randint(1,10)
    mina = Mine(i, mina_x, mina_y, 25, 25, gold, YELLOW)
    print 'mine', i, mina_x, mina_y, gold

    mines.append(mina)

    all_sprite_list.add(mina)
print len(mines), "mines created"

# Create players objects
players = []
player_pos = []

for i in range(args.robots):
    player_x = np.random.randint(10,SCREEN_WIDTH-35)
    player_y = np.random.randint(10,SCREEN_HEIGHT-35)
    player_pos.append((player_x, player_y))
    strategy = eval('Player'+str(args.robotstrategy))
    
    player = strategy(i, player_x, player_y, capacity=1)
    
    player.walls = wall_list
    all_sprite_list.add(player)
    players.append(player)
    # wall_list.add(player)

clock = pygame.time.Clock()

done = False

i = 0
while not done:
    i+=1
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            duration = time() - t0
            print 'duration:', duration, 's'
            print
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

    cond = True

    for player in players:

        # Checking base
        if inside(player, base):
            aux = base.toDeposit(player.releaseGold())

        # Checking mines
        for mine in mines:
            if inside(player, mine):
                player.storeGold(mine)
                if not mine.gold:
                    mines.remove(mine)
        

        # Game ending
        cond = cond and not player.gold

        # Moviment
        player.moviment(player_pos, gradient)

    if cond and not len(mines):
        duration = time() - t0
        print 'duration:', duration, 's'
        print i, 'ciclos'
        done = True


   
    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
print '___________________________________________________________________________'
print
