import os
import sys
import pygame as pg
from pygame.locals import *


# Constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
CAPTION = "Projeto de Jogos Digitais"

def mover():
    # centralizar a tela do jogo
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # iniciar pygame
    pg.init()
    # setar quais eventos sao aceitos
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(CAPTION)
    SCREEN = pg.display.set_mode(SCREEN_SIZE)  
    # loop principal
    while True:
        SCREEN.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

mover()