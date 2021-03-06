from cmath import rect
from time import time
from tkinter import Canvas
from turtle import width
from numpy import place
import pygame
from pygame.locals import *
from sqlalchemy import false
import movs as genes

#define fps
clock = pygame.time.Clock()
fps = 60
# bgratio = 16 : 9
WIDTH = 16
HEIGHT = 9
FLOOR = 2
PIXEL_UNIT = 2
TILE_SIZE = 24 * PIXEL_UNIT #24 es el tamaño del pixelart
screen_width = TILE_SIZE*WIDTH
screen_height = TILE_SIZE*HEIGHT

pygame.display.set_icon( pygame.image.load('assets/icon.png') )
pygame.display.set_caption('Artificial Nemesis Selection')
screen = pygame.display.set_mode((screen_width, screen_height))

def loadSprite(img_file):
    sprite = pygame.image.load(f"resources/{img_file}").convert_alpha() #convert() #
    return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))

#load Background and floor
bg = pygame.image.load("resources/bg_sky.png").convert()
bg = pygame.transform.scale(bg, (screen_width, screen_height))
base1 = loadSprite('bg_floor.png')
base2 = loadSprite('bg_floor2.png')
draw_bg = lambda : screen.blit(bg, (0, 0))

#Desplazamiento horizontal por el mundo
nemesis_genes = genes.pob_ini
num_nemesis = len(nemesis_genes)
scroll_hor = 0 #?
world_width = num_nemesis * (WIDTH + 1) # * TILE_SIZE?
are_fighting = True# True #Nuestra pantalla inicia con 1 nemesis y player
current_nemesis = 0

current_level = 0

class HealthBar:
    def __init__(self, toLeft = True):
        self.x = TILE_SIZE
        self.y = TILE_SIZE//2
        self.width = TILE_SIZE*2
        self.height = TILE_SIZE//8
        if not toLeft: self.x = screen_width - self.x - self.width
        self.border = (self.x - PIXEL_UNIT, self.y - PIXEL_UNIT,
            self.width + PIXEL_UNIT*2, self.height + PIXEL_UNIT*2 )

    def draw(self, health):
        # Surface, color, (X Y Widht Height)
        # self.c_border = (33,30,97)
        # self.c_damage = (224, 119, 170)
        # self.c_health = (255, 210, 142)
        health = (health * self.width) / 100
        pygame.draw.rect(screen, (33,30,97), self.border)
        pygame.draw.rect(screen, (224, 119, 170), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 210, 142), (self.x, self.y, health, self.height))


class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y,
                img_none_r, img_walking_right:list, 
                img_block_r, img_attack_r, img_shot_r,
                img_ui_face, main_look_right:bool = True ):
        pygame.sprite.Sprite.__init__(self)
        self.main_look_right = main_look_right
        self.weakness = 10 #puntos de vida disminuidos por golpe

        self.spriteRigth = [loadSprite(i) for i in img_walking_right]
        self.spriteLeft = [ pygame.transform.flip(s, True, False) for s in self.spriteRigth ]
        self.current_sprite_right = self.current_sprite_left = 0
        self.image = self.spriteRigth[self.current_sprite_right]
        self.is_animating = False

        self.imageblock = loadSprite(img_block_r)
        self.imageblockleft = pygame.transform.flip(self.imageblock, True, False)
        self.imageattack = loadSprite(img_attack_r)
        self.imageattackleft = pygame.transform.flip(self.imageattack, True, False)
        self.imageshot = loadSprite(img_shot_r)
        self.imageshotleft = pygame.transform.flip(self.imageattack, True, False)
        self.imageND = loadSprite(img_none_r)
        #if main_look_right is False: self.imageND = pygame.transform.flip(self.imageND, True, False)
        self.imageNDleft = pygame.transform.flip(self.imageND, True, False)

        self.UI = loadSprite(img_ui_face)
        self.healthBar = HealthBar(main_look_right)

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
        self.cooldown = 200 #500 #milliseconds

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
        self.image = self.imageND if self.look else self.imageNDleft
        self.isBlocked = False

    def AnimationNormalAttack(self):
        self.image = self.imageND if self.look else self.imageNDleft
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
            self.healt -= self.weakness                      #Le baja puntos de vida
            player.invencivility = True                      #Se hace invencible. Como los ticks son tan rapidos, la función se aplica muy rapido y baja mas de 10 puntos. Es por esto que lo hace invencible, basicamente funciona como un cooldown de daño
            pygame.time.set_timer(pygame.USEREVENT +3 , 200 ) #800 #En 0,8 segundos, vuelve a ser vulnerable
     
    def Block(self):
        #self.isBlocked = True                            #¿Esta bloqueando? Si
        pygame.time.set_timer(pygame.USEREVENT +1 , 500) #Establece timer del escudo, Cooldown del escudo, se desactiva a los 0,5 segundos
        self.image = self.imageblock if self.look else self.imageblockleft

    def Attack(self):
        #self.isAttack = True
        pygame.time.set_timer(pygame.USEREVENT +2 , 900) #Establece cooldown del ataque, cada 0.9 segundos se puede volver a atacar   
        self.image = self.imageattack if self.look else self.imageattackleft
   
    def Shoot(self):
        pass
        
    def HealthBar(self):
        screen.blit(self.UI, (0,0) if self.main_look_right else (screen_width-TILE_SIZE,0) ) #image (left top)
        self.healthBar.draw(self.healt)

    def update(self): 
        pass
        #time_now = pygame.time.get_ticks() #Tiempo actual    


