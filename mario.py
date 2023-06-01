import os
import sys
import pygame as pg
from pygame.locals import *

class Mario(pg.sprite.Sprite):
    # construtor
    def __init__(self, reverse, reverse_time):
        pg.sprite.Sprite.__init__(self)
        self.right_mario_frame = []
        self.left_mario_frame = []
        self.mario_sprite_sheet = pg.image.load("./resources/graphics/mario_bros.png")
        self.mario_sprite_sheet = self.mario_sprite_sheet.convert_alpha()
        self.frame_index = 0
        self.mario_frame_init()
        self.image = self.right_mario_frame[self.frame_index]
        self.rect = self.image.get_rect()
        self.in_transition_state = False
        self.allow_jump = True
        self.facing_right = True
        self.dead = False
        self.state = "walk"

        self.reverse = reverse
        self.reverse_time = reverse_time
        self.death_timer = 0
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = 6
        self.max_y_vel = 11
        self.x_accel = 0.15
        self.jump_vel = -10
        self.gravity = 1.01

    # obter frame do mario
    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        image.blit(self.mario_sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        image = pg.transform.scale(image,
                                    (int(rect.width*2.5),
                                    int(rect.height*2.5)))
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

    def check_to_allow_jump(self, keys):
        """Verificar se pode pular"""
        if not (keys[pg.K_SPACE] or keys[pg.K_UP]):
            self.allow_jump = True

    def parado(self, keys):
        self.check_to_allow_jump(keys)

        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0
        if self.reverse:
            if keys[pg.K_LEFT]:
                self.facing_right = True
                self.state = "walk"
            elif keys[pg.K_RIGHT]:
                self.facing_right = False
                self.state = 'walk'
            elif keys[pg.K_SPACE] or keys[pg.K_UP]:
                if self.allow_jump:
                    self.state = 'jump'
                    self.y_vel = -10
            else:
                self.state = 'stand'
        else:
            if keys[pg.K_LEFT]:
                self.facing_right = False
                self.state = "walk"
            elif keys[pg.K_RIGHT]:
                self.facing_right = True
                self.state = 'walk'
            elif keys[pg.K_SPACE] or keys[pg.K_UP]:
                if self.allow_jump:
                    self.state = 'jump'
                    self.y_vel = -10
            else:
                self.state = 'stand'
    
    def jumping(self, keys):
        self.allow_jump = False
        self.frame_index = 4
        self.gravity = 0.31
        self.y_vel += self.gravity

        if self.y_vel >= 0 and self.y_vel < self.max_y_vel:
            self.gravity = 1.01
            self.state = 'fall'
        if self.reverse:
            if keys[pg.K_RIGHT]:
                if self.x_vel > (self.max_x_vel * - 1):
                    self.x_vel -= self.x_accel

            elif keys[pg.K_LEFT]:
                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel
        else:
            if keys[pg.K_LEFT]:
                if self.x_vel > (self.max_x_vel * - 1):
                    self.x_vel -= self.x_accel

            elif keys[pg.K_RIGHT]:
                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel

        if not (keys[pg.K_SPACE] or keys[pg.K_UP]):
            self.gravity = 1.01
            self.state = "fall"

    def falling(self, keys):
        """Called when Mario is in a FALL state"""
        if self.y_vel < 11:
            self.y_vel += self.gravity
        if self.reverse:
            if keys[pg.K_RIGHT]:
                if self.x_vel > (self.max_x_vel * - 1):
                    self.x_vel -= self.x_accel
            elif keys[pg.K_LEFT]:
                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel
        else:
            if keys[pg.K_LEFT]:
                if self.x_vel > (self.max_x_vel * - 1):
                    self.x_vel -= self.x_accel
            elif keys[pg.K_RIGHT]:
                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel

    def walking(self, keys):
        self.check_to_allow_jump(keys)
        if self.frame_index == 0:
            self.frame_index += 1
            self.walking_timer = self.current_time
        else:
            if (self.current_time - self.walking_timer >
                    self.calculate_animation_speed()):
                if self.frame_index < 3:
                    self.frame_index += 1
                else:
                    self.frame_index = 1

                self.walking_timer = self.current_time
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            if self.allow_jump:
                # setup.SFX['big_jump'].play()
                self.state = 'jump'
                if self.x_vel > 4.5 or self.x_vel < -4.5:
                    self.y_vel = -10 - .5
                else:
                    self.y_vel = -10
        if self.reverse:
            if keys[pg.K_RIGHT]:
                self.facing_right = False
                if self.x_vel > 0:
                    self.frame_index = 5
                    self.x_accel = 0.35
                else:
                    self.x_accel = 0.15

                if self.x_vel > (self.max_x_vel * -1):
                    self.x_vel -= self.x_accel
                    if self.x_vel > -0.5:
                        self.x_vel = -0.5
                elif self.x_vel < (self.max_x_vel * -1):
                    self.x_vel += self.x_accel

            elif keys[pg.K_LEFT]:
                self.facing_right = True
                if self.x_vel < 0:
                    self.frame_index = 5
                    self.x_accel = 0.35
                else:
                    self.x_accel = 0.15

                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel
                    if self.x_vel < 0.5:
                        self.x_vel = 0.5
                elif self.x_vel > self.max_x_vel:
                    self.x_vel -= self.x_accel

            else:
                if self.facing_right:
                    if self.x_vel > 0:
                        self.x_vel -= self.x_accel
                    else:
                        self.x_vel = 0
                        self.state = "stand"
                else:
                    if self.x_vel < 0:
                        self.x_vel += self.x_accel
                    else:
                        self.x_vel = 0
                        self.state = "stand"
        else:
            if keys[pg.K_LEFT]:
                self.facing_right = False
                if self.x_vel > 0:
                    self.frame_index = 5
                    self.x_accel = 0.35
                else:
                    self.x_accel = 0.15

                if self.x_vel > (self.max_x_vel * -1):
                    self.x_vel -= self.x_accel
                    if self.x_vel > -0.5:
                        self.x_vel = -0.5
                elif self.x_vel < (self.max_x_vel * -1):
                    self.x_vel += self.x_accel

            elif keys[pg.K_RIGHT]:
                # self.get_out_of_crouch()
                self.facing_right = True
                if self.x_vel < 0:
                    self.frame_index = 5
                    self.x_accel = 0.35
                else:
                    self.x_accel = 0.15

                if self.x_vel < self.max_x_vel:
                    self.x_vel += self.x_accel
                    if self.x_vel < 0.5:
                        self.x_vel = 0.5
                elif self.x_vel > self.max_x_vel:
                    self.x_vel -= self.x_accel

            else:
                if self.facing_right:
                    if self.x_vel > 0:
                        self.x_vel -= self.x_accel
                    else:
                        self.x_vel = 0
                        self.state = "stand"
                else:
                    if self.x_vel < 0:
                        self.x_vel += self.x_accel
                    else:
                        self.x_vel = 0
                        self.state = "stand"
                    
    def calculate_animation_speed(self):
        """Used to make walking animation speed be in relation to
        Mario's x-vel"""
        if self.x_vel == 0:
            animation_speed = 130
        elif self.x_vel > 0:
            animation_speed = 130 - (self.x_vel * (13))
        else:
            animation_speed = 130 - (self.x_vel * (13) * -1)

        return animation_speed

    def update(self, keys, game_info):
        """Updates Mario's states and animations once per frame"""
        self.current_time = game_info["current_time"]
        self.handle_state(keys)
        self.animation()
    
    def animation(self):
        if self.facing_right:
            self.image = self.right_mario_frame[self.frame_index]
        else:
            self.image = self.left_mario_frame[self.frame_index]
    
    def start_death_jump(self, game_info):
        """Used to put Mario in a DEATH_JUMP state"""
        self.dead = True
        game_info["mario_dead"] = True
        self.y_vel = -11
        self.gravity = .5
        self.state = "death_jump"
        self.in_transition_state = True

    def jumping_to_death(self):
        """Called when Mario is in a DEATH_JUMP state"""
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 500:
            self.rect.y += self.y_vel
            self.y_vel += self.gravity

    def handle_state(self, keys):
        """Determines Mario's behavior based on his state"""
        if self.state == "stand":
            self.parado(keys)
        elif self.state == "walk":
            self.walking(keys)
        elif self.state == "jump":
            self.jumping(keys)
        elif self.state == "fall":
            self.falling(keys)
        elif self.state == "death_jump":
            self.jumping_to_death()

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
    keys = pg.key.get_pressed()
    # loop principal
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(mario.image, 
                    (SCREEN_WIDTH/2-mario.image.get_rect().centerx, 
                     SCREEN_HEIGHT - mario.image.get_rect().height - 20))
        game_info = {}
        game_info["current_time"] = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
        mario.update(keys, game_info)
        pg.display.update()
# main()