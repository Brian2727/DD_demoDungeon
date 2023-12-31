import math
import random

import pygame.sprite

from constants import SLASH_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE, WEAPON_SCALE
from helperTools import load_weapon_animation


class Projectile(pygame.sprite.Sprite):
        def __init__(self,weapon_name,x,y,angle):
            pygame.sprite.Sprite.__init__(self)
            self.angle = angle
            self.animation_list = load_weapon_animation(weapon_name,WEAPON_SCALE)
            self.original_image = self.animation_list[0]
            self.update_time = pygame.time.get_ticks()
            self.image = pygame.transform.rotate(self.original_image,angle)
            self.animation_index = 0
            self.rect = self.image.get_rect()
            self.rect.center = (x + (math.cos(math.radians(self.angle)) * 80),y)
            #calculate speed of slash
            self.dx = math.cos(math.radians(self.angle)) * SLASH_SPEED

        def update(self,enemy_list):
            damage = 0
            damage_pos = None

            animation_timer = 50
            self.image =  pygame.transform.rotate(self.animation_list[self.animation_index],self.angle)

            if (pygame.time.get_ticks() - self.update_time) >= animation_timer:
                self.animation_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.animation_index >= len(self.animation_list) - 1:
                self.animation_index = 0

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.kill()
            try:
                for enemy in enemy_list:
                    if enemy.rect.colliderect(self.rect):
                        damage = (20 + random.randint(-5,5))
                        damage_pos = enemy.rect.center
                        enemy.health -= damage
                        enemy.change_action('hit')
                        enemy.move_x += self.dx * 1
                        self.kill()
                        break
            except:
                if enemy_list.rect.colliderect(self.rect):
                    damage = (20 + random.randint(-5, 5))
                    damage_pos = enemy_list.rect.center
                    #enemy.action = 'hit'
                    #enemy.animation_index = 0
                    enemy_list.rect.centerx += math.cos(math.radians(self.angle)) * 20
                    self.kill()


            self.rect.x += 2 * self.dx
            return damage , damage_pos


        def draw(self,screen):
            screen.blit(self.image,(self.rect.centerx - int(self.image.get_width()/2),self.rect.centery - int(self.image.get_height()/2)))

class Slash_Static(Projectile):

    def __init__(self,animation_list,x,y,angle,animation_index):
        super().__init__(animation_list,x,y,angle)
        self.animation_list = load_weapon_animation(animation_list, SCALE )
        self.dx = 0
        self.time_alive_counter = pygame.time.get_ticks()
        self.animation_index = animation_index

    def update(self,enemy_list):
        damage = 0
        damage_pos = None
        time_alive = 200
        self.image = pygame.transform.rotate(self.animation_list[self.animation_index], self.angle)
        if pygame.time.get_ticks()-self.time_alive_counter >= time_alive:
            self.kill()
        try:
            for enemy in enemy_list:
                if enemy.rect.colliderect(self.rect):
                    damage = (20 + random.randint(-5, 5))
                    damage_pos = enemy.rect.center
                    enemy.health -= damage
                    enemy.change_action('hit')
                    enemy.rect.x += math.cos(math.radians(self.angle))*20
                    self.kill()
                    break
        except:
            if enemy_list.rect.colliderect(self.rect):
                damage = (20 + random.randint(-5, 5))
                damage_pos = enemy_list.rect.center
                # enemy.action = 'hit'
                # enemy.animation_index = 0
                enemy_list.move_x += self.dx * 1
                self.kill()

        self.rect.x += 2 * self.dx
        return damage, damage_pos