#create Player class
class Player(Agent):
    def __init__(self, x, y):
        Agent.__init__(self, x, y, "p_none-none.png",
        ["p_none-right1.png", "p_none-none.png", "p_none-right2.png"],
        "p_block-none.png", "p_close-none.png", "p_far-none.png",
        "ui_face_player.png" )
        #'still', 'a_close' , 'a_far', 'block', 'w_right', 'w_left', 'jump'
        self.currAction = 'still'

    def Shoot(self):
        time_now = pygame.time.get_ticks()
        bullet = Bullets(self.rect.centerx, self.rect.top+10, self.look)
        bullet_group.add( bullet )
        self.last_shot = time_now
        self.image = self.imageshot if self.look else self.imageshotleft
        return 
        
    def update(self):
        time_now = pygame.time.get_ticks() #Tiempo actual
       
        #Cuando se presiona:
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.MoveLeft()            #Se mueve a la izquierda 
            self.AnimationMoveLeft()   #Se anima el movimiento
            self.currAction = 'w_right'
            
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.MoveRight()           #Se mueve a la derecha
            self.AnimationMoveRight()  #Se anima el movimiento
            self.currAction = 'w_left'
            
        if key[pygame.K_SPACE] and self.isJump is False:
            self.isJump = True
            self.currAction = 'jump'
            
        if key[pygame.K_h]:
            self.damage()
            
        if key[pygame.K_x]: #Bloquear
            self.Block()
            self.currAction = 'block'
                 
        if key[pygame.K_c]: #Atacar
            self.Attack()
            self.currAction = 'a_close'
                   
        if key[pygame.K_z] and time_now - self.last_shot > self.cooldown: #Disparar
            self.Shoot()
            self.currAction = 'a_far'

        self.HealthBar()  
        self.jump() #La accion de saltar se verifica y se realiza constantemente, dado que tiene que actualizar su posición con cada Tick
    

class Nemesis(Agent):
    def __init__(self,x,y):
        Agent.__init__(self, x, y, "n_none-none.png",
        ["n_none-right1.png", "n_none-none.png", "n_none-right2.png"],
        "n_block-none.png", "n_close-none.png", "n_far-none.png",
        "ui_face_nemesis.png", False )
    
    def __del__(self): pass

    def Shoot(self):
        time_now = pygame.time.get_ticks()
        bullet = EnemyBullets(self.rect.centerx, self.rect.top+10, self.look)
        enemybullet_group.add(bullet)
        self.last_shot = time_now
        self.image = self.imageshot if self.look else self.imageshotleft
        return 
        
    def update(self, player_currAction):
        #asumiendo que para que realice un update
        #el player tuvo que haberlo visto
        nemesis_genes[current_nemesis].duration += 1
        time_now = pygame.time.get_ticks() #Tiempo actual

        #Cuando el player:....
        #movs_ord de acuerdo al numero devuelvo la accion
        num_act_player = genes.movs[player_currAction]
        num_reaction = nemesis_genes[current_nemesis].reactions[num_act_player]
        #movs de acuerdo a la accion devuelvo el numero
        reaction = genes.movs_ord[num_reaction]
        #print(reaction)
        #'still', 'a_close' , 'a_far', 'block', 'w_right', 'w_left', 'jump'
        #if (reaction == 'still'): pass
        if (reaction == 'a_close'):  #Atacar
            self.Attack()
        if (reaction == 'a_far') and time_now - self.last_shot > self.cooldown: #Disparar
            self.Shoot()
        if (reaction == 'block'): #Bloquear
            self.Block()
        if (reaction == 'w_left')  and self.rect.left > 0:
            self.MoveLeft()            #Se mueve a la izquierda 
            self.AnimationMoveLeft()   #Se anima el movimiento
        if (reaction == 'w_right') and self.rect.right < screen_width:
            self.MoveRight()           #Se mueve a la derecha
            self.AnimationMoveRight()  #Se anima el movimiento
        if (reaction == 'jump') and self.isJump is False:
            self.isJump = True

        self.jump()
        self.HealthBar()
        

