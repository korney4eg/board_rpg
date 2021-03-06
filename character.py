#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

import random
from config import *
import time

class Weapon:
    def __init__(self,name,range,damage):
        self.name = name
        self.range = range
        self.damage = damage
        
    def getRange(self):
        return self.range    
    
    def getDamage(self):
        return self.damage 
    
    def getName(self):
        return self.name       
        
class Atack:
    
    def __init__(self,person):
        self.person = person
        if self.person.__class__.__name__ =="Warior":
            self.points = 1

        elif self.person.__class__.__name__ =="Archer":
            self.points = 2

        elif self.person.__class__.__name__ =="Mage":
            self.points = 2
        self.range = self.person.weapon.getRange()
                
    def getRange(self):
#         self.range =  self.person.PER / 3
#         if self.range == 0:
#             self.range = 1
        return self.range
    
    
    def isEnough(self,points):
        return self.points <= points
    
    def getDamage(self):
        if self.person.__class__.__name__ =="Warior":
            self.dam = self.person.STR
        elif self.person.__class__.__name__ =="Archer":
            self.dam = self.person.PER
        elif self.person.__class__.__name__ =="Mage":
            self.dam = self.person.INT
        self.dam += self.person.weapon.getDamage()
        # Critical strike
        if random.randrange(100) < 2 * self.person.LCK:
            self.dam *= 2
            print "Critical damage", self.dam
        else:
            print "damage = ",self.dam
        return self.dam
    
class Armor:
    def __init__(self,person):
        self.person = person
        self.armor = self.person.AGL
        self.missChance = self.person.AGL
    
    def getArmor(self):
        if random.randrange(100) < self.missChance:
            print "missed!",self.armor
            return self.armor*1000
        else:
            print "armor = ",self.armor
            return self.armor
    
class Team:
    def __init__(self, name):
        self.name = name
        self.wariors = []
        
    def addToTeam(self,warior):
        self.wariors.append(warior)
        warior.team = self.name
        
    def addTeamToBoard(self,board):
        for war in self.wariors:
            board.addPerson(war)
            
    def changePic(self,pic):
        for war in self.wariors:
            war.changePic(pic)        
            


