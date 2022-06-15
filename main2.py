import pygame
from pygame.locals import *

#define fps
clock = pygame.time.Clock()
fps = 60


screen_width = 700
screen_height = 394

screen = pygame.display.set_mode((screen_width, screen_height))


#define colours
red = (255, 0, 0)
green = (0, 255, 0)


#load image
bg = pygame.image.load("resources/bg_sky.png").convert()

def draw_bg():
    screen.blit(bg, (0, 0))


#create spaceship class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/p_none-right1.png")
        self.imageblock = pygame.image.load("resources/p_block-none.png")
        self.imageattack = pygame.image.load("resources/p_close-right1.png")
        self.imageND = pygame.image.load("resources/p_none-right1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.isJump = False
        self.jump_high = 20
        self.jump_vel = self.jump_high
        self.isBlocked = False
        self.isAttack = False
        self.look = True # True derecha , False izquierda
        self.last_shot = pygame.time.get_ticks()

    def jump(self):
        if self.isJump is True:
            self.rect.y -= self.jump_vel
            self.jump_vel -= 1
            if self.jump_vel < -(self.jump_high):
                self.jump_vel = self.jump_high
                self.isJump = False


    def AnimationNormalBlock(self):
        self.image = self.imageND
        self.isBlocked = False

    def AnimationNormalAttack(self):
        self.image = self.imageND
        self.isAttack = False

    def update(self):
        #set movement speed
        speed = 8
        #set a cooldown variable
        cooldown = 500 #milliseconds


        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
            self.look = False
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
            self.look = True
        if key[pygame.K_SPACE] and self.isJump is False:
            self.isJump = True
        if key[pygame.K_x]:
            self.isBlocked = True
            pygame.time.set_timer(pygame.USEREVENT +1 , 1000) #ESTABLECE TIMER DEL ESCUDO
            if self.isBlocked is True:
                self.image = self.imageblock
            
            
        if key[pygame.K_c]:
            self.isAttack = True
            pygame.time.set_timer(pygame.USEREVENT +2 , 1000) #ESTABLECE TIMER DEL ATAQUE
            if self.isAttack is True:
                self.image = self.imageattack

    

        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_z] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
    


#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/bullet.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        self.rect.x += 10
        if self.rect.bottom < 0:
            self.kill()


#create sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


#create player
player = Player(int(screen_width / 2), screen_height - 100)
player_group.add(player)



run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT +1 : 
            player.AnimationNormalBlock()
        if event.type == pygame.USEREVENT +2 : 
            player.AnimationNormalAttack()

    player.jump()

    #update player
    player.update()


    #update sprite groups
    bullet_group.update()

    #draw sprite groups
    player_group.draw(screen)
    bullet_group.draw(screen)


    pygame.display.update()

pygame.quit()