"""
Based on Paul Vincent Craven code
http://simpson.edu/author/pcraven-2/
"""

import pygame
import numpy as np

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = (   255,   0, 0)
GREEN    = (   0,   255, 0)
YELLOW   = ( 255,   255, 0)

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

    def getBalance():
        return self.gold

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