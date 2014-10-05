"""
Based on Paul Vincent Craven code
http://simpson.edu/author/pcraven-2/
"""

import pygame, abc
import numpy as np
from objects import Base, Mine, Wall

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = (   255,   0, 0)
GREEN    = (   0,   255, 0)
YELLOW   = ( 255,   255, 0)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    # Constructor function
    def __init__(self, id, x, y, capacity=1):

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None


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

        self.id = id

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

        # if self.inside(self.base):
        #     aux = self.base.toDeposit(self.gold)
        #     self.gold-=aux

        # for mine in self.mines:
        #     if self.inside(mine):
        #         self.storeGold(mine)

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

    def inside(self, obj):

        inside_x = (obj.rect.x <= self.rect.x and obj.rect.x+obj.rect.width >= self.rect.x)
        inside_y = (obj.rect.y <= self.rect.y and obj.rect.y+obj.rect.height >= self.rect.y)

        return (inside_x and inside_y)

    @abc.abstractmethod
    def moviment(self, player_pos):

        def isIn(vector, point):
            try:
                index = vector[point]
                return True
            except:
                return False

        possibility = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]

        if (self.rect.x <= 10 or self.rect.x < 0):
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
        elif (self.rect.x >= SCREEN_WIDTH-30):
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
        if (self.rect.y <= 10 or self.rect.y < 0):
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
        elif (self.rect.y >= SCREEN_HEIGHT-30):
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

        mov_x, mov_y = possibility[np.random.randint(len(possibility))]
        new_pos = (player_pos[self.id][0]+mov_x, player_pos[self.id][1]+mov_y)

        while isIn(player_pos, new_pos):
            try:
                possibility.remove((mov_x, mov_y))
            except:
                pass
            mov_x, mov_y = possibility[np.random.randint(len(possibility))]
            new_pos = (player_pos[self.id][0]+mov_x, player_pos[self.id][1]+mov_y)

        self.changespeed(mov_x,mov_y)
        player_pos[self.id] = (new_pos)
