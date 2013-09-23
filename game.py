import pygame, os
from pygame.locals import *

DEBUG = True

def deb(mes):
    if DEBUG: print mes

class Board:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.wariors = []
        deb( "Initializing board "+str(x)+"x"+str(y)+" Complited")


    def deathWork(self):
        for warior in self.wariors:
            if warior.hp <=0:
                deb("Warior "+warior.name+" is dead now")
                self.wariors.remove(warior)

    def addWarior(self,warior):
        if warior not in self.wariors:
            self.wariors.append(warior)
            deb( "added warior,named "+warior.name+" to position "+str(warior.x)+"x"+str(warior.y)+" and his hp="+str(warior.hp))


    def getWariorByPos(self,(x,y)):
        for war in self.wariors:
            if war.x == x and war.y == y:
                return war
        return None

    def updateWarior(self,warior,d):
        if warior in self.wariors:
            if (warior.x == 0 and d == "l") or (warior.x == self.x and d == "r") or (warior.y == 0 and d == "u") or (warior.y == self.y and d == "d"):
                return 1

            if   d == "u" :newPos = (warior.x,warior.y - 1)
            elif d == "d" :newPos = (warior.x,warior.y + 1)
            elif d == "l" :newPos = (warior.x- 1,warior.y )
            elif d == "r" :newPos = (warior.x+ 1,warior.y )
            deb("Now "+warior.name+" wants to move to "+str(newPos))
            deb("Trying to get warior by position"+str(newPos))
            enemy = self.getWariorByPos(newPos)
            if enemy != None:
                deb(warior.name+" have seen "+enemy.name+" on " +str(newPos))
                warior.hit(enemy)
                deb(" Now "+enemy.name+" has " +str(enemy.hp))

            else:
                warior.x,warior.y = newPos
                deb("Now "+warior.name+" moved to "+str(newPos))
            self.deathWork()


    def getWill(self):
        bestWar= None
        bestWill = 0
        for war in self.wariors:
            if war.curWill > bestWill:
                deb("Warior "+war.name+" with will "+str(war.curWill))
                bestWar = war
                bestWill= war.curWill
        deb ("Best warior is "+str(bestWar)+" his name is "+str(bestWar.name) +"he has will="+str(bestWar.will))
        return bestWar



    def draw(self):
        line = ""
        #os.system('clear')
        print "##"*(self.x+1)
        for a in range (self.y):
            line ="#"
            for b in range(self.x):
                printed = False
                for war in self.wariors:
                    if war.x ==  b and war.y == a:
                        printed = True
                        line+= war.name
                        break
                if not printed:
                    line += "_"
                if b < self.x-1:
                    line +="|"
            print line+"#"
        print "##"*(self.x+1)
        print

class Warior:
    def __init__ (self,name,hp,x,y,dam,will):
        self.name=name
        self.hp=hp
        self.x=x
        self.y=y
        self.dam=dam
        self.will=will
        self.curWill = will

    def hit (self,enemy):
        enemy.hp = enemy.hp - self.dam

    def getNearestEnemy(self,board):
        deb("Looking for the nearest enemy")
        deb("The hero is "+str(self))
        nearWar=Warior("",0,0,0,0,0)
        mindxy = 100
        for war in board.wariors:
            if war == self:
                continue
            dx = war.x - self.x
            dy = war.y - self.y
            if dx**2+dy**2 < mindxy:
                mindxy = dx**2+dy**2
                nearWar = war
                deb("Aha, here he is "+str(nearWar.name))
        deb("The enemy is "+str(nearWar))
        return nearWar

    def moveToWar(self,enemy):
        deb("How should he goes...")
        deb("my x="+str(self.x)+" y="+str(self.y))
        deb("his x="+str(enemy.x)+" y="+str(enemy.y))
        if abs(self.x-enemy.x) >= abs(self.y - enemy.y):
            deb("x -x >= y - y")
            if self.x > enemy.x:
                return "l"
            else:
                return "r"
        else:
            if self.y > enemy.y:
                return "u"
            else:
                return "d"



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
            deb ("Everyone has no will,the turn will end now")
            for war in self.board.wariors:
                war.curWill += war.will
                deb("Warior "+str(war)+" has will="+str(war.curWill))

    def main(self):
        while len( self.board.wariors) > 1:
            self.board.draw()
            curWar = self.board.getWill()
            deb ("In main the hero"+str(curWar))
            enemy = curWar.getNearestEnemy(self.board)
            deb("In main enemy is "+str(enemy))
            direction = curWar.moveToWar(enemy)
            self.board.updateWarior(curWar,direction)
            raw_input("NExt turn ...")
            self.endTurn(curWar)



board = Board(5,5)
war = Warior("J",5,0,0,15,5)
board.addWarior(war)
war2 = Warior("A",100,4,4,1,3)
board.addWarior(war2)
new_game = Game(board)
new_game.board.draw()
#pygame.init()
#DISPLAYSURF = pygame.display.set_mode((400, 300))
#pygame.display.set_caption('Hello World!')