#create Bullets class
class Bullets(pygame.sprite.Sprite):
    
    def __init__(self, x, y, look):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadSprite("shot_player.png")
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
        if (pygame.sprite.spritecollide(self, nemesis_group,False) #s[current_nemesis]
            and nemesis.isBlocked is False):
            self.kill()
            nemesis.damage()
        if (pygame.sprite.spritecollide(self, nemesis_group,False)
            and nemesis.isBlocked is True):
            self.kill()
            

#Create Enemy Bullets Class  : Se crea para que tengan diferentes colliders a la clase Bullets normal

class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, look):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadSprite("shot_nemesis.png")
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
bullet_group = pygame.sprite.Group()
nemesis_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()

#create player (pos Anchor X, pos Anchor Y)
player = Player(TILE_SIZE, (HEIGHT-FLOOR)*TILE_SIZE - TILE_SIZE//2 )
player_group.add(player)

#create Nemesis_ss (pos Anchor X, pos Anchor Y)
nemesis = Nemesis(screen_width - TILE_SIZE*2, (HEIGHT-FLOOR)*TILE_SIZE - TILE_SIZE//2 )
nemesis_group.add(nemesis)


print('ancho del mundo',world_width)
# generate_groups()
run = True
while run:

    clock.tick(fps)

    #deaths
    if(player.healt <= 0):
        del player
        print("El player fue vencido en el nivel", current_level)
        break
    #current_nemesis
    # if(nemesis[current_nemesis].healt <= 1):
    if(nemesis.healt <= 1):
        #are_fighting = False
        #reiniciamos la salud del jugador
        player.healt = 100 
        print('nemesis a eliminar', current_nemesis)
        nemesis_group.empty()
        nemesis = Nemesis(screen_width - TILE_SIZE*2, (HEIGHT-FLOOR)*TILE_SIZE - TILE_SIZE//2 )
        nemesis_group.add(nemesis)
        current_nemesis += 1
        if current_nemesis >= num_nemesis :
            #SET NEW LEVEL
            current_level += 1
            current_nemesis = 0
            are_fighting = True
            print("duraciones:", [n.duration for n in nemesis_genes] )
            best_of_level, new_population = genes.newGeneration(nemesis_genes)
            print('Mejor del nivel',best_of_level)
            nemesis_genes = new_population
            # generate_groups()
            print('actual level',current_level)
    #draw background
    draw_bg()
    #FLOOR TILES | CAMERA
    if are_fighting is False:
        #si están peleando la pantalla se queda estática
        scroll_hor += (player.rect.x - scroll_hor) #= player.x?
    # world_width
    for x in range(world_width):
        screen.blit(base1, (x * TILE_SIZE - scroll_hor, (HEIGHT-FLOOR)*TILE_SIZE))
        for y in range(FLOOR-1):
            screen.blit(base2, (x * TILE_SIZE - scroll_hor, (HEIGHT-y-1)*TILE_SIZE))
    
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
            nemesis[current_nemesis].vulneravility()
        if event.type == pygame.USEREVENT +5 : 
            nemesis[current_nemesis].AnimationNormalBlock()
        if event.type == pygame.USEREVENT +6 : 
            nemesis[current_nemesis].AnimationNormalAttack()
            
    #update player
    player.update()
    nemesis.update(player.currAction)

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
