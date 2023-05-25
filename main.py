import os
import control
import pygame as pg
from pygame.locals import *
import main_menu

# Constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
CAPTION = "Hospital Run!"
SCREEN = pg.display.set_mode(SCREEN_SIZE)  
SCREEN_RECT = SCREEN.get_rect()
# centralizar a tela do jogo
os.environ['SDL_VIDEO_CENTERED'] = '1'
# iniciar pygame
pg.init()
# setar quais eventos sao aceitos
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(CAPTION)

# def main():

#     keys = pg.key.get_pressed()
#     current_time = pg.time.get_ticks()
#     menu = main_menu.Menu()
#     keydown = None
#     # loop principal
#     while True:

#         for event in pg.event.get():
#             if event.type == QUIT:
#                 pg.quit()
#                 sys.exit()
#             elif event.type == pg.KEYDOWN:
#                 keydown = True
#                 keys = pg.key.get_pressed()
#             elif event.type == pg.KEYUP:
#                 keys = pg.key.get_pressed()
        
#         menu.update(SCREEN, keys, current_time, keydown)
#         pg.display.update()
#         keydown = False

def main():
    """Add states to control here."""
    run_it = control.Control()
    state_dict = {"main_menu": main_menu.Menu()
                #   "load_screen": load_screen.LoadScreen(),
                #   "time_out": load_screen.TimeOut(),
                #   "game_over": load_screen.GameOver(),
                #   "level1": level1.Level1()
                }

    run_it.setup_states(state_dict, "main_menu")
    run_it.main()

if __name__=='__main__':
    main()