#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame
#from pygame.locals import *
import  random
from time import sleep

#DEBUG -- уровень дебага = 0..5
DEBUG = 0

# Для графики
#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
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
MOVE_COLOR = (255,255,102,52)
HIT_COLOR = (255,71,71,52) 
MOVES = {"u":(0,-1),"d":(0,1),"l":(-1,0),"r":(1,0)}

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

    def getByPos(self,(x,y)):
        if (x < 0 ) or (x >= self.x) or (y < 0) or (y >= self.y):
            return 100
        for war in self.wariors:
            if war.x == x and war.y == y:
                return 2
        return 1        
        
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
        boardsurf = pygame.Surface((W*cell+400,H*cell))
        boardPic = pygame.image.load('images/ground.png').convert()
        pygame.draw.rect(boardsurf, BLACK, pygame.Rect(W*cell, 0, 400, H*cell))
        #pygame.draw.rect(boardsurf, (0, 26, 48), pygame.Rect(0, 0, W*cell, H*cell))
        screen.blit(boardsurf,(0,0))
        for w in range(W):
            for h in range(H):
                screen.blit(boardPic,(w*cell,h*cell))
        cur = None
        for war in self.wariors:
            if war.image == "":
                war.image = pygame.image.load('images/soldier.png').convert_alpha()
            war.draw(screen)
            if war.current:
                cur = war
                
        l = 20
        for war in self.wariors:
            war.drawChars(screen,W*cell + 45 , l)
            l+= 30
        if cur!= None:
            self.drawTurn(screen,cur)
        
    def drawTurn(self,screen,warior):
        moves = ["u","d","l","r"]
        positions = [[(warior.x,warior.y)]]
        move = []
        hit = []
        
        #print positions[0]
        
        while (len(positions[0])<=warior.curPoints):

            pos = positions.pop(0)
            #print pos
            for mo in moves:
                pos2=[]
                newPos =  pos[-1][0] +MOVES[mo][0],pos[-1][1] +MOVES[mo][1]
                #print "from",pos[-1],
                #print " I can go ", MOVES[mo]
                #print newPos
                getPos = self.getByPos(newPos)
                if  getPos == 1:
                    #print "found grass"
                    if newPos not in move:
                        #print "I wasn't here"rr

                        pos2 = pos + [newPos]
                        #print "now pos=",pos
                        move.append(newPos)
                        #print "moves are ",move
                        if pos not in positions:
                            positions.append(pos2)
                            #print "positions are ",positions
                elif getPos == 2:
                    if (newPos not in hit) and (warior.x != newPos[0] or warior.y!= newPos[1]):
                        hit.append(newPos)
        #print "it's done"

        for m in move:
            movesurf = pygame.Surface((cell,cell)) 
            movesurf.set_colorkey((0,0,0)) 
            pygame.draw.circle(movesurf, MOVE_COLOR, (11, 11), 4)
            movesurf = movesurf.convert()
            screen.blit(movesurf,(m[0]*cell,m[1]*cell))
        for h in hit:
            
            pygame.draw.circle(movesurf, HIT_COLOR, (11, 11), 4)
            movesurf = movesurf.convert()
            screen.blit(movesurf,(h[0]*cell,h[1]*cell))

        



