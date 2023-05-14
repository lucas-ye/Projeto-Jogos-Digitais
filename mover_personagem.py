import os
import sys
import pygame as pg
from pygame.locals import *


# Constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
CAPTION = "Projeto de Jogos Digitais"


class Mario():
    # construtor
    def __init__(self):
        self.right_mario_frame = []
        self.left_mario_frame = []
        self.mario_sprite_sheet = pg.image.load("./resources/graphics/mario_bros.png")
        self.mario_sprite_sheet = self.mario_sprite_sheet.convert_alpha()
        self.frame_index = 0
        self.mario_frame_init()
        self.image = self.right_mario_frame[self.frame_index]

    # obter frame do mario
    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        print(rect, rect.centerx)
        image.blit(self.mario_sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        image = pg.transform.scale(image,
                                    (int(rect.width*2.5),
                                    int(rect.height*2.5)))
        print(image.get_rect().center)
        return image

    # inicializar todos os frames do mario a partir do sprite_sheet
    def mario_frame_init(self):

        self.right_mario_frame.append(
            self.get_image(176, 0, 16, 32))  # Right standing [0]
        self.right_mario_frame.append(
            self.get_image(81, 0, 16, 32))  # Right walking 1 [1]
        self.right_mario_frame.append(
            self.get_image(97, 0, 15, 32))  # Right walking 2 [2]
        self.right_mario_frame.append(
            self.get_image(113, 0, 15, 32))  # Right walking 3 [3]
        self.right_mario_frame.append(
            self.get_image(144, 0, 16, 32))  # Right jump [4]
        self.right_mario_frame.append(
            self.get_image(128, 0, 16, 32))  # Right skid [5]
        self.right_mario_frame.append(
            self.get_image(160, 10, 16, 22))  # Right crouching [6]
        for frame in self.right_mario_frame:
            self.left_mario_frame.append(pg.transform.flip(frame, True, False))

    def mover(self, keys):
        # pular
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            print("pular")
        # para esquerda
        if keys[pg.K_LEFT]:
            print("esquerda")
        # para direita
        if keys[pg.K_RIGHT]:
            self.frame_index+=1
            if self.frame_index == 4:
                self.frame_index = 1
            print(self.frame_index)
            self.image = self.right_mario_frame[self.frame_index]
        # agachar
        if keys[pg.K_DOWN]:
            print("agachar")
def main():
    # centralizar a tela do jogo
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # iniciar pygame
    pg.init()
    # setar quais eventos sao aceitos
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(CAPTION)
    SCREEN = pg.display.set_mode(SCREEN_SIZE)  
    mario = Mario()

    # loop principal
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(mario.image, 
                    (SCREEN_WIDTH/2-mario.image.get_rect().centerx, 
                     SCREEN_HEIGHT - mario.image.get_rect().height - 20))
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                mario.mover(keys)
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
                mario.mover(keys)
        pg.display.update()

main()