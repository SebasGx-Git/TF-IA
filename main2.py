from tkinter import Canvas
import pygame
from pygame.locals import *



#define fps
clock = pygame.time.Clock()
fps = 60


screen_width = 480
screen_height = 312
TILE_SIZE = 24


screen = pygame.display.set_mode((screen_width, screen_height))



#define colours
red = (255, 0, 0)
green = (0, 255, 0)


#load image
bg = pygame.image.load("resources/bg_sky.png").convert()
base1 = pygame.image.load("resources/bg_floor.png").convert()
base2 = pygame.image.load("resources/bg_floor2.png").convert()

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2']]


def draw_bg():
    screen.blit(bg, (0, 0))


#create Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.spriteRigth = []
        self.spriteRigth.append(pygame.image.load("resources/p_none-right.png"))
        self.spriteRigth.append(pygame.image.load("resources/p_none-right1.png"))
        self.spriteRigth.append(pygame.image.load("resources/p_none-right2.png"))
        self.current_sprite_right = 0

        self.spriteLeft = []
        self.spriteLeft.append(pygame.image.load("resources/p_none-left.png"))
        self.spriteLeft.append(pygame.image.load("resources/p_none-left1.png"))
        self.spriteLeft.append(pygame.image.load("resources/p_none-left2.png"))
        self.current_sprite_left = 0


        self.image = self.spriteRigth[self.current_sprite_right]

        self.is_animating = False

        
        self.imageblock = pygame.image.load("resources/p_block-none.png")
        self.imageblockleft = pygame.image.load("resources/p_block-left.png")
        self.imageattack = pygame.image.load("resources/p_far-right1.png")
        self.imageattackleft = pygame.image.load("resources/p_far-left1.png")
        self.imageND = pygame.image.load("resources/p_none-right2.png")

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.isJump = False
        self.healt = 100
        self.jump_high = 15
        self.jump_vel = self.jump_high
        self.isBlocked = False
        self.isAttack = False
        self.look = True # True derecha , False izquierda
        self.last_shot = pygame.time.get_ticks()
        self.invencivility = False #Tiempo de recuperación despues de daño

    def animate(self):
        self.is_animating = True

    def damage(self):
        self.healt -= 10

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
        speed = 5
        #set a cooldown variable
        cooldown = 500 #milliseconds


        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
            self.look = False

            self.image = self.spriteLeft[int(self.current_sprite_left)]

            self.animate()
            if self.is_animating == True:

                self.current_sprite_left += 0.2

                if self.current_sprite_left >= len(self.spriteLeft):
                    self.current_sprite_left = 0
                    self.is_animating = False

                self.image = self.spriteLeft[int(self.current_sprite_left)]

        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
            self.look = True
            
            self.animate()
            if self.is_animating == True:

                self.current_sprite_right += 0.2

                if self.current_sprite_right >= len(self.spriteRigth):
                    self.current_sprite_right = 0
                    self.is_animating = False

                self.image = self.spriteRigth[int(self.current_sprite_right)]

        if key[pygame.K_SPACE] and self.isJump is False:
            self.isJump = True

        if key[pygame.K_h]:
            if player.invencivility is False:
                self.damage()
                player.invencivility = True
                pygame.time.set_timer(pygame.USEREVENT +3 , 800) #ESTABLECE DE INVENCIBILIDAD

        if key[pygame.K_x]:
            self.isBlocked = True
            pygame.time.set_timer(pygame.USEREVENT +1 , 900) #ESTABLECE TIMER DEL ESCUDO
            if self.isBlocked is True and self.look is True:
                self.image = self.imageblock
            elif self.isBlocked is True and self.look is False:
                self.image = self.imageblockleft
            
            
        if key[pygame.K_c]:
            self.isAttack = True
            pygame.time.set_timer(pygame.USEREVENT +2 , 900) #ESTABLECE TIMER DEL ATAQUE
            if self.isAttack is True and self.look is True:
                self.image = self.imageattack
            elif self.isAttack is True and self.look is False:
                self.image = self.imageattackleft
    

        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_z] and time_now - self.last_shot > cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.top+10, self.look)
            bullet_group.add(bullet)
            self.last_shot = time_now
    


#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, look):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.look = look

    def update(self):
        if self.look is True:
            self.rect.x += 10
            if self.rect.x >= screen_width:
                self.kill()
        if self.look is False:
            self.rect.x -= 10
            if self.rect.x <= -10:
                self.kill()
            
#Create Enemy Bullets Class  : Se crea para que tengan diferentes colliders a la clase Bullets normal            
class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, look):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/enemy-bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.look = look

    def update(self):
        if self.look is True:
            self.rect.x += 10
            if self.rect.x >= screen_width:
                self.kill()
        if self.look is False:
            self.rect.x -= 10
            if self.rect.x <= -10:
                self.kill()
            


#create sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


#create player
player = Player(int(screen_width / 2), screen_height - 83)
player_group.add(player)



run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw health 
    pygame.draw.rect(screen, red, (50,20,100,5))
    pygame.draw.rect(screen, green, (50,20,player.healt,5))
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT +1 : 
            player.AnimationNormalBlock()
        if event.type == pygame.USEREVENT +2 : 
            player.AnimationNormalAttack()
        if event.type == pygame.USEREVENT +3:
            player.invencivility = False

    player.jump()

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(base1, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                screen.blit(base2, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    #update player
    player.update()


    #update sprite groups
    bullet_group.update()

    #draw sprite groups
    player_group.draw(screen)
    bullet_group.draw(screen)


    pygame.display.update()
    print(player.invencivility)

pygame.quit()
