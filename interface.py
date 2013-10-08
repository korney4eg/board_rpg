#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame

from config import *

class Interface:
    def __init__(self):
        self.objects = {}
        
    def addObject(self,obj,pos):
        if obj not in self.objects.keys():
            self.objects[obj]=pos

    def clearInt(self):
        self.objects = {}
            
    def delObject(self,obj):
        if obj in self.objects.keys():
            self.objects.remove(obj)
    
    def draw(self,screen):
        for obj in self.objects:
            obj.draw(screen)
            
    def getObjectByPos(self,pos):
        for obj in self.objects.keys():
            if self.objects[obj][0]<= pos[0] <= self.objects[obj][0]+obj.xPx\
            and self.objects[obj][1]<= pos[1] <= self.objects[obj][1]+obj.yPx:
                return obj, self.objects[obj]
            
            

            