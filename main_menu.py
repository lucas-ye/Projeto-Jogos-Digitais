import pygame as pg
import state
import info, mario
import main

class Menu(state._State):
    def __init__(self):
        """Initializes the state"""
        self.next = None
        self.current_state = "main_menu"
        state._State.__init__(self)
        persist  = {"score": 0,
                   "lives": 3,
                   "top_score": 0, # vai ser substituido por ranking
                   "sound": True,
                   "current_time": 0.0,
                   "level_state": None,
                   "camera_start": 0,
                   "level": 1,
                   "mario_dead": False}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):
        """Called every time the game's state becomes this one.  Initializes
        certain values"""
        self.next = 'load_screen'
        self.persist = persist
        self.game_info = persist
        self.overhead_info = info.OverheadInfo(self.game_info, 'main_menu')

        self.sprite_sheet = pg.image.load("./resources/graphics/title_screen1.png")
        self.setup_background()
        self.setup_mario()
        self.setup_cursor()


    def setup_cursor(self):
        """Creates the mushroom cursor to select 1 or 2 player game"""
        self.cursor = pg.sprite.Sprite()
        dest = (260, 373)
        self.cursor.image, self.cursor.rect = self.get_image(
            24, 160, 8, 8, dest, pg.image.load("./resources/graphics/item_objects.png"))
        self.cursor.state = "PLAY"


    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario(False, None)
        self.mario.rect.x = 90
        self.mario.rect.bottom = main.SCREEN_HEIGHT - 62


    def setup_background(self):
        """Setup the background image to blit"""
        self.background = pg.image.load("./resources/graphics/level_1.png")
        self.background_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                   (int(self.background_rect.width*2.679),
                                    int(self.background_rect.height*2.679)))
        self.viewport = main.SCREEN.get_rect(bottom=main.SCREEN_RECT.bottom)

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.get_image(
            1, 60, 176, 88, (170, 100), self.sprite_sheet)



    def get_image(self, x, y, width, height, dest, sprite_sheet):
        """Returns 图片 and rects to blit onto the screen"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        if sprite_sheet == self.sprite_sheet:
            image.set_colorkey((255, 0, 220))
            image = pg.transform.scale(image,
                                   (int(rect.width*2.5),
                                    int(rect.height*2.5)))
        else:
            image.set_colorkey((0, 0, 0))
            image = pg.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)


    def update(self, surface, keys, current_time, keydown):
        """Updates the state every refresh"""
        self.current_time = current_time
        self.game_info["current_time"] = self.current_time
        self.update_cursor(keys, keydown)
        self.overhead_info.update(self.game_info)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.mario.image, self.mario.rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)


    def update_cursor(self, keys, keydown):
        """Update the position of the cursor"""
        if keydown:
            if self.cursor.state == "PLAY":
                if keys[pg.K_DOWN]:
                    self.cursor.state = "INSTRUCTION"
                    self.cursor.rect.x = 237
                    self.cursor.rect.y = 418
                elif keys[pg.K_RETURN]:
                    self.reset_game_info()
                    self.done = True
            elif self.cursor.state == "INSTRUCTION":
                if keys[pg.K_UP]:
                    self.cursor.state = "PLAY"
                    self.cursor.rect.x = 260
                    self.cursor.rect.y = 373
                elif keys[pg.K_DOWN]:
                    self.cursor.state = "SOUND"
                    self.cursor.rect.x = 134
                    self.cursor.rect.y = 463
            elif self.cursor.state == "SOUND":
                if keys[pg.K_UP]:
                    self.cursor.state = "INSTRUCTION"
                    self.cursor.rect.x = 237
                    self.cursor.rect.y = 418
                elif keys[pg.K_RETURN]:
                    if self.game_info["sound"]:
                        self.game_info["sound"] = False
                        print("som desligado")
                    else:
                        self.game_info["sound"] = True
                        print("som ligado")
    def reset_game_info(self):
        """resetar as informacoes do jogo"""
        self.game_info["score"] = 0
        self.game_info["lives"] = 3
        self.game_info["current_time"] = 0.0
        self.game_info["level_state"] = None

        self.persist = self.game_info