# -*- coding: utf-8 -*-

import pygame
#from time import sleep
from character import Warior
from config import *
from board import Board


        







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

                


if  __name__ ==  "__main__" :
    board = Board(W,H)
    war = Warior("J",500,0,0,15,5,True,spd=4)
    board.addWarior(war)
    war3 = Warior("B",100,4,H-1,1,7,spd=3)
    board.addWarior(war3)
    war4 = Warior("C",100,W-1,H-1,25,1)
    board.addWarior(war4)
    new_game = Game(board)
