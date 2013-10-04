from config import *
import pygame

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
