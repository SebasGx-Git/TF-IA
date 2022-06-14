from sre_constants import JUMP
from tkinter import SEL
import pygame
from pygame.locals import *
import threading

Clock = pygame.time.Clock()
FPS = 60

class Attack:
    def __init__(self, surface, x, y):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block_attack.jpg").convert()
        self.x = x
        self.y = y

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        self.parent_screen.blit(self.block, (self.x, self.y))
    
    def dissapear(self):
        self.kill()

class Player:
    def __init__(self, surface):
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block_shield = pygame.image.load("resources/block_shield.jpg").convert()
        self.block_attack = pygame.image.load("resources/block_attack.jpg").convert()
        self.x = 400
        self.y = 500
        self.look = True #Derecha , False Izquierda
        self.jump = False
        self.jump_high = 20
        self.isshield = False
        self.isattack = False
        self.jump_vel = self.jump_high

    def move_left(self):
        self.x -= 5
        self.look = False
        self.draw()

    def move_right(self):
        self.x += 5
        self.look = True
        self.draw()


    def move_jump(self):
        self.y -= self.jump_vel
        self.jump_vel -= 1
        if self.jump_vel < -(self.jump_high):
            self.jump = False 
            self.jump_vel = self.jump_high
        self.draw()
    
    def attack(self): 
        atk = Attack(self, self.x + 40, self.y)
        atk.draw()
        t = threading.Timer(1.5, atk.dissapear)
        t.start()

    def shield(self): 
        self.isshield = True
    
    def ofshield(self):
        self.isshield = False


    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        self.parent_screen.blit(self.block, (self.x, self.y))
        if self.isshield is True:
            self.parent_screen.blit(self.block_shield, (self.x, self.y))
        pygame.display.flip()

   

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((700, 700))
        
        self.player = Player(self.surface)

        
        
        Clock.tick(FPS)

        self.player.draw()

       


    def run(self):
        running = True
        
        while running:
            Clock.tick(FPS)
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()
            if keys[pygame.K_SPACE]:
                self.player.jump = True
            if keys[pygame.K_z]: 
                self.player.shield()
                pygame.time.set_timer(pygame.USEREVENT +1 , 1000) #ESTABLECE TIMER DEL ESCUDO
                
            if keys[pygame.K_x]:
                self.player.attack()



                


            if self.player.jump is True:
                self.player.move_jump()
            
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.USEREVENT +1 : 
                    self.player.ofshield()
                
            
            pygame.display.update()
            

if __name__ == '__main__':
    game = Game()
    game.run()
     
