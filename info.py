import os
import sys
import pygame as pg
from pygame.locals import *

# Constantes
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
CAPTION = "Projeto de Jogos Digitais"

class Character(pg.sprite.Sprite):
    """Parent class for all characters used for the overhead level info"""
    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OverheadInfo(object):
    """Class for level information like score, coin total,
        and time remaining"""
    def __init__(self, game_info, state):
        self.sprite_sheet = pg.image.load("./resources/graphics/text_images.png")
        self.time = 401
        self.current_time = 0
        self.total_lives = game_info["lives"]
        self.top_score = game_info["top_score"]
        self.state = state
        self.game_info = game_info

        self.create_image_dict()
        self.create_score_group()
        self.create_info_labels()
        self.create_load_screen_labels()
        self.create_countdown_clock()
        self.create_mario_image()
        self.create_game_over_label()
        self.create_time_out_label()
        self.create_main_menu_labels()


    def create_image_dict(self):
        """Creates the initial 图片 for the score"""
        self.image_dict = {}
        image_list = []

        image_list.append(self.get_image(3, 230, 7, 7))  # 0
        image_list.append(self.get_image(12, 230, 7, 7)) # 1
        image_list.append(self.get_image(19, 230, 7, 7)) # 2
        image_list.append(self.get_image(27, 230, 7, 7)) # 3
        image_list.append(self.get_image(35, 230, 7, 7)) # 4
        image_list.append(self.get_image(43, 230, 7, 7)) # 5
        image_list.append(self.get_image(51, 230, 7, 7)) # 6
        image_list.append(self.get_image(59, 230, 7, 7)) # 7
        image_list.append(self.get_image(67, 230, 7, 7)) # 8
        image_list.append(self.get_image(75, 230, 7, 7)) # 9

        image_list.append(self.get_image(83, 230, 7, 7))  # a
        image_list.append(self.get_image(91, 230, 7, 7))  # b
        image_list.append(self.get_image(99, 230, 7, 7))  # c
        image_list.append(self.get_image(107, 230, 7, 7)) # d
        image_list.append(self.get_image(115, 230, 7, 7)) # e
        image_list.append(self.get_image(123, 230, 7, 7)) # f
        image_list.append(self.get_image(3, 238, 7, 7))   # g
        image_list.append(self.get_image(11, 238, 7, 7))  # h
        image_list.append(self.get_image(20, 238, 7, 7))  # i
        image_list.append(self.get_image(27, 238, 7, 7))  # j
        image_list.append(self.get_image(35, 238, 7, 7))  # k
        image_list.append(self.get_image(44, 238, 7, 7))  # l
        image_list.append(self.get_image(51, 238, 7, 7))  # m
        image_list.append(self.get_image(59, 238, 7, 7))  # n
        image_list.append(self.get_image(67, 238, 7, 7))  # o
        image_list.append(self.get_image(75, 238, 7, 7))  # p
        image_list.append(self.get_image(83, 238, 7, 7))  # q
        image_list.append(self.get_image(91, 238, 7, 7))  # r
        image_list.append(self.get_image(99, 238, 7, 7))  # s
        image_list.append(self.get_image(108, 238, 7, 7)) # t
        image_list.append(self.get_image(115, 238, 7, 7)) # u
        image_list.append(self.get_image(123, 238, 7, 7)) # v
        image_list.append(self.get_image(3, 246, 7, 7))   # w
        image_list.append(self.get_image(11, 246, 7, 7))  # x
        image_list.append(self.get_image(20, 246, 7, 7))  # y
        image_list.append(self.get_image(27, 246, 7, 7))  # z
        image_list.append(self.get_image(48, 248, 7, 7))  #  

        image_list.append(self.get_image(68, 249, 6, 2)) # -
        image_list.append(self.get_image(75, 247, 6, 6)) # *



        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image


    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((92, 148, 252))
        image = pg.transform.scale(image,
                                   (int(rect.width*2.9),
                                    int(rect.height*2.9)))
        return image


    def create_score_group(self):
        """Creates the initial empty score (000000)"""
        self.score_images = []
        self.create_label(self.score_images, '000000', 75, 55)


    def create_info_labels(self):
        """Creates the labels that describe each info"""
        self.mario_label = []
        self.world_label = []
        self.time_label = []
        self.stage_label = []


        self.create_label(self.mario_label, 'MARIO', 75, 30)
        self.create_label(self.world_label, 'LEVEL', 343, 30)
        self.create_label(self.time_label, 'TIME', 625, 30)
        self.create_label(self.stage_label, '1-1', 370, 55)

        self.label_list = [self.mario_label,
                           self.world_label,
                           self.time_label,
                           self.stage_label]


    def create_load_screen_labels(self):
        """Creates labels for the center info of a load screen"""
        world_label = []
        number_label = []

        self.create_label(world_label, 'WORLD', 280, 200)
        self.create_label(number_label, '1-1', 430, 200)

        self.center_labels = [world_label, number_label]


    def create_countdown_clock(self):
        """Creates the count down clock for the level"""
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)


    def create_label(self, label_list, string, x, y):
        """Creates a label (WORLD, TIME, MARIO)"""
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

        self.set_label_rects(label_list, x, y)


    def set_label_rects(self, label_list, x, y):
        """Set the location of each individual character"""
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)
            letter.rect.y = y
            print(i, letter.rect.x, letter.rect.y)
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2


    def create_mario_image(self):
        """Get the mario image"""
        self.life_times_image = self.get_image(75, 247, 6, 6)
        self.life_times_rect = self.life_times_image.get_rect(center=(378, 295))
        self.life_total_label = []
        self.create_label(self.life_total_label, str(self.total_lives),
                          450, 285)

        self.sprite_sheet = pg.image.load("./resources/graphics/mario_bros.png")
        self.mario_image = self.get_image(176, 0, 16, 32)
        self.mario_rect = self.mario_image.get_rect(center=(320, 290))


    def create_game_over_label(self):
        """Create the label for the GAME OVER screen"""
        game_label = []
        over_label = []

        self.create_label(game_label, 'GAME', 295, 300)
        self.create_label(over_label, 'OVER', 415, 300)

        self.game_over_label = [game_label, over_label]


    def create_time_out_label(self):
        """Create the label for the time out screen"""
        time_out_label = []

        self.create_label(time_out_label, 'TIME OUT', 297, 310)
        self.time_out_label = [time_out_label]


    def create_main_menu_labels(self):
        """Create labels for the MAIN MENU screen"""
        instruction = []
        play_game = []
        desligar_ligar_som = []
        top = []
        top_score = []

        self.create_label(play_game, 'PLAY GAME', 298, 315)
        self.create_label(instruction, 'INSTRUCTION', 275, 360)
        self.create_label(desligar_ligar_som, 'TURN OFF OR ON SOUND', 172, 405)
        self.create_label(top, 'TOP - ', 290, 465)
        self.create_label(top_score, '000000', 400, 465)

        self.main_menu_labels = [play_game, instruction, desligar_ligar_som,
                                 top, top_score]


    def update(self, level_info, mario=None):
        """Updates all overhead info"""
        self.mario = mario
        self.handle_level_state(level_info)


    def handle_level_state(self, level_info):
        """Updates info based on what state the game is in"""
        if self.state == "main_menu":
            self.score = level_info["score"]
            self.update_score_images(self.score_images, self.score)
            self.update_score_images(self.main_menu_labels[3], self.top_score)

        elif self.state == "load_screen":
            self.score = level_info["score"]
            self.update_score_images(self.score_images, self.score)

        elif self.state == "level":
            self.score = level_info["score"]
            self.update_score_images(self.score_images, self.score)
            if level_info["level_state"] != "frozen" \
                    and self.mario.state != "walking_to_castle" \
                    and self.mario.state != "end_of_level_fall" \
                    and not self.mario.dead:
                self.update_count_down_clock(level_info)

        elif self.state == "time_out":
            self.score = level_info["score"]
            self.update_score_images(self.score_images, self.score)

        elif self.state == "game_over":
            self.score = level_info["score"]
            self.update_score_images(self.score_images, self.score)

        elif self.state == "fast_count_down":
            level_info["score"] += 50
            self.score = level_info["score"]
            self.update_count_down_clock(level_info)
            self.update_score_images(self.score_images, self.score)
            if self.time == 0:
                self.state = "end_of_level"

        elif self.state == "end_of_level":
            pass


    def update_score_images(self, images, score):
        """Updates what numbers are to be blitted for the score"""
        index = len(images) - 1

        for digit in reversed(str(score)):
            rect = images[index].rect
            images[index] = Character(self.image_dict[digit])
            images[index].rect = rect
            index -= 1


    def update_count_down_clock(self, level_info):
        """Updates current time"""
        if self.state == "fast_count_down":
            self.time -= 1

        elif (level_info["current_time"] - self.current_time) > 400:
            self.current_time = level_info["current_time"]
            self.time -= 1
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)
        if len(self.count_down_images) < 2:
            for i in range(2):
                self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)
        elif len(self.count_down_images) < 3:
            self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)


    def draw(self, surface):
        """Draws overhead info based on state"""
        if self.state == "main_menu":
            self.draw_main_menu_info(surface)
        elif self.state == "load_screen":
            self.draw_loading_screen_info(surface)
        elif self.state == "level":
            self.draw_level_screen_info(surface)
        elif self.state == "game_over":
            self.draw_game_over_screen_info(surface)
        elif self.state == "fast_count_down":
            self.draw_level_screen_info(surface)
        elif self.state == "end_of_level":
            self.draw_level_screen_info(surface)
        elif self.state == "time_out":
            self.draw_time_out_screen_info(surface)
        else:
            pass



    def draw_main_menu_info(self, surface):
        """Draws info for main menu"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)
            temp = info.image
            temp_rect = info.rect
        surface.blit(temp, temp_rect)
        for label in self.main_menu_labels:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)



    def draw_loading_screen_info(self, surface):
        """Draws info for loading screen"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.center_labels:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for word in self.life_total_label:
            surface.blit(word.image, word.rect)

        surface.blit(self.mario_image, self.mario_rect)
        surface.blit(self.life_times_image, self.life_times_rect)


        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)



    def draw_level_screen_info(self, surface):
        """Draws info during regular game play"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for digit in self.count_down_images:
                surface.blit(digit.image, digit.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)



    def draw_game_over_screen_info(self, surface):
        """Draws info when game over"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.game_over_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)



    def draw_time_out_screen_info(self, surface):
        """Draws info when on the time out screen"""
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.time_out_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)


game_info  = {"score": 0,
                   "lives": 3,
                   "top_score": 0, # vai ser substituido por ranking
                   "current_time": 0.0,
                   "level_state": None,
                   "camera_start": 0,
                   "mario_dead": False}

os.environ['SDL_VIDEO_CENTERED'] = '1'
# iniciar pygame
pg.init()
# setar quais eventos sao aceitos
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)  
SCREEN.fill((100, 100, 100))
overhead_info = OverheadInfo(game_info, 'time_out')
# loop principal
overhead_info.draw(SCREEN)
pg.draw.line(SCREEN, (0, 0, 0), (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), 1)
while True:
    # SCREEN.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()


