"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example

Explanation video: http://youtu.be/8IRyt7ft7zg

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame
import numpy as np

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

class Mine(pygame.sprite.Sprite):
    
    def __init__(self, id, x, y, width, height, gold, color=BLUE):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.id=id
        
        self.gold = gold

        self.width = width
        self.height = height

    def toMine(self):

        quantity = np.random(0,self.gold+1)

        if (self.gold - quantity) > 0:
            self.gold -= quantity
            return quantity
        else:
            aux = self.gold
            self.gold = 0
            return aux

    def toMine(self, quantity):

        if (self.gold - quantity) > 0:
            self.gold -= quantity
            return quantity
        else:
            aux = self.gold
            self.gold = 0
            return aux

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height, color=BLUE):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Base(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color=RED, gold=0.):
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.stock_gold = gold

        self.width = width
        self.height = height

    def toDeposit(self, gold):

        if gold > 0:
            print 'Gold deposited'
            self.stock_gold += gold

        return gold

    def inside(self, x, y):
        inside_x = (x >= self.rect.x and x <= self.rect.x+self.width)
        inside_y = (y >= self.rect.y and y <= self.rect.y+self.height)

        return (inside_x and inside_y)

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    # Set speed vector
    change_x = 0
    change_y = 0
    walls = None

    # Constructor function
    def __init__(self, x, y, base, mines, capacity=100):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.gold = 0
        self.capacity = capacity

        self.base = base
        self.mines = mines

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if self.inside(base):
            aux = base.toDeposit(self.gold)
            self.gold-=aux

        for mine in self.mines:
            if self.inside(mine):
                self.storeGold(mine)

    def storeGold(self, mine):

        capacity = self.capacity - self.gold
        if capacity > 0:
            gold = mine.toMine(capacity)
            if gold > 0:
                self.gold += gold
                print 'Got', gold, 'gold from mine', mine.id

        if mine.gold == 0:
            mine.kill()

    def releaseGold(self):

        gold = self.gold
        self.gold = 0

        return gold

    # def releaseGold(self, gold):

    #     if self.gold < gold:
    #         self.gold = 0
    #         return self.gold

    #     self.gold-=gold

    #     return self.gold

    def inside(self, obj):

        # print obj.rect.x, obj.rect.y

        inside_x = (obj.rect.x <= self.rect.x and obj.rect.x+obj.rect.width >= self.rect.x)
        inside_y = (obj.rect.y <= self.rect.y and obj.rect.y+obj.rect.height >= self.rect.y)

        return (inside_x and inside_y)	

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

wall = Wall(10, 200, 100, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# Base
base_x = np.random.randint(10,SCREEN_WIDTH-60)
base_y = np.random.randint(10,SCREEN_HEIGHT-60)

base = Base(base_x, base_y, 50, 50, RED)
# wall_list.add(wall)
all_sprite_list.add(base)

mines = []

# Minas
for i in range(8):
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
print len(mines)
# Create the player paddle object
player = Player(10, 10, base, mines)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:

    for event in pygame.event.get():

        # print player.rect.x, player.rect.y

        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:

            # print player.rect.x, player.rect.y

            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:

            # print player.rect.x, player.rect.y

            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    # if base.inside(player.rect.x, player.rect.y):
    #     base.toDeposit(player)

    # for pos, mine in enumerate(mines):
    #     if mines[pos].inside(player.rect.x, player.rect.y):
    #         player.storeGold(mines[pos])

    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
