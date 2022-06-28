from cmath import rect
from time import time
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

        self.UI = pygame.image.load("resources/ui_face_player.png")

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
        self.speed = 5
        self.jump_vel = self.jump_high
        self.isBlocked = False
        self.isAttack = False
        self.look = True # True derecha , False izquierda
        self.cooldown = 500 #milliseconds

        self.last_shot = pygame.time.get_ticks()
        
        self.invencivility = False #Tiempo de recuperación despues de daño

    def animate(self):
        self.is_animating = True

    
       
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

    def vulneravility(self):
        self.invencivility = False

    def AnimationMoveLeft(self):
        self.image = self.spriteLeft[int(self.current_sprite_left)]    #El sprite actual se posiciona en la imagen actual
        self.animate()                                                 #¿Esta animado? Si
        if self.is_animating == True:                                  

            self.current_sprite_left += 0.2                            #Para que la animación sea mas lenta, se recorre en decimales

            if self.current_sprite_left >= len(self.spriteLeft):       #Cuando se recorren la fila de imagenes del sprite, y llega al final, vuelve al inicio
                self.current_sprite_left = 0
                self.is_animating = False

            self.image = self.spriteLeft[int(self.current_sprite_left)]

    def AnimationMoveRight(self): #Se explica el funcionamiento en AnimationMoveLeft ya que funcionan de manera similar
        self.animate()
        if self.is_animating == True:

            self.current_sprite_right += 0.2

            if self.current_sprite_right >= len(self.spriteRigth):
                self.current_sprite_right = 0
                self.is_animating = False

            self.image = self.spriteRigth[int(self.current_sprite_right)]

    def MoveLeft(self):
        self.rect.x -= self.speed
        self.look = False

    def MoveRight(self):
        self.rect.x += self.speed
        self.look = True

    def damage(self):
        if player.invencivility is False:                    #Mientras no sea invencible:
            self.healt -= 10                                 #Le baja 10 puntos de vida
            player.invencivility = True                      #Se hace invencible. Como los ticks son tan rapidos, la función se aplica muy rapido y baja mas de 10 puntos. Es por esto que lo hace invencible, basicamente funciona como un cooldown de daño
            pygame.time.set_timer(pygame.USEREVENT +3 , 800) #En 0,8 segundos, vuelve a ser vulnerable
     
    def Block(self):
        self.isBlocked = True                            #¿Esta bloqueando? Si
        pygame.time.set_timer(pygame.USEREVENT +1 , 900) #Establece timer del escudo, Cooldown del escudo, se desactiva a los 0,9 segundos
        
        if self.isBlocked is True and self.look is True: #Esta bloqueando y mira a la derecha
            self.image = self.imageblock                 #Se activa animación de bloqueo a la derecha
        elif self.isBlocked is True and self.look is False:
            self.image = self.imageblockleft

    def Attack(self):
        self.isAttack = True
        pygame.time.set_timer(pygame.USEREVENT +2 , 900) #Establece cooldown del ataque, cada 0.9 segundos se puede volver a atacar   
            
        if self.isAttack is True and self.look is True:
            self.image = self.imageattack
        elif self.isAttack is True and self.look is False:
            self.image = self.imageattackleft
   
    def HealthBar(self):
        screen.blit(self.UI, (30,10))
        pygame.draw.rect(screen, red, (50,20,100,5))
        pygame.draw.rect(screen, green, (50,20,self.healt,5))

    def Shoot(self):
        time_now = pygame.time.get_ticks()
        bullet = Bullets(self.rect.centerx, self.rect.top+10, self.look)
        bullet_group.add(bullet)
        self.last_shot = time_now

    def update(self):
        time_now = pygame.time.get_ticks() #Tiempo actual
       
        #Cuando se presiona:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.MoveLeft()            #Se mueve a la izquierda 
            self.AnimationMoveLeft()   #Se anima el movimiento
            
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.MoveRight()           #Se mueve a la derecha
            self.AnimationMoveRight()  #Se anima el movimiento
            
        if key[pygame.K_SPACE] and self.isJump is False:
            self.isJump = True
            
        if key[pygame.K_h]:
            self.damage()
            
        if key[pygame.K_x]: #Bloquear
            self.Block()
                 
        if key[pygame.K_c]: #Atacar
            self.Attack()
                   
        if key[pygame.K_z] and time_now - self.last_shot > self.cooldown: #Disparar
            self.Shoot()

        self.HealthBar()  
       

        self.jump() #La accion de saltar se verifica y se realiza constantemente, dado que tiene que actualizar su posición con cada Tick
    

