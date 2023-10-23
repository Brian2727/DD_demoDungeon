import math

import pygame
import random
from Mobs.Entities import Character
from helperTools import load_animations
from weapon import Projectile


class Skeleton(Character,pygame.sprite.Sprite):
    skeleton_animation_map = {
        "walk": [],
        "idle": [],
        "slash": [],
        "dead":  [],
        "hit":   [],
    }
    def __init__(self, x, y,weapon_animation_list,health,type):
        self.rand_action = 0
        self.attention_spam = pygame.time.get_ticks()
        self.animation_list = load_animations(type,self.skeleton_animation_map)
        super().__init__(x, y,weapon_animation_list,type)
        self.type = type
        self.health = health
        self.prev_x = self.rect.centerx
        self.attack_range = 70

    def move(self,tiles):
        tick_timer = 10500
        if (pygame.time.get_ticks() - self.attention_spam) > tick_timer:
            self.rand_action = random.randint(1,3)
            self.move_x = random.randint(-1,1)
        self.horizontal_movement_collition(tiles)
        if self.action == 'hit' or self.action == 'dead':
            pass
        else:
            if self.rand_action == 1:
                self.move_x = self.move_x * 2
            if self.rand_action == 2:
                #self.change_action('jump')
                self.change_action('slash')
                self.move_x = 0
            if self.rand_action == 3:
                self.change_action('slash')
                self.move_x = 1

        #self.rect.x += self.move_x + tiles.sprites()[0].x_shift

    def jump(self):
        self.move_y += self.jump_speed

    def ai(self,player,tiles):
        slash_spawn_time = 100
        if not self.action == 'hit':
            self.move_x = tiles.sprites()[0].x_shift
        clipped_line = ()
        attention_timer = 1500
        line_of_sight = ((self.rect.centerx,self.rect.centery),(player.rect.centerx,player.rect.centery))

        for tile in tiles:
            if tile.rect.clipline(line_of_sight):
                clipped_line = tile.rect.clipline(line_of_sight)

        dist = math.sqrt(((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))

        if self.action == 'slash':
            if self.animation_index == 5 and (pygame.time.get_ticks() - self.slash_animation_tick) >= slash_spawn_time:
                print("creating Slash")
                slash_wave = Projectile(self.weapons_animation_list, self.rect.centerx, self.rect.centery,
                                        self.slash_dir*3)
                slash_wave.dx = 0
                self.slash_animation_tick = pygame.time.get_ticks()
                return slash_wave
        if not clipped_line and dist < 400 and not self.action == 'slash' and not self.action == 'hit' :
            if (pygame.time.get_ticks() - self.attention_spam) > attention_timer:
                self.prev_x = self.rect.centerx

            if self.rect.centerx > player.rect.centerx and dist > 50:
                self.move_x += -self.speed
                self.change_action('walk')
                self.flip = True
            elif self.rect.centerx < player.rect.centerx and dist > 50:
                self.move_x += self.speed
                self.flip = False
                self.change_action('walk')
            else:
                self.change_action('idle')

            if self.action == 'walk' and self.prev_x == self.rect.centerx:
                self.attention_spam = pygame.time.get_ticks()

            #attack  Player
            if dist <= self.attack_range:
                self.change_action('slash')



    def update(self,tiles,player):
        slash_wave = self.ai(player,tiles)
        self.horizontal_movement_collition(tiles)
        self.vertical_movement_collition(tiles)
        slash_spawn_time = 2000

        if self.health <= 0:
            self.change_action('dead')
        elif self.action == 'walk':
            self.change_action('walk')
        elif self.action == 'idle':
            self.change_action('idle')
        elif self.action == 'hit':
            self.change_action('hit')

        #print(f"animation {self.action} and index of animation = {self.animation_index}")
        animation_timer = 100
        self.image = self.animation_list[self.action][self.animation_index]

        if (pygame.time.get_ticks() - self.update_time) >= animation_timer:
            self.animation_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.animation_index >= len(self.animation_list[self.action]) - 1:
            if self.action == 'slash':
                self.change_action('idle')
            if self.action == 'hit':
                self.change_action('idle')
            if self.action == 'dead':
                self.kill()
            self.animation_index = 0

        return slash_wave

    def get_input(self):
        pass