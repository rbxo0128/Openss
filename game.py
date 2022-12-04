import pygame

GAME_WIDTH = 480
GAME_HEIGHT = 800

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      
        self.rect.topleft = init_pos                    
        self.speed = 8                                  
        self.misiles = pygame.sprite.Group()            
        self.img_index = 0                              
        self.is_hit = False

    def get_pos(self):
        x = self.rect.x
        y = self.rect.y
        return [x,y]

    def set_pos(self, x_pos, y_pos):
        self.rect.x = x_pos
        self.rect.y = y_pos

    def shoot(self, misile_img):
        misile = Misile(misile_img,self.rect.midtop)
        self.misiles.add(misile)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= GAME_HEIGHT - self.rect.height:
            self.rect.top = GAME_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= GAME_WIDTH - self.rect.width:
            self.rect.left = GAME_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Misile(pygame.sprite.Sprite):
    def __init__(self, misile_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = misile_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0
        self.power_items = pygame.sprite.Group()
        self.life_items = pygame.sprite.Group()
        self.speed_items = pygame.sprite.Group()

    def move(self):
        self.rect.top += self.speed

    def give_power_item(self, item_img):
        item_power = Power_Item(item_img,self.rect.midbottom)
        self.power_items.add(item_power)

    def give_life_item(self, item_img):
        item_life = Life_Item(item_img,self.rect.midbottom)
        self.life_items.add(item_life)

    def give_speed_item(self, item_img):
        item_speed = Speed_Item(item_img,self.rect.midbottom)
        self.speed_items.add(item_speed)


class Power_Item(pygame.sprite.Sprite):
    def __init__(self, item_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed =  3

    def move(self):
        self.rect.top += self.speed

class Life_Item(pygame.sprite.Sprite):
    def __init__(self, item_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed =  3

    def move(self):
        self.rect.top += self.speed

class Speed_Item(pygame.sprite.Sprite):
    def __init__(self, item_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = item_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed =  3

    def move(self):
        self.rect.top += self.speed