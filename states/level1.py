import os
import sys
import pygame as pg
from pygame.locals import *


# Constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
CAPTION = "Projeto de Jogos Digitais"


class Level1:
    def __init__(self, SCREEN):
        self.SCREEN = SCREEN

    # def startup(self, current_time, persist):
    #     """Called when the State object is created"""
    #     self.game_info = persist
    #     self.persist = self.game_info
    #     self.game_info[c.CURRENT_TIME] = current_time
    #     self.game_info[c.LEVEL_STATE] = c.NOT_FROZEN
    #     self.game_info[c.MARIO_DEAD] = False

    #     self.state = c.NOT_FROZEN
    #     self.death_timer = 0
    #     self.flag_timer = 0
    #     self.flag_score = None
    #     self.flag_score_total = 0

    #     self.moving_score_list = []
    #     self.overhead_info_display = info.OverheadInfo(self.game_info, c.LEVEL)
    #     self.sound_manager = game_sound.Sound(self.overhead_info_display)

    def setup_background(self):
        """Sets the background image, rect and scales it to the correct
        proportions"""
        self.background = pg.image.load("./resources/graphics/level1.png")
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                  (int(self.back_rect.width*2.679),
                                  int(self.back_rect.height*2.679)))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = self.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.game_info[c.CAMERA_START_X]

def main():
    # centralizar a tela do jogo
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # iniciar pygame
    pg.init()
    # setar quais eventos sao aceitos
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(CAPTION)
    SCREEN = pg.display.set_mode(SCREEN_SIZE)  
    # loop principal
    Level1 = Level1(SCREEN)
    while True:
        SCREEN.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

main()