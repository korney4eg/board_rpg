#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

import random
from config import *


class Atack:
    
    def __init__(self,range,dam,points):
        self.range = range
        self.dam = dam
        self.points = points
    
    def getRange(self):
        return self.range
    
    def getDamage(self):
        return self.dam
    
    def isEnough(self,points):
        return self.points <= points
    
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
    def __init__ (self,name,hp,x,y,dam,will,human=False,spd=1, team = ""):
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
        self.hp=hp
        self.x=x
        self.y=y
        self.dam=dam
        self.will=will
        self.curWill = will
        self.spd = spd
        if team == "":
            self.team = str(random.randint(1,64000))
        else:
            self.team = teeam
        if human:
            self.human = True
        else:
            self.human = False
        self.team = ""    
        self.color = (random.randrange(10,255),random.randrange(10,255),random.randrange(10,255))
        self.Points = spd
        self.curPoints = self.Points
        self.current = False
        self.pic = pygame.image.load(SOLDIER_PIC).convert
        self.image =  ""
        self.atack = Atack(25,dam,1)
        
    def hit (self,enemy):
        enemy.hp = enemy.hp - self.atack.getDamage()
        self.curPoints -= self.atack.points
        
    def moveTo(self,board,(x,y)):
        if board.getPersonByPos == None:
            self.x = x
            self.y = y
            
    def changePic(self,pic):
        self.pic = pygame.image.load(pic).convert

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
            
    def goTo(self,pos):
        if abs(self.x-pos[0]) >= abs(self.y - pos[1]):
            if self.x > pos[0]:
                return "l"
            else:
                return "r"
        else:
            if self.y > pos[1]:
                return "u"
            else:
                return "d"
                        
    def updatePerson(self,board,d):
        if d not in "udlr" or d =="": 
            return 0
        newPos = (MOVES[d][0]+self.x,MOVES[d][1]+self.y)

        deb(2,"Now "+self.name+" wants to move to "+str(newPos))
        deb(2,"Trying to get warior by position"+str(newPos))
        
        if board.getByPos(newPos) == 1:
            self.moveTo(board, newPos)
        enemy = board.getPersonByPos(newPos)
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
        pygame.draw.circle(screen, COL, (x-35, y+13), 2)
        
        basicFont = pygame.font.SysFont(None, 24)
        
        # set up the text
        text = basicFont.render(self.name+" "+str(self.hp), True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.centerx = x + 50
        textRect.centery = y + 10
        screen.blit(text, textRect)
        
        
if  __name__ ==  "__main__" :  pass