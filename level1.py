import pygame as pg
import state, info
# import game_sound
import mario
import collider
import main


class Level1(state._State):
    def __init__(self):
        super().__init__()
        self.current_state = "level1"

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.game_info = persist
        self.persist = self.game_info
        self.game_info["current_time"] = current_time
        self.game_info["level_state"] = "not_frozen"
        self.game_info["mario_dead"] = False

        self.state = "not_frozen"
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0

        self.moving_score_list = []
        self.overhead_info_display = info.OverheadInfo(self.game_info, "level")
        # self.sound_manager = game_sound.Sound(self.overhead_info_display)

        self.setup_background()
        self.setup_ground()
        self.setup_mario()
        self.setup_spritegroups()

    def setup_background(self):
        """Sets the background image, rect and scales it to the correct
        proportions"""
        self.background = pg.image.load("./resources/graphics/level_1.png")
        self.back_rect = self.background.get_rect()
        self.background = pg.transform.scale(self.background,
                                  (int(self.back_rect.width*2.679),
                                  int(self.back_rect.height*2.679)))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = main.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.game_info["camera_start"]

    def setup_ground(self):
        """Creates collideable, invisible rectangles over top of the ground for
        sprites to walk on"""
        ground_rect1 = collider.Collider(0, 538, self.back_rect.height, 60)

        self.ground_group = pg.sprite.Group(ground_rect1)


    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario()
        self.mario.rect.x = self.viewport.x + 110
        self.mario.rect.bottom = 538

    def setup_spritegroups(self):
        """Sprite groups created for convenience"""

        self.ground_step_pipe_group = pg.sprite.Group(self.ground_group)
        self.mario_and_enemy_group = pg.sprite.Group(self.mario)

    def update(self, surface, keys, current_time):
        """Updates Entire level using states.  Called by the control object"""
        self.game_info["current_time"] = self.current_time = current_time
        self.handle_states(keys)
        self.check_if_time_out()
        self.blit_everything(surface)
        # self.sound_manager.update(self.game_info, self.mario)



    def handle_states(self, keys):
        """If the level is in a FROZEN state, only mario will update"""
        if self.state == "frozen":
            self.update_during_transition_state(keys)
        elif self.state == "not_frozen":
            self.update_all_sprites(keys)
        elif self.state == c.FLAG_AND_FIREWORKS:
            self.update_flag_and_fireworks()


    def update_during_transition_state(self, keys):
        """Updates mario in a transition state (like becoming big, small,
         or dies). Checks if he leaves the transition state or dies to
         change the level state back"""
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.check_for_mario_death()
        self.overhead_info_display.update(self.game_info, self.mario)


    def update_all_sprites(self, keys):
        """Updates the location of all sprites on the screen."""
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.adjust_sprite_positions()
        self.check_for_mario_death()
        self.update_viewport()
        self.overhead_info_display.update(self.game_info, self.mario)


    def adjust_sprite_positions(self):
        """Adjusts sprites by their x and y velocities and collisions"""
        self.adjust_mario_position()

    def adjust_mario_position(self):
        """Adjusts Mario's position based on his x, y velocities and
        potential collisions"""
        self.last_x_position = self.mario.rect.right
        self.mario.rect.x += round(self.mario.x_vel)
        self.check_mario_x_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = (self.viewport.x + 5)


    def check_mario_x_collisions(self):
        """Check for collisions after Mario is moved on the x axis"""
        collider = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)


        if collider:
            self.adjust_mario_for_x_collisions(collider)


    def adjust_mario_for_x_collisions(self, collider):
        """Puts Mario flush next to the collider after moving on the x axis"""
        if self.mario.rect.x < collider.rect.x:
            self.mario.rect.right = collider.rect.left
        else:
            self.mario.rect.left = collider.rect.right

        self.mario.x_vel = 0


    def check_mario_y_collisions(self):
        """Checks for collisions when Mario moves along the y-axis"""
        ground_step_or_pipe = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)

        if ground_step_or_pipe:
            self.adjust_mario_for_y_ground_pipe_collisions(ground_step_or_pipe)

        self.test_if_mario_is_falling()


    def prevent_collision_conflict(self, obstacle1, obstacle2):
        """Allows collisions only for the item closest to marios centerx"""
        if obstacle1 and obstacle2:
            obstacle1_distance = self.mario.rect.centerx - obstacle1.rect.centerx
            if obstacle1_distance < 0:
                obstacle1_distance *= -1
            obstacle2_distance = self.mario.rect.centerx - obstacle2.rect.centerx
            if obstacle2_distance < 0:
                obstacle2_distance *= -1

            if obstacle1_distance < obstacle2_distance:
                obstacle2 = False
            else:
                obstacle1 = False

        return obstacle1, obstacle2


    def adjust_mario_for_y_ground_pipe_collisions(self, collider):
        """Mario collisions with pipes on the y-axis"""
        if collider.rect.bottom > self.mario.rect.bottom:
            self.mario.y_vel = 0
            self.mario.rect.bottom = collider.rect.top
            if self.mario.state == c.END_OF_LEVEL_FALL:
                self.mario.state = c.WALKING_TO_CASTLE
            else:
                self.mario.state = c.WALK
        elif collider.rect.top < self.mario.rect.top:
            self.mario.y_vel = 7
            self.mario.rect.top = collider.rect.bottom
            self.mario.state = c.FALL


    def test_if_mario_is_falling(self):
        """Changes Mario to a FALL state if more than a pixel above a pipe,
        ground, step or box"""
        self.mario.rect.y += 1
        test_collide_group = pg.sprite.Group(self.ground_step_pipe_group,
                                                 self.brick_group)


        if pg.sprite.spritecollideany(self.mario, test_collide_group) is None:
            if self.mario.state != c.JUMP \
                and self.mario.state != c.DEATH_JUMP \
                and self.mario.state != c.SMALL_TO_BIG \
                and self.mario.state != c.BIG_TO_FIRE \
                and self.mario.state != c.BIG_TO_SMALL \
                and self.mario.state != c.FLAGPOLE \
                and self.mario.state != c.WALKING_TO_CASTLE \
                and self.mario.state != c.END_OF_LEVEL_FALL:
                self.mario.state = c.FALL
            elif self.mario.state == c.WALKING_TO_CASTLE or \
                self.mario.state == c.END_OF_LEVEL_FALL:
                self.mario.state = c.END_OF_LEVEL_FALL

        self.mario.rect.y -= 1


    def check_if_falling(self, sprite, sprite_group):
        """Checks if sprite should enter a falling state"""
        sprite.rect.y += 1

        if pg.sprite.spritecollideany(sprite, sprite_group) is None:
            if sprite.state != c.JUMP:
                sprite.state = c.FALL

        sprite.rect.y -= 1


    def check_to_add_flag_score(self):
        """Adds flag score if at top"""
        if self.flag_score.y_vel == 0:
            self.game_info["score"] += self.flag_score_total
            self.flag_score_total = 0


    def check_for_mario_death(self):
        """Restarts the level if Mario is dead"""
        if self.mario.rect.y > main.SCREEN_HEIGHT and not self.mario.in_castle:
            self.mario.dead = True
            self.mario.x_vel = 0
            self.state = 'frozen'
            self.game_info["mario_dead"] = True

        if self.mario.dead:
            self.play_death_song()


    def play_death_song(self):
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 3000:
            self.set_game_info_values()
            self.done = True


    def set_game_info_values(self):
        """sets the new game values after a player's death"""
        if self.game_info["score"] > self.persist["top_score"]:
            self.persist["top_score"] = self.game_info["score"]
        if self.mario.dead:
            self.persist["lives"] -= 1

        if self.persist["lives"] == 0:
            self.next = "game_over"
            self.game_info["camera_start"] = 0
        elif self.mario.dead == False:
            self.next = "main_menu"
            self.game_info["camera_start"] = 0
        elif self.overhead_info_display.time == 0:
            self.next = "time_out"
        else:
            if self.mario.rect.x > 3670 \
                    and self.game_info["camera_start"] == 0:
                self.game_info["camera_start"] = 3440
            self.next = "load_screen"


    def check_if_time_out(self):
        """Check if time has run down to 0"""
        if self.overhead_info_display.time <= 0 \
                and not self.mario.dead \
                and not self.mario.in_castle:
            self.state = "frozen"
            self.mario.start_death_jump(self.game_info)


    def update_viewport(self):
        """Changes the view of the camera"""
        third = self.viewport.x + self.viewport.w//3
        mario_center = self.mario.rect.centerx
        mario_right = self.mario.rect.right

        if self.mario.x_vel > 0 and mario_center >= third:
            mult = 0.5 if mario_right < self.viewport.centerx else 1
            new = self.viewport.x + mult * self.mario.x_vel
            highest = self.level_rect.w - self.viewport.w
            self.viewport.x = min(highest, new)


    def update_flag_and_fireworks(self):
        """Updates the level for the fireworks and castle flag"""
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.game_info)
        self.overhead_info_display.update(self.game_info)

        self.end_game()


    def end_game(self):
        """End the game"""
        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_game_info_values()
            self.next = "game_over"
            # self.sound_manager.stop_music()
            self.done = True


    def blit_everything(self, surface):
        """Blit all sprites to the main surface"""
        self.level.blit(self.background, self.viewport, self.viewport)
        if self.flag_score:
            self.flag_score.draw(self.level)
        #self.check_point_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)
        surface.blit(self.level, (0,0), self.viewport)
        self.overhead_info_display.draw(surface)
        for score in self.moving_score_list:
            score.draw(surface)