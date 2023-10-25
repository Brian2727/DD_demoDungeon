import os

import pygame as pygame

from Level import Level
from Mobs.Skeleton import Skeleton
from constants import *
from Mobs.Entities import *
from helperTools import scale_img

#initializes Py game
pygame.init()

#mob animation
#mob_animation_list = { "Stick_Samuray": [] , } this was used to load char animation with function but now embeeded in class
#loading fonts
font = pygame.font.Font("assets/Fonts/AtariClassic.ttf")



#initializing Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DD The Demo Dungeon')

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter >= 50:
            self.kill()



clock = pygame.time.Clock()


#loading animation bladeDash

slash_animation = []
for i in range(len(os.listdir(f"assets/images/weapons/BladeArk/" ))):
    image = pygame.image.load(f"assets/images/weapons/BladeArk/{i}.png" ).convert_alpha()
    image = scale_img(image, WEAPON_SCALE)
    slash_animation.append(image)

#create projectile group
slash_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

first_level = Level(FIRST_LEVEL_MAP,screen)
player = first_level.player
first_level.run()

def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, WHITE,(x * TILE_SIZE,0),(x*TILE_SIZE,SCREEN_HEIGHT))
        pygame.draw.line(screen, WHITE, (0 , x * TILE_SIZE), (SCREEN_WIDTH,x*TILE_SIZE))


#skeleton animation
#creating skeleton this will be automatic eventually


#character animation no longer needed since movement is inside the char class and the position is updated
# player = Character(100,100,slash_animation,"Stick_Samuray")
# move_x = 0
# move_y = 0
# moving_left = False
# moving_right = False
# moving_up    = False
# moving_down  = False

#enemies list
enemy_list = first_level.enemies
enemy_proj = pygame.sprite.Group()


#MainGame Loop
GameLive = True

while (GameLive):

    screen.fill(BG)
    first_level.run()
    clock.tick(60)

    #draw player
    for enemy in enemy_list:
        enemy.draw(screen)
        slash_wave = enemy.update(first_level.tiles,player)
        if slash_wave:
            enemy_proj.add(slash_wave)

    #draw player and update
    player.draw(screen)
    slash_wave = player.move(first_level.tiles)
    player.get_input()

    #Work with waepon damage and area of effect
    if slash_wave:
        slash_group.add(slash_wave)

    for slash in slash_group:
        slash.draw(screen)
        damage,damage_pos = slash.update(enemy_list)
        if damage_pos:
            damage_text_group.add(DamageText(damage_pos[0],damage_pos[1] - 10, str(damage), RED))

    for slash in enemy_proj:
        slash.draw(screen)
        damage, damage_pos = slash.update(player)
        if damage_pos:
            damage_text_group.add(DamageText(damage_pos[0], damage_pos[1] - 10, str(damage), RED))

    #Show damage text
    damage_text_group.update()
    damage_text_group.draw(screen)



    #update display
    pygame.display.update()


#end game.
pygame.quit()
