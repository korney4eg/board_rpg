from config import *
import pygame
import math

class Board():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xPx = self.x * cell
        self.yPx = self.y * cell
        self.wariors = []
        self.curWar = None
        self.teams = {}
        self.viewHealth =True
        deb(2, "Initializing board " + str(x) + "x" + str(y) + " Complited")


    def deathWork(self):
        for warior in self.wariors:
            if warior.hp <= 0:
                deb(1, "Person " + warior.name + " is dead now")
                print 
                self.teams[warior.team] -=1
                if self.teams[warior.team] == 0:
                    del self.teams[warior.team]
                self.wariors.remove(warior)


    def addPerson(self, warior):
        if warior not in self.wariors:
            self.wariors.append(warior)
            deb(2, "added warior,named " + warior.name + " to position " + str(warior.x) + "x" + str(warior.y) + " and his hp=" + str(warior.hp))
            if warior.team not in self.teams.keys():
                self.teams[warior.team] =1
            else:
                self.teams[warior.team] +=1
            
    def getByPos(self, (x, y)):
        if (x < 0) or (x >= self.x) or (y < 0) or (y >= self.y):
            return 100
        for war in self.wariors:
            if war.x == x and war.y == y:
                return 2
        return 1        
        

    
    def getPersonByPos(self, (x, y)):
        for war in self.wariors:
            if war.x == x and war.y == y:
                return war
        return None

    def getWill(self):
        bestWar = None
        bestWill = 0
        for war in self.wariors:
            if war.curWill > bestWill:
                deb(2, "Person " + war.name + " with will " + str(war.curWill))
                bestWar = war
                bestWill = war.curWill
        deb (3, "Best warior is " + str(bestWar) + " his name is " + str(bestWar.name) + "he has will=" + str(bestWar.will))
        self.curWar = bestWar
        return bestWar

    def countPersons(self):
        return len(self.wariors)
    
    def countTeams(self):
        return len(self.teams.items())

    def draw(self, screen):
        boardsurf = pygame.Surface((W * cell + 400, H * cell))
        boardPic = pygame.image.load('images/ground.png').convert()
        pygame.draw.rect(boardsurf, BLACK, pygame.Rect(W * cell, 0, 400, H * cell))
        # pygame.draw.rect(boardsurf, (0, 26, 48), pygame.Rect(0, 0, W*cell, H*cell))
        screen.blit(boardsurf, (0, 0))
        for w in range(W):
            for h in range(H):
                screen.blit(boardPic, (w * cell, h * cell))
        cur = None
        for war in self.wariors:
            war.draw(screen)
            self.drawHealth(screen,war)

#             if war.current:
#                 cur = war
                
        l = 20
        if self.curWar != None:
            self.curWar.drawChars(screen, W * cell + 45 , l)
        if self.curWar != None:
            self.drawTurn(screen, self.curWar)
        
    def drawHealth(self,screen,war):
        x,y = war.x *cell,war.y*cell
        if self.viewHealth:
            pygame.draw.rect(screen, RED, pygame.Rect(x, y+cell - 3, cell - 3, 2))    
            pygame.draw.rect(screen, GREEN, pygame.Rect(x, y+cell - 3, war.hp*1.0/war.maxHP*(cell - 3), 2)) 
            if war.curPoints > 0:
                pygame.draw.rect(screen, YELLOW, pygame.Rect(x, y+cell , war.curPoints*1.0/war.Points*(cell - 3), 2)) 
            
 
    def getMoves(self, warior):
        moves = ["u", "d", "l", "r"]
        positions = [[(warior.x, warior.y)]]
        move = []
        hit = []
        shut = []
        # print positions[0]
        
        while (len(positions[0]) <= warior.curPoints):

            pos = positions.pop(0)
            # print pos
            for mo in moves:
                pos2 = []
                newPos = pos[-1][0] + MOVES[mo][0], pos[-1][1] + MOVES[mo][1]
                # print "from",pos[-1],
                # print " I can go ", MOVES[mo]
                # print newPos
                getPos = self.getByPos(newPos)
                if  getPos == 1:
                    # print "found grass"
                    if newPos not in move:
                        # print "I wasn't here"rr

                        pos2 = pos + [newPos]
                        # print "now pos=",pos
                        move.append(newPos)
                        # print "moves are ",move
                        if pos not in positions:
                            positions.append(pos2)
                            # print "positions are ",positions
                elif getPos == 2:
                    if (newPos not in hit) and (warior.x != newPos[0] or warior.y != newPos[1]) \
                    and warior.team != self.getPersonByPos(newPos).team:
                        hit.append(newPos)
        
        if warior.atack.getRange() > 1:
            for war in self.wariors:
                dist = getDistance((warior.x, warior.y), (war.x, war.y))
                if dist <= warior.atack.getRange() and warior.atack.isEnough(warior.curPoints)\
                and warior.team != self.getPersonByPos((war.x, war.y)).team:
                    hit.append((war.x, war.y))
                    
            for w in range(W):
                for h in range(H):
                    dist = getDistance((warior.x, warior.y), (w, h))
                    if (dist <= warior.atack.getRange()) and ((w,h) not in hit) and ((warior.x, warior.y) != (w, h)):
                        shut.append((w,h)) 
        return move, hit, shut
    
    def drawTurn(self, screen, warior):

        # print "it's done"
        move, hit, shut = self.getMoves(warior)
        for m in move:
            movesurf = pygame.Surface((cell, cell)) 
            movesurf.set_colorkey((0, 0, 0)) 
            pygame.draw.circle(movesurf, MOVE_COLOR, (cell / 2, cell / 2), 4)
            movesurf = movesurf.convert()
            screen.blit(movesurf, (m[0] * cell, m[1] * cell))
        for h in hit:
            movesurf = pygame.Surface((cell, cell))
            movesurf.set_colorkey((0, 0, 0))
            pygame.draw.circle(movesurf, HIT_COLOR, (cell / 2, cell / 2), 4)
            movesurf = movesurf.convert()
            screen.blit(movesurf, (h[0] * cell, h[1] * cell))
        for s in shut:
            movesurf = pygame.Surface((cell, cell))
            movesurf.set_colorkey((0, 0, 0))
            pygame.draw.circle(movesurf, SHUT_COLOR, (cell / 2, cell / 2), 1)
            movesurf = movesurf.convert()
            screen.blit(movesurf, (s[0] * cell, s[1] * cell))        


    
    def onClick(self, pos):
        onBx, onBy = pos[0] / cell, pos[1] / cell
        self.curWar.updatePerson(self,(onBx, onBy))