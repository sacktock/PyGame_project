import pygame
from pygame.locals import *
import os
import random
    
class Button(object):
    def __init__(self,x,y,width,height,text_color,background_color,text):
        self.rect=pygame.Rect(x,y,width,height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.text_color=text_color
        self.background_color=background_color
        self.angle=0

    def check(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.background_color,(self.rect),0)
        drawTextcenter(self.text,font,screen,self.x+self.width/2,self.y+self.height/2,self.text_color)  
        pygame.draw.rect(screen,self.text_color,self.rect,3)

def drawTextcenter(text,font,screen,x,y,color):
    textobj=font.render(text,True,color)
    textrect=textobj.get_rect(center=(x,y))
    screen.blit(textobj,textrect)

def drawText(text, font, surface, x, y,color):
    textobj=font.render(text, 1, color)
    textrect=textobj.get_rect(center=(x,y))
    surface.blit(textobj, textrect)
