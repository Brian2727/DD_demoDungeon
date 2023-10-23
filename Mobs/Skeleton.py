import pygame
import random
from Mobs.Entities import Character
from helperTools import load_animations


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

    def ai(self,player,tiles):
        self.move_x += tiles.sprites()[0].x_shift

    def update(self,tiles):
        self.ai(player,tiles)
        self.horizontal_movement_collition(tiles)
        self.vertical_movement_collition(tiles)
        slash_spawn_time = 2000
        slash_wave = None
        if self.health <= 0:
            self.change_action('dead')

        if self.action == 'walk':
            self.change_action('walk')

        if self.action == 'idle':
            self.change_action('idle')

        if self.action == 'hit':
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