class Nemesis(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.spriteRigth = []
        self.spriteRigth.append(pygame.image.load("resources/n_close-right.png"))
        self.spriteRigth.append(pygame.image.load("resources/n_close-right1.png"))
        self.spriteRigth.append(pygame.image.load("resources/n_close-right2.png"))
        self.current_sprite_right = 0

        self.spriteLeft = []
        self.spriteLeft.append(pygame.image.load("resources/n_close-left.png"))
        self.spriteLeft.append(pygame.image.load("resources/n_close-left1.png"))
        self.spriteLeft.append(pygame.image.load("resources/n_close-left2.png"))
        self.current_sprite_left = 0

        self.UI = pygame.image.load("resources/ui_face_nemesis.png")

        self.image = self.spriteLeft[self.current_sprite_left]

        self.is_animating = False

        
        self.imageblock = pygame.image.load("resources/n_block-right.png")
        self.imageblockleft = pygame.image.load("resources/n_block-left.png")
        self.imageattack = pygame.image.load("resources/n_far-right.png")
        self.imageattackleft = pygame.image.load("resources/n_far-left.png")
        self.imageND = pygame.image.load("resources/n_close-left1.png")

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.isJump = False
        self.healt = 100
        self.jump_high = 15
        self.speed = 5
        self.jump_vel = self.jump_high
        self.isBlocked = False
        self.isAttack = False
        self.look = False # True derecha , False izquierda
        self.cooldown = 500 #milliseconds

        self.last_shot = pygame.time.get_ticks()
        
        self.invencivility = False #Tiempo de recuperación despues de daño

    def animate(self):
        self.is_animating = True

       
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

    def AnimationMoveLeft(self):
        self.image = self.spriteLeft[int(self.current_sprite_left)]    #El sprite actual se posiciona en la imagen actual
        self.animate()                                                 #¿Esta animado? Si
        if self.is_animating == True:                                  

            self.current_sprite_left += 0.2                            #Para que la animación sea mas lenta, se recorre en decimales

            if self.current_sprite_left >= len(self.spriteLeft):       #Cuando se recorren la fila de imagenes del sprite, y llega al final, vuelve al inicio
                self.current_sprite_left = 0
                self.is_animating = False

            self.image = self.spriteLeft[int(self.current_sprite_left)]

    def AnimationMoveRight(self): #Se explica el funcionamiento en AnimationMoveLeft ya que funcionan de manera similar
        self.animate()
        if self.is_animating == True:

            self.current_sprite_right += 0.2

            if self.current_sprite_right >= len(self.spriteRigth):
                self.current_sprite_right = 0
                self.is_animating = False

            self.image = self.spriteRigth[int(self.current_sprite_right)]

    def MoveLeft(self):
        self.rect.x -= self.speed
        self.look = False

    def MoveRight(self):
        self.rect.x += self.speed
        self.look = True
    
    def vulneravility(self):
        self.invencivility = False

    def damage(self):
        if player.invencivility is False:                    #Mientras no sea invencible:
            self.healt -= 10                                 #Le baja 10 puntos de vida
            player.invencivility = True                      #Se hace invencible. Como los ticks son tan rapidos, la función se aplica muy rapido y baja mas de 10 puntos. Es por esto que lo hace invencible, basicamente funciona como un cooldown de daño
            pygame.time.set_timer(pygame.USEREVENT +4 , 800) #En 0,8 segundos, vuelve a ser vulnerable
     
    def Block(self):
        self.isBlocked = True                            #¿Esta bloqueando? Si
        pygame.time.set_timer(pygame.USEREVENT +5 , 900) #Establece timer del escudo, Cooldown del escudo, se desactiva a los 0,9 segundos
        
        if self.isBlocked is True and self.look is True: #Esta bloqueando y mira a la derecha
            self.image = self.imageblock                 #Se activa animación de bloqueo a la derecha
        elif self.isBlocked is True and self.look is False:
            self.image = self.imageblockleft

    def Attack(self):
        self.isAttack = True
        pygame.time.set_timer(pygame.USEREVENT +6 , 900) #Establece cooldown del ataque, cada 0.9 segundos se puede volver a atacar   
            
        if self.isAttack is True and self.look is True:
            self.image = self.imageattack
        elif self.isAttack is True and self.look is False:
            self.image = self.imageattackleft

    def Shoot(self):
        time_now = pygame.time.get_ticks()
        bullet = EnemyBullets(self.rect.centerx, self.rect.top+10, self.look)
        enemybullet_group.add(bullet)
        self.last_shot = time_now

    def HealthBar(self):
        screen.blit(self.UI, (screen_width-55,10))
        pygame.draw.rect(screen, red, (screen_width-150,20,100,5))
        pygame.draw.rect(screen, green, (screen_width-150,20,self.healt,5))

    def update(self):
        time_now = pygame.time.get_ticks() #Tiempo actual
       
        #Cuando se presiona:
        key = pygame.key.get_pressed()
        if key[pygame.K_k] and self.rect.left > 0:
            self.MoveLeft()            #Se mueve a la izquierda 
            self.AnimationMoveLeft()   #Se anima el movimiento
            
        if key[pygame.K_l] and self.rect.right < screen_width:
            self.MoveRight()           #Se mueve a la derecha
            self.AnimationMoveRight()  #Se anima el movimiento

        if key[pygame.K_p] and self.isJump is False:
            self.isJump = True

        if key[pygame.K_g] and time_now - self.last_shot > self.cooldown: #Disparar
            self.Shoot()

        if key[pygame.K_i]: #Bloquear
            self.Block()
                 
        if key[pygame.K_o]: #Atacar
            self.Attack()

        self.jump()
        self.HealthBar()

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
        if pygame.sprite.spritecollide(self, nemesis_group,False) and nemesis.isBlocked is False:
            self.kill()
            nemesis.damage()
        if pygame.sprite.spritecollide(self, nemesis_group,False) and nemesis.isBlocked is True:
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
        if pygame.sprite.spritecollide(self, player_group,False) and player.isBlocked is False:
            self.kill()
            player.damage()
        if pygame.sprite.spritecollide(self, player_group,False) and player.isBlocked is True:
            self.kill()


#create sprite groups
player_group = pygame.sprite.Group()
nemesis_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

#create player
player = Player(int(screen_width / 4), screen_height - 83)
player_group.add(player)

nemesis = Nemesis(int(screen_width - 100), screen_height - 83)
nemesis_group.add(nemesis)


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
        if event.type == pygame.USEREVENT +3:
            player.vulneravility()

        #TIMERS DEL NEMESIS
        if event.type == pygame.USEREVENT +4 : 
            nemesis.vulneravility()
        if event.type == pygame.USEREVENT +5 : 
            nemesis.AnimationNormalBlock()
        if event.type == pygame.USEREVENT +6 : 
            nemesis.AnimationNormalAttack()
            

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
    nemesis.update()

    #update sprite groups
    bullet_group.update()
    enemybullet_group.update()
    #draw sprite groups
    player_group.draw(screen)
    bullet_group.draw(screen)
    nemesis_group.draw(screen)
    enemybullet_group.draw(screen)

    pygame.display.update()
    #print(player.isAttack)

pygame.quit()
