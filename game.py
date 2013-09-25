#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import os, random
from time import sleep

#DEBUG -- уровень дебага = 0..5
DEBUG = 4

# Для графики
#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
cell=20
W=25
H=25
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def deb(debug ,mes):
    if debug <= DEBUG: print mes

class Board():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wariors = []
        deb( 2,"Initializing board "+str(x)+"x"+str(y)+" Complited")


    def deathWork(self):
        for warior in self.wariors:
            if warior.hp <=0:
                deb(1,"Warior "+warior.name+" is dead now")
                self.wariors.remove(warior)

    def addWarior(self,warior):
        if warior not in self.wariors:
            self.wariors.append(warior)
            deb(2, "added warior,named "+warior.name+" to position "+str(warior.x)+"x"+str(warior.y)+" and his hp="+str(warior.hp))


    def getWariorByPos(self,(x,y)):
        for war in self.wariors:
            if war.x == x and war.y == y:
                return war
        return None

    def getWill(self):
        bestWar= None
        bestWill = 0
        for war in self.wariors:
            if war.curWill > bestWill:
                deb(2,"Warior "+war.name+" with will "+str(war.curWill))
                bestWar = war
                bestWill= war.curWill
        deb (3,"Best warior is "+str(bestWar)+" his name is "+str(bestWar.name) +"he has will="+str(bestWar.will))
        return bestWar

    def countWariors(self):
        return len(self.wariors)

    def draw(self,screen):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(W*cell, 0, 400, H*cell))
        pygame.draw.rect(screen, (0, 26, 48), pygame.Rect(0, 0, W*cell, H*cell))
        for war in self.wariors:
            war.draw(screen)
        l = 20
        for war in self.wariors:
            war.drawChars(screen,W*cell + 45 , l)
            l+= 30
        line = ""
        #os.system('clear')
#        print "##"*(self.x+1)
#        for a in range (self.y):
#            line ="#"
#            for b in range(self.x):
#                printed = False
#                for war in self.wariors:
#                    if war.x ==  b and war.y == a:
#                        printed = True
#                        line+= war.name
#                        break
#                if not printed:
#                    line += "_"
#                if b < self.x-1:
#                    line +="|"
#            print line+"#"
#        print "##"*(self.x+1)
#        print


