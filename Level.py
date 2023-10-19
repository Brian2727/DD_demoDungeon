import os

import pygame
from Entities import Character
from Tiles import Tile
from constants import *
from helperTools import scale_img, load_weapon_animation

class Level:

    def __init__(self,level_data,surface):
        self.setup_level(level_data)
        self.screen = surface

    def setup_level(self,level_data):
        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        image = pygame.image.load("assets/images/tiles/level/0.png").convert_alpha()
        image = scale_img(image, 1.5)

        for row_index,row in enumerate(level_data):
            for col_index,cell in enumerate(level_data[row_index]):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    tile = Tile(image,x,y)
                    self.tiles.add(tile)
                if cell == 'P':
                    slash_animation = load_weapon_animation('BladeArk')
                    self.player = Character(x,y,slash_animation,"Stick_Samuray")

    def scroll_x(self):
        if self.player.rect.center[0] >= SCREEN_WIDTH-100 and self.player.dir > 0:
            self.player.action = 'walk'
            self.player.speed = 0
            self.player.move_x = 0
            return -5
        elif self.player.rect.center[0] <= SCREEN_WIDTH-(SCREEN_WIDTH-55)   and self.player.dir < 0:
            self.player.action = 'walk'
            self.player.move_x = 0
            self.player.speed = 0
            return 5
        else:
            self.player.dir = 0
            self.player.speed = 2
            return 0

    def horizontal_movement_collition(self):
        player = self.player
        print(self.player.move_x)
        self.player.rect.x += self.player.move_x
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.move_x < 0:
                    print(f'moving on the negative {player.move_x}')
                    player.rect.right = tile.rect.left
                elif player.move_x > 0:
                    player.rect.left = tile.rect.right

    def vertical_movement_collition(self):
        player = self.player
        player.applygravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.move_y < 0:
                    player.rect.top = tile.rect.bottom

                elif player.move_y > 0:
                    player.rect.bottom = tile.rect.top
                    player.move_y = 0

    def run(self):

        self.tiles.update(self.scroll_x())
        self.tiles.draw(self.screen,(255,0,0))
        #self.horizontal_movement_collition()
        #self.vertical_movement_collition()