class Person():
    def __init__ (self,name,x,y,will,human=False, team = ""):
        """                имя    hp    x     y      dam    will     hum
        war2 = Person("A",    100,   0,    24,    1,    3,        True) --- это объявление бойца
         Пояснения:
         имя  -- имя бойца, пока нигде не пишется и не фигурирует
         hp  --  здоровье бойца. Когда становиться = 0, боец погибает и пропадает с поля
          x  -- координата x на поле, максимальна == длина поля -1
         y  -- координата y на поле , максимальна == высота поля -1
         dam -- урон, наносимый противнику
         will -- воля, у кого больше, тот раньше ходит
         hum -- боец управляется человеком или компом. Если стоит значение True, то управлнеие человеком, если ничего или False  - бот
        
         Следующая команда добавляет созданного бойца на поле
        board.addPerson(war2)
         Можно поиграться и добавить дополнительных ботов"""
        self.name=name
        self.getBase()
        self.getSPECIAL()
        self.refresh()
        self.wearWeapon()
        self.x=x
        self.y=y
        self.hp = self.maxHP
        self.mp = self.maxMP
        self.will=will
        self.curWill = will
        if team == "":
            self.team = str(random.randint(1,64000))
        else:
            self.team = team
        if human:
            self.human = True
        else:
            self.human = False
        self.curPoints = self.Points
        self.current = False
        self.pic = None
        self.getPic()
        self.atack = Atack(self)
        self.armor = Armor(self)

    def getBase(self):
        self.STR = 0
        self.PER = 0
        self.END = 5
        self.INT = 0
        self.AGL = 2
        self.LCK = 0
        
    
    def changeParm(self,parm,value):
        if parm in ['STR','PER','END','INT','AGL','LCK']:
            if parm == 'STR':
                self.STR = value
            elif parm == 'PER':
                self.PER += value
            elif parm == 'END':
                self.END += value
            elif parm == 'END':
                self.END += value
            elif parm == 'INT':
                self.INT += value
            elif parm == 'AGL':
                self.AGL += value
            elif parm == 'LCK':
                self.LCK += value
                    
                    
    def refresh(self):
        self.Points = self.AGL
        self.maxHP = self.END * 2
        self.maxMP = self.INT * 2
        
        
    def getSPECIAL(self):
        pass

    def getPic(self):
        self.image = ""
        
    def wearWeapon(self):
        self.weapon = Weapon("Club",1,0)
            
   
    def hit (self,enemy):
        dam = self.atack.getDamage() - enemy.armor.getArmor()
        if  dam > 0:
            enemy.hp = enemy.hp - dam
        self.curPoints -= self.atack.points
        
    def moveTo(self,board,(x,y)):
        if board.getPersonByPos == None:
            self.x = x
            self.y = y
            
    def changePic(self,pic):
        self.pic = pygame.image.load(pic).convert
        #self.image = pic

    def getNearestEnemy(self,board):
        deb(3,"Looking for the nearest enemy")
        deb(3,"The hero is "+str(self))
        nearWar=Person("",0,9999,9999,0,0)
        mindxy = 9999
        for war in board.wariors:
            if war.team == self.team:
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
    
    def animateHit(self,screen, aim):
        if self.__class__.__name__ =="Mage":
            ballsurf = pygame.Surface((4, 4))
            ballsurf.set_colorkey((0, 0, 0))
            pygame.draw.circle(ballsurf, MAGIC_BALL, (2, 2), 2)
            ballsurf = ballsurf.convert()
            rect = ballsurf.get_rect()
            rect.topleft = (self.x*cell,self.y*cell)
            while rect.x < aim[0] and rect.y < aim[1]:
                dx = (rect.x - aim[0])/30
                dy = (rect.y - aim[1])/30
                move_ip(dx,dy)
                screen.blit(ballsurf, rect) 
                pygame.display.flip()
                pygame.display.update()
      
                        
    def findNextPosTo(self,board,pos):
        """ find best path to position"""
        #TODO implement labirynth
        m,b,c = board.getMoves(self)
        minDist = 1000
        for move in MOVES.values():
            newPos = self.x+move[0],self.y+move[1]
            if newPos in m:
                dist =  getDistance(newPos,pos)
                if dist < minDist:
                    bestPath =  newPos
                    minDist = dist
        return   bestPath                
    
    def updateBot(self,board,screen = ""):
        """ board - is our plaing board
        here is AI programmed"""
        if self.curPoints == 0:
            return 
        enemy = self.getNearestEnemy(board)
        if getDistance((self.x,self.y),(enemy.x,enemy.y))<= self.atack.getRange() and self.atack.isEnough(self.curPoints):
            #shut
            self.animateHit(board.screen,(enemy.x,enemy.y))
            self.hit(enemy)
        elif ( self.curPoints < self.atack.points):
                # if attacked and have no more points to another atack, just wait
            self.curPoints = 0   
        else:
            #find path to enemy
            self.x,self.y = self.findNextPosTo (board,(enemy.x,enemy.y))
            self.curPoints -= 1
        board.deathWork()
        
        
    def updatePerson(self,board,pos):
        moves, hits, shut = board.getMoves(self)
        attacked = False
        if board.getByPos((pos[0], pos[1])) == 2 and \
        getDistance((self.x, self.y), (pos[0],pos[1])) <= self.atack.getRange()\
        and self.atack.isEnough(self.curPoints):
            enemy = board.getPersonByPos((pos[0],pos[1]))
            if self.team != enemy.team:
                self.animateHit(board.screen,(enemy.x,enemy.y))
                self.hit(enemy)
        elif (pos[0],pos[1]) in moves or (pos[0],pos[1]) in hits:
            while ((pos[0],pos[1]) != (self.x, self.y)) and (not attacked):
                self.x,self.y = self.findNextPosTo (board,pos)
                self.curPoints -= 1
                if board.getByPos(pos) == 2:
                    attacked = True

        board.deathWork()
            
    def ima(self,screen,x,y):
        if self.image != "":
            if self.pic == None:
                self.pic = pygame.image.load(self.image).convert_alpha()
            screen.blit(self.pic, (x,y-1))
            
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
        pygame.draw.circle(screen, COL, (x-35, y+113), 2)
        
        basicFont = pygame.font.SysFont(None, 24)
        
        # set up the text
        text = basicFont.render(self.name, True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.x = x + 50
        textRect.y = y + 10
        screen.blit(text, textRect)
        pygame.draw.rect(screen, RED, pygame.Rect(x+100, y, 100, 6))    
        pygame.draw.rect(screen, GREEN, pygame.Rect(x+100, y, self.hp*1.0/self.maxHP*100, 6)) 
        if self.curPoints > 0:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(x+100, y+10 , self.curPoints*1.0/self.Points*100, 6)) 

        
class Warior(Person):
    
    def getPic(self):
        self.image =  SOLDIER_PIC
    
    def getSPECIAL(self):
        self.STR += 5
        self.PER += 2
        self.END += 4
        self.INT += 1
        self.AGL += 3
        self.LCK += 3    
           
    def wearWeapon(self):
        self.weapon = Weapon("Axe",1,4)
        
class Archer(Person):
    def getPic(self):
        self.image =  ARCHER_PIC
        
    def getSPECIAL(self):
        self.STR += 2
        self.PER += 4
        self.END += 3
        self.INT += 1
        self.AGL += 5
        self.LCK += 3 
    def wearWeapon(self):          
        self.weapon = Weapon("Bow",6,3)
     
class Mage(Person):
    def getPic(self):
        self.image =  MAGE_PIC
        
    def getSPECIAL(self):
        self.STR += 1
        self.PER += 3
        self.END += 2
        self.INT += 6
        self.AGL += 3
        self.LCK += 3 
    
    def wearWeapon(self):  
        self.weapon = Weapon("Wand",6,3)   
if  __name__ ==  "__main__" :  pass