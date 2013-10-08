# -*- coding: utf-8 -*-

import pygame
# from time import sleep
from character import Person, Team,Archer,Warior
from config import *
from board import Board
from interface import Interface


class Game:
    def __init__(self, board):
        self.board = board
        self.objects = {board:()}
        self.main()



    def endTurn(self, warior):
        warior.curWill = 0
        will = 0
        for war in self.board.wariors:
            will += war.curWill
        if will == 0:
            deb(2, "Everyone has no will,the turn will end now")
            for war in self.board.wariors:
                war.curWill += war.will
                deb(3, "Person " + str(war) + " has will=" + str(war.curWill))
                war.curPoints = war.Points
                
    def fight(self, screen):
        interface = Interface()
        interface.addObject(self.board, (0, 0))
        done = False
        clock = pygame.time.Clock()
        interface.draw(screen)
#        while not done:
        turnMade = False
        while self.board.countTeams() > 1 :
            if done: 
                exit() 
            curWar = self.board.getWill()
            curWar.current
            if curWar.curPoints == 0:
                turnMade = True            
            key = ""
            self.board.draw(screen)
            deb (1, "It time to go," + str(curWar.name))
            if not curWar.human:
                enemy = curWar.getNearestEnemy(self.board)
                deb(2, "In main enemy is " + str(enemy.name))
                direction = curWar.moveToWar(enemy)
#                moved = True
                curWar.updatePerson(self.board, direction)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True 
                if curWar.human: 
                    pos = pygame.mouse.get_pos() 
                    # print pos
                    if event.type == pygame.KEYDOWN:
#                         if event.key ==  pygame.K_LEFT:
#                             direction = "l"
#                         elif event.key ==  pygame.K_RIGHT:
#                             direction = "r"
#                         elif event.key ==  pygame.K_UP:
#                             direction = "u"   
#                         elif event.key ==  pygame.K_DOWN:
#                             direction = "d"
                        if event.key == pygame.K_SPACE:
                            turnMade = True
#                         if   direction in "udlr": 
                            # while not event.type == pygame.KEYUP: continue
                              
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        #print "left button clicked"
                        if event.button == 1:
                            # print pos
                            obj, intPos = interface.getObjectByPos(pos)
                            obj.onClick((pos[0] - intPos[0], pos[1] - intPos[1]))

            if turnMade:
                self.endTurn(curWar)
                turnMade = False
                curWar.current = False

            deb(2, "Now you should press Enter")
            
            pygame.display.flip()
            pygame.display.update() 
            clock.tick(5)

                
    def main(self):
        """ Main func """
        pygame.init()  # Инициация PyGame, обязательная строчка 
        screen = pygame.display.set_mode((W * cell + 400, H * cell))  # Создаем окошко
        pygame.display.set_caption("Board game")  # Пишем в шапку
        background = pygame.Surface(screen.get_size())
        background.fill(BLACK)  # fill the background white (red,green,blue)
        background = background.convert()  # faster blitting
        self.fight(screen)
                


if  __name__ == "__main__" :
    board = Board(W, H)
    team1 = Team("korney")
    team2 = Team("comp")
    #war = Person("J", 100, 0, 0, 15, 5, True, spd=4)
    war = Archer(name= "Arc", hp = 100, x = 0, y = 0, dam = 5, will = 6, human = True,spd=4)
    team1.addToTeam(war)
    war3 = Warior("Barb", 100, W - 10, H - 20, 10, 7,True, spd=3)
    team1.addToTeam(war3)
    #team1.changePic("images/archer.png")
    war4 = Warior("C", 100, W - 1, H - 1, 25,8, spd = 1)
    team2.addToTeam(war4)
    war5 = Warior("A", 100, 4, H - 1, 25,6,  spd = 1)
    team2.addToTeam(war5)
    team1.addTeamToBoard(board)
    team2.addTeamToBoard(board)
    new_game = Game(board)
