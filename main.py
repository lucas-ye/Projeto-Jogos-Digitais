import os
import control
import pygame as pg
from pygame.locals import *
import main_menu, load_screen, level1, level2, level3

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

def main():
    """Add states to control here."""
    run_it = control.Control()
    state_dict = {"main_menu": main_menu.Menu(),
                  "load_screen": load_screen.LoadScreen(),
                  "time_out": load_screen.TimeOut(),
                  "game_over": load_screen.GameOver(),
                  "level1": level1.Level1(),
                  "level2": level2.Level2(),
                  "level3": level3.Level3(),
                }

    run_it.setup_states(state_dict, "main_menu")
    run_it.main()

if __name__=='__main__':
    main()