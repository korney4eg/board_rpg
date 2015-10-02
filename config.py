# -*- coding: utf-8 -*-
import math
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
cell=32
W=20 # weight of the board
H=20 # height of the board
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255,239,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MOVE_COLOR = (255,255,102,52)
HIT_COLOR = (255,71,71,52) 
SHUT_COLOR = GREEN
MAGIC_BALL = (0,255,255)
MOVES = {"u":(0,-1),"d":(0,1),"l":(-1,0),"r":(1,0)}

#Picture of the soldier
SOLDIER_PIC="images/soldier.png"
ARCHER_PIC = "images/archer.png"
MAGE_PIC = "images/mage.png"
def deb(debug ,mes):
    if debug <= DEBUG: print mes
    
def getDistance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
