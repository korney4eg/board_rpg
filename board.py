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
        
    def getDistance(self, pos1, pos2):
        return round(math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2))
    
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
            if war.image == "":
                war.image = pygame.image.load(SOLDIER_PIC).convert_alpha()
            war.draw(screen)
#             if war.current:
#                 cur = war
                
        l = 20
        for war in self.wariors:
            war.drawChars(screen, W * cell + 45 , l)
            l += 30
        if self.curWar != None:
            self.drawTurn(screen, self.curWar)
        
    def getMoves(self, warior):
        moves = ["u", "d", "l", "r"]
        positions = [[(warior.x, warior.y)]]
        move = []
        hit = []
        
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
        if warior.atack.range > 1:
            for war in self.wariors:
                dist = self.getDistance((warior.x, warior.y), (war.x, war.y))
                if dist <= warior.atack.getRange() and warior.atack.isEnough(warior.curPoints)\
                and warior.team != self.getPersonByPos((war.x, war.y)).team:
                    hit.append((war.x, war.y))
        return move, hit
    
    def drawTurn(self, screen, warior):

        # print "it's done"
        move, hit = self.getMoves(warior)
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

    def onClick(self, pos):
        done = False
        onBx, onBy = pos[0] / cell, pos[1] / cell
        #print onBx, onBy
        moves, hits = self.getMoves(self.curWar)
        attacked = False
        if self.getByPos((onBx, onBy)) == 2 and \
        self.getDistance((self.curWar.x, self.curWar.y), (onBx, onBy))\
        and self.curWar.atack.isEnough(self.curWar.curPoints):
            enemy = self.getPersonByPos((onBx, onBy))
            if self.curWar.team != enemy.team:
                self.curWar.hit(enemy)
                self.deathWork()
                return
            
        # if self.curWar.atack.range >= self.getDistance(pos1, pos2)
        if (onBx, onBy) in moves or (onBx, onBy) in hits:
            while ((onBx, onBy) != (self.curWar.x, self.curWar.y)) and (not attacked):
                direction = self.curWar.goTo((onBx, onBy))
                newPos = (MOVES[direction][0] + self.curWar.x, MOVES[direction][1] + self.curWar.y)
                #print "next position", newPos
                if self.getByPos(newPos) == 2:
                    attacked = True
                    
                  #  print "I want to atack enemy from", (self.curWar.x, self.curWar.y), "to", (onBx, onBy)
                self.curWar.updatePerson(self, direction)