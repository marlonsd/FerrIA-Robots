import pygame
from objects import Base, Mine, Wall

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = (   255,   0, 0)
GREEN    = (   0,   255, 0)
YELLOW   = ( 255,   255, 0)

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

        if self.inside(self.base):
            aux = self.base.toDeposit(self.gold)
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