class Warior():
    def __init__ (self,name,hp,x,y,dam,will,human=False):
        self.name=name
        self.hp=hp
        self.x=x
        self.y=y
        self.dam=dam
        self.will=will
        self.curWill = will
        if human:
            self.human = True
        else:
            self.human = False
            
        self.color = (random.randrange(10,255),random.randrange(10,255),random.randrange(10,255))

    def hit (self,enemy):
        enemy.hp = enemy.hp - self.dam

    def getNearestEnemy(self,board):
        deb(3,"Looking for the nearest enemy")
        deb(3,"The hero is "+str(self))
        nearWar=Warior("",0,9999,9999,0,0)
        mindxy = 9999
        for war in board.wariors:
            if war == self:
                continue
            dx = war.x - self.x
            dy = war.y - self.y
            if dx**2+dy**2 < mindxy:
                mindxy = dx**2+dy**2
                nearWar = war
                deb(3,"Aha, here he is "+str(nearWar.name))
        if nearWar.name == "":
            return None
        deb(3,"The enemy is "+str(nearWar))
        return nearWar

    def moveToWar(self,enemy):
        deb(3,"How should he goes...")
        deb(3,"my x="+str(self.x)+" y="+str(self.y))
        deb(3,"his x="+str(enemy.x)+" y="+str(enemy.y))
        if abs(self.x-enemy.x) >= abs(self.y - enemy.y):
            if self.x > enemy.x:
                return "l"
            else:
                return "r"
        else:
            if self.y > enemy.y:
                return "u"
            else:
                return "d"
            
            
    def updateWarior(self,board,d):
        if self in board.wariors:
            if (self.x == 0 and d == "l") or (self.x == board.x-1 and d == "r") or (self.y == 0 and d == "u") or (self.y == board.y-1 and d == "d"):
                return 1

            if   d == "u" :newPos = (self.x,self.y - 1)
            elif d == "d" :newPos = (self.x,self.y + 1)
            elif d == "l" :newPos = (self.x- 1,self.y )
            elif d == "r" :newPos = (self.x+ 1,self.y )
            deb(2,"Now "+self.name+" wants to move to "+str(newPos))
            deb(2,"Trying to get warior by position"+str(newPos))
            enemy = board.getWariorByPos(newPos)
            if enemy != None:
                deb(2,self.name+" have seen "+enemy.name+" on " +str(newPos))
                self.hit(enemy)
                deb(1," Now "+enemy.name+" has " +str(enemy.hp))

            else:
                self.x,self.y = newPos
                deb(1,"Now "+self.name+" moved to "+str(newPos))
            board.deathWork()
            
            
    def draw(self, screen): # Выводим себя на экран
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x*cell, self.y*cell, cell, cell))
        
    def drawChars(self, screen,x,y): # Выводим себя на экран
        pygame.draw.rect(screen, self.color, pygame.Rect(x, y, cell, cell))
        # set up fonts
        basicFont = pygame.font.SysFont(None, 24)
        
        # set up the text
        text = basicFont.render(str(self.hp), True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = x + 40
        textRect.centery = y + 10
        screen.blit(text, textRect)



class Game:
    def __init__(self,board):
        self.board = board
        self.main()



    def endTurn(self,warior):
        warior.curWill = 0
        will =0
        for war in self.board.wariors:
            will += war.curWill
        if will == 0:
            deb(2,"Everyone has no will,the turn will end now")
            for war in self.board.wariors:
                war.curWill += war.will
                deb(3,"Warior "+str(war)+" has will="+str(war.curWill))
                
#    def control(self):
#        """Handle the controls of the game."""
#
#        keys = pygame.key.get_pressed()
#
#        def pressed(key):
#            """Check if the specified key is pressed."""
#
#            return self.pressed_key == key or keys[key]
#
#
#
#        if pressed(pg.K_UP):
#            pass
#        elif pressed(pg.K_DOWN):
#            pass
#        elif pressed(pg.K_LEFT):
#            pass
#        elif pressed(pg.K_RIGHT):
#            pass
#        self.pressed_key = None
        
    def main(self):
        pygame.init() # Инициация PyGame, обязательная строчка 
        screen = pygame.display.set_mode((W*cell+400, H*cell)) # Создаем окошко
        pygame.display.set_caption("Board game") # Пишем в шапку
        done = False
        clock = pygame.time.Clock()
        self.board.draw(screen)
        while not done:
            if self.board.countWariors() <= 1: break
            curWar = self.board.getWill()
            deb (1,"It time to go,"+str(curWar.name))
            if not curWar.human:
                enemy = curWar.getNearestEnemy(self.board)
                deb(2,"In main enemy is "+str(enemy.name))
                direction = curWar.moveToWar(enemy)
                
            else:
                
                turnMade = False
                deb(2,"wait for key pressed")

                while  turnMade == False:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                    pressed = pygame.key.get_pressed()
                    deb(20,str(pressed))
                    turnMade = True
                    if pressed [pygame.K_LEFT]:
                        direction = "l"
                    elif pressed [pygame.K_RIGHT]:
                        direction = "r"
                    elif pressed [pygame.K_UP]:
                        direction = "u"   
                    elif pressed [pygame.K_DOWN]:
                        direction = "d"    
                    else:
                        turnMade = False                                       

                        
            curWar.updateWarior(self.board,direction)
            self.endTurn(curWar)
            deb(2,"Now you should press Enter")
            self.board.draw(screen)
            pygame.display.flip()
            pygame.display.update() 
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done


                



board = Board(W,H)
war = Warior("J",5,0,0,15,5)
board.addWarior(war)
#war2 = Warior("A",100,0,24,1,3,True)
#board.addWarior(war2)
# Можно поиграться и добавить дополнительных ботов
war3 = Warior("B",100,0,H-1,1,7)
board.addWarior(war3)
war4 = Warior("C",100,W-1,H-1,25,1)
board.addWarior(war4)
new_game = Game(board)
#pygame.init()
#screen = pygame.display.set_mode((W*cell, H*cell)) # Создаем окошко
#pygame.display.set_caption("Board game") # Пишем в шапку
#done = False
#clock = pygame.time.Clock()
#while not done:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#                done = True
#        board.draw(screen)
#        pygame.display.flip()
#        clock.tick(30)
#DISPLAYSURF = pygame.display.set_mode((400, 300))
#pygame.display.set_caption('Hello World!')

