# -*- coding: utf-8 -*-

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
W=20
H=20
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