class Warior():
    def __init__ (self,name,hp,x,y,dam,will,human=False,spd=1):
        self.name=name
        self.hp=hp
        self.x=x
        self.y=y
        self.dam=dam
        self.will=will
        self.curWill = will
        self.spd = spd
        if human:
            self.human = True
        else:
            self.human = False
        self.team = ""    
        self.color = (random.randrange(10,255),random.randrange(10,255),random.randrange(10,255))
        self.Points = spd
        self.curPoints = self.Points
        self.current = False
        self.pic = pygame.image.load("images/soldier.png").convert
        self.image =  ""
    def hit (self,enemy):
        enemy.hp = enemy.hp - self.dam
        
    def moveTo(self,board,(x,y)):
        if board.getWariorByPos == None:
            self.x = x
            self.y = y

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


    def addToTeam(self,team):
        self.team = team
        
    def getTeam(self):
        return self.team
    
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
        if d not in "udlr" or d =="": 
            return 0
        newPos = (MOVES[d][0]+self.x,MOVES[d][1]+self.y)

        deb(2,"Now "+self.name+" wants to move to "+str(newPos))
        deb(2,"Trying to get warior by position"+str(newPos))
        
        if board.getByPos(newPos) == 1:
            self.moveTo(board, newPos)
        enemy = board.getWariorByPos(newPos)
        if enemy != None:
            deb(2,self.name+" have seen "+enemy.name+" on " +str(newPos))
            self.hit(enemy)
            deb(1," Now "+enemy.name+" has " +str(enemy.hp))

        else:
            self.x,self.y = newPos
            deb(1,"Now "+self.name+" moved to "+str(newPos))
        self.curPoints -= 1
        board.deathWork()
            
    def ima(self,screen,x,y):
        if self.image != "":
            screen.blit(self.image, (x,y))
        else:
            pygame.draw.rect(screen, self.color, pygame.Rect(x, y, cell, cell))

            
    def draw(self, screen): # Выводим себя на экран
        
        self.ima(screen,self.x*cell, self.y*cell)
        


    def drawChars(self, screen,x,y): # Выводим себя на экран
        
        self.ima(screen,x,y)
        if self.current:
            COL = GREEN
        else:
            COL = BLACK
        pygame.draw.circle(screen, COL, (x-15, y+13), 2)
        
        basicFont = pygame.font.SysFont(None, 24)
        
        # set up the text
        text = basicFont.render(self.name+" "+str(self.hp), True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = x + 50
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
                war.curPoints = war.Points
                
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
        background = pygame.Surface(screen.get_size())
        background.fill(BLACK)     # fill the background white (red,green,blue)
        background = background.convert()  # faster blitting
        done = False
        clock = pygame.time.Clock()
        self.board.draw(screen)
#        while not done:
        turnMade = False
        while self.board.countWariors() > 1 :
            if done: 
                exit() 
            curWar = self.board.getWill()
            curWar.current = True
            if curWar.curPoints == 0:
                turnMade = True
            
            key = ""
            self.board.draw(screen)
            deb (1,"It time to go,"+str(curWar.name))
            if not curWar.human:
                enemy = curWar.getNearestEnemy(self.board)
                deb(2,"In main enemy is "+str(enemy.name))
                direction = curWar.moveToWar(enemy)
                moved = True
                


            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True 
                if curWar.human and event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_LEFT:
                        direction = "l"
                    elif event.key ==  pygame.K_RIGHT:
                        direction = "r"
                    elif event.key ==  pygame.K_UP:
                        direction = "u"   
                    elif event.key ==  pygame.K_DOWN:
                        direction = "d"
                    elif event.key ==  pygame.K_SPACE:
                        turnMade = True
                    if   direction in "udlr": 
                        #while not event.type == pygame.KEYUP: continue
                        moved = True   
            if moved:
                curWar.updateWarior(self.board,direction)
                
                if direction !="":
                    direction = ""
                moved = False
            if turnMade:
                self.endTurn(curWar)
                turnMade = False
                curWar.current = False

            deb(2,"Now you should press Enter")
            
            pygame.display.flip()
            pygame.display.update() 
            clock.tick(5)

                

#                имя    hp    x     y      dam    will     hum
#war2 = Warior("A",    100,   0,    24,    1,    3,        True) --- это объявление бойца
# Пояснения:
# имя  -- имя бойца, пока нигде не пишется и не фигурирует
# hp  --  здоровье бойца. Когда становиться = 0, боец погибает и пропадает с поля
#  x  -- координата x на поле, максимальна == длина поля -1
# y  -- координата y на поле , максимальна == высота поля -1
# dam -- урон, наносимый противнику
# will -- воля, у кого больше, тот раньше ходит
# hum -- боец управляется человеком или компом. Если стоит значение True, то управлнеие человеком, если ничего или False  - бот
#
# Следующая команда добавляет созданного бойца на поле
#board.addWarior(war2)
# Можно поиграться и добавить дополнительных ботов

board = Board(W,H)
war = Warior("J",500,0,0,15,5,True,spd=4)
board.addWarior(war)
war3 = Warior("B",100,4,H-1,1,7,spd=3)
board.addWarior(war3)
war4 = Warior("C",100,W-1,H-1,25,1)
board.addWarior(war4)
new_game = Game(board)
