import pygame

from helperTools import load_animations
from weapon import Projectile


class Character(pygame.sprite.Sprite):
    animation_list = {
        "walk": [],
        "idle": [],
        "slash": []
    }
    def __init__(self, x, y, weapons_animation_list,type):
        super().__init__()


        #movement
        self.jump_speed = -20
        self.gravity = 1
        self.dir = 0
        self.speed = 1
        self.move_x = 0
        self.move_y = 0
        #animation
        self.slash_animation_tick = pygame.time.get_ticks()
        self.slashing = False
        self.weapons_animation_list = weapons_animation_list
        self.animation_index = 0
        self.running = False
        self.animation_list = load_animations(type, self.animation_list)
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.flip = False
        self.image = self.animation_list['idle'][self.animation_index]
        #position
        self.rect = pygame.Rect(0,0,40,85)
        self.rect.center = (x,y)
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
                        self.action = 'slash'
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


    def applygravity(self):
        self.move_y += self.gravity
        self.rect.y += self.move_y

    def jump(self):
        self.move_y = self.jump_speed


    def move(self,tiles):

        if self.move_x < 0 and self.action != 'slash':
            self.dir = -1
            self.change_action('walk')
            self.flip = True
            self.slash_dir = 180
        elif self.move_x > 0 and self.action != 'slash':
            self.change_action('walk')
            self.flip = False
            self.slash_dir = 0
            self.dir = 1
        elif self.move_x == 0 and self.action != 'slash' and self.dir == 0:
            self.change_action('idle')

        slash = self.update(tiles)
        ##
           # self.rect.x += self.move_x
            #self.rect.y += self.move_y

        return slash

    def horizontal_movement_collition(self,tiles):

        if self.action != 'slash':
            self.rect.x += self.move_x
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.move_x < 0:
                    print(f'moving on the negative {self.move_x}')
                    self.rect.left = tile.rect.right
                elif self.move_x > 0:
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


    def update(self,tiles):
        self.horizontal_movement_collition(tiles)
        self.vertical_movement_collition(tiles)
        slash_spawn_time = 100
        slash_wave = None
        if self.action == 'walk':
            self.change_action('walk')

        if self.action == 'idle':
            self.change_action('idle')

        if self.action == 'slash':

            if (pygame.time.get_ticks() - self.slash_animation_tick) >= slash_spawn_time and not self.slashing:
                print("creating Slash")
                slash_wave = Projectile(self.weapons_animation_list,self.rect.centerx,self.rect.centery,self.slash_dir)
                self.slash_animation_tick = pygame.time.get_ticks()
                self.slashing = True
            self.change_action('slash')

        animation_timer = 100
        self.image = self.animation_list[self.action][self.animation_index]



        if (pygame.time.get_ticks() - self.update_time) >= animation_timer:
            self.animation_index += 1
            self.update_time = pygame.time.get_ticks()


        if self.animation_index >= len(self.animation_list[self.action]) - 1:
            if self.action == 'slash':
                self.slashing = False
                self.change_action('idle')
            self.animation_index = 0

        return slash_wave

    def change_action(self,new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()
            #self.update()

    def draw(self,screen):

        image_flip = pygame.transform.flip(self.image,self.flip,False)
        screen.blit(image_flip,self.rect)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)

class Skeleton(Character,pygame.sprite.Sprite):
    skeleton_animation_map = {
        "walk": [],
        "idle": [],
        "slash": [],
        "dead":  [],
        "hit":   [],
    }
    def __init__(self, x, y,weapon_animation_list,health,type):

        self.animation_list = load_animations(type,self.skeleton_animation_map)
        super().__init__(x, y,weapon_animation_list,type)
        self.type = type
        self.health = health

    def update(self,tiles):
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