import pygame.sprite


class Tile(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self,x_shift):
        self.rect.x += x_shift

    def draw(self,screen,color):
        #screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, color, self.rect, 20)