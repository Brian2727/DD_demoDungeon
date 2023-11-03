import pygame

from constants import TILE_SIZE
from helperTools import load_animations
from weapons.weapon import Projectile, Slash_Static


class Character(pygame.sprite.Sprite):
    animation_list = {
        "walk": [],
        "idle": [],
        "slash": [],
        "close_slash":[],
        "jump": [],
        "on_air": []
    }
    def __init__(self, x, y, weapons,type):
        super().__init__()
        #movement
        self.type = type
        self.jump_speed = -20
        self.gravity = 1
        self.dir = 0
        self.speed = 1
        self.move_x = 0
        self.move_y = 0
        #animation
        self.slash_animation_tick = pygame.time.get_ticks()
        self.slashing = False
        self.weapon_1 = weapons[0]
        self.weapon_2 = weapons[1]
        self.animation_index = 0
        self.running = False
        self.animation_list = load_animations(type, self.animation_list)
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.image = self.animation_list['idle'][self.animation_index]
        #position
        self.rect = pygame.Rect(x,y,TILE_SIZE,TILE_SIZE + (TILE_SIZE/2))
        self.slash_dir = 0

    def get_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameLive = False

            # take key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.dir = -1
                    self.move_x = -self.speed
                if event.key == pygame.K_d:
                    self.dir = +1
                    self.move_x = self.speed
                if event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_k:
                    if self.move_x == 0:
                        self.change_action('slash')
                        self.slashing = True
                if event.key == pygame.K_l:
                    self.change_action('close_slash')
                    self.slashing = True
                if event.key == pygame.K_SPACE:
                    self.jump()




            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.dir = 0
                    self.move_x = 0
                if event.key == pygame.K_d:
                    self.dir = 0
                    self.move_x = 0
                if event.key == pygame.K_w:
                    self.dir = 0

                if event.key == pygame.K_s:
                    self.dir = 0

                if event.key == pygame.K_l:
                    self.slashing = False

                if event.key == pygame.K_k:
                    pass


    def applygravity(self):
        self.move_y += self.gravity
        self.rect.y += self.move_y

    def jump(self):
        self.change_action('jump')
        self.move_y = self.jump_speed


    def move(self,tiles):

        if not self.action == 'on_air':
            if self.move_x < 0 and self.action != 'slash' and self.action != 'close_slash':
                self.dir = -1
                if self.action != 'jump':
                    self.change_action('walk')
                self.flip = True
                self.slash_dir = 180
            elif self.move_x > 0 and self.action != 'slash' and self.action != 'close_slash':
                if self.action != 'jump':
                    self.change_action('walk')
                self.flip = False
                self.slash_dir = 0
                self.dir = 1
            elif self.move_x == 0 and self.action != 'slash' and self.action != 'close_slash' and self.dir == 0:
                if self.action != 'jump':
                    self.change_action('idle')


        slash = self.update(tiles)
        ##
           # self.rect.x += self.move_x
            #self.rect.y += self.move_y

        return slash

    def horizontal_movement_collition(self,tiles):

        if self.action != 'slash' and self.action != 'hit':
            self.rect.x += self.move_x
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.move_x < 0:
                    if not tiles.sprites()[0].x_shift == 0:
                        self.move_x += 2 * 2
                    else:
                        print(f'moving on the negative {self.move_x}')
                        self.rect.left = tile.rect.right
                elif self.move_x > 0:
                    if not tiles.sprites()[0].x_shift == 0:
                        self.move_x += -2 * 2
                    else:
                        self.rect.right = tile.rect.left

    def vertical_movement_collition(self,tiles):
        self.applygravity()
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.move_y < 0:
                    self.rect.top = tile.rect.bottom

                elif self.move_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.move_y = 0
                    if self.action == 'jump' or self.action == 'on_air':
                        self.change_action('idle')
                    break


    def update(self,tiles):
        self.horizontal_movement_collition(tiles)
        self.vertical_movement_collition(tiles)
        if self.slashing:
            if self.action == 'slash':
                animation_timer = 200
            else:
                animation_timer = 50
        else:
            animation_timer = 150
        slash_spawn_time = 100
        slash_wave = None
        if self.action == 'walk':
            self.change_action('walk')
        if self.action == 'idle':
            self.change_action('idle')
        if self.action == 'slash':
            if self.slashing and self.animation_index == 4:
                print("creating Slash")
                slash_wave = Projectile(self.weapon_1, self.rect.centerx, self.rect.centery, self.slash_dir)
                self.slash_animation_tick = pygame.time.get_ticks()
                self.slashing = False
            self.change_action('slash')
        if self.action == 'close_slash':
            if self.animation_index == 4:
                slash_wave = Slash_Static(self.weapon_2,(self.rect.centerx ),self.rect.centery,self.slash_dir,0)
            elif self.animation_index == 8:
                slash_wave = Slash_Static(self.weapon_2, (self.rect.centerx ), self.rect.centery,
                                      self.slash_dir, 1)
            self.change_action("close_slash")


        self.image = self.animation_list[self.action][self.animation_index]

        if (pygame.time.get_ticks() - self.update_time) >= animation_timer:
            self.animation_index += 1
            self.update_time = pygame.time.get_ticks()


        if self.animation_index >= len(self.animation_list[self.action]) - 1:
            if self.action == 'slash':
                self.slashing = False
                self.change_action('idle')
            if self.action == 'close_slash' and not self.slashing:
                self.slashing = False
                self.change_action('idle')
            if self.action == 'jump':
                self.change_action('on_air')
            self.animation_index = 0

        return slash_wave

    def change_action(self,new_action):
        if self.action == new_action:
            pass
        else:
            print(f"{self.type} is cdhanging Action from {self.action} to {new_action}")
            self.action = new_action
            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()
            #self.update()

    def draw(self,screen):
        image_flip = pygame.transform.flip(self.image,self.flip,False)
        screen.blit(image_flip,self.rect)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)

