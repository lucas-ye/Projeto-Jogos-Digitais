import pygame as pg
import state, info
import sound
import mario
import collider
import main
import fire


class Level3(state._State):
    def __init__(self):
        super().__init__()
        self.current_state = "level3"

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.game_info = persist
        self.persist = self.game_info
        self.game_info["current_time"] = current_time
        self.game_info["level_state"] = "not_frozen"
        self.game_info["mario_dead"] = False
        self.game_info["level"] = 3
        self.state = "not_frozen"
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0
        self.overhead_info_display = info.OverheadInfo(self.game_info, "level3")
        if self.game_info["sound"]:
            self.sound_manager = sound.Sound(self.overhead_info_display)
        else:
            self.sound_manager = None

        self.setup_background()
        self.setup_ground()
        self.setup_mario()
        self.setup_fire()
        self.setup_spritegroups()
        self.setup_finishpoint()

    def setup_fire(self):
        # 52 x 60
        fire1 = fire.Fire(500, 538)
        fire2 = fire.Fire(800, 538)
        fire3 = fire.Fire(800, 478)
        fire4 = fire.Fire(1500, 538)
        fire5 = fire.Fire(1500, 458)
        fire6 = fire.Fire(2400, 538)
        fire7 = fire.Fire(2400, 250)
        fire8 = fire.Fire(3400, 538)
        fire9 = fire.Fire(3400, 270)
        fire10 = fire.Fire(4500, 538)
        fire11 = fire.Fire(4500, 300)
        fire12 = fire.Fire(5700, 538)
        fire13 = fire.Fire(5700, 310)
        fire14 = fire.Fire(6900, 538)
        fire15 = fire.Fire(6952, 538)
        fire16 = fire.Fire(8000, 538)
        fire17 = fire.Fire(8052, 538)
        fire18 = fire.Fire(8104, 538)
        fire19 = fire.Fire(8052, 478)
        self.fire_group1 = pg.sprite.Group(fire1, fire2, fire3, fire4, fire5, fire6, fire7, fire8, fire9, fire10, fire11, fire12, fire13, fire14, fire15, fire16, fire17, fire18, fire19)

        # self.fire_group_list = [fire_group1]

    def setup_finishpoint(self):
        self.finishpoint = pg.sprite.Group(collider.Collider(8787, 0, 10, self.back_rect.height))
        
    def setup_background(self):
        """Sets the background image, rect and scales it to the correct
        proportions"""
        self.background = pg.image.load("./resources/graphics/level_3.png")
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
        ground_rect1 = collider.Collider(0, 538, self.back_rect.width, 60)
        ground_rect2 = collider.Collider(self.back_rect.width, 0, 10, self.back_rect.height)
        ground_rect3 = collider.Collider(0, 0, 10, self.back_rect.height)

        self.ground_group = pg.sprite.Group(ground_rect1, ground_rect2, ground_rect3)


    def setup_mario(self):
        """Places Mario at the beginning of the level"""
        self.mario = mario.Mario(3)
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
        if self.sound_manager:
            self.sound_manager.update(self.game_info, self.mario)


    def handle_states(self, keys):
        """If the level is in a FROZEN state, only mario will update"""
        if self.state == "frozen":
            self.update_during_transition_state(keys)
        elif self.state == "not_frozen":
            self.update_all_sprites(keys)
        elif self.state == "flag_and_fireworks":
            self.update_flag_and_fireworks()


    def update_during_transition_state(self, keys):
        """Updates mario in a transition state (like becoming big, small,
         or dies). Checks if he leaves the transition state or dies to
         change the level state back"""
        self.fire_group1.update(self.game_info)
        self.mario.update(keys, self.game_info)
        if self.flag_score:
            self.flag_score.update(None, self.game_info)
            self.check_to_add_flag_score()
        self.check_for_mario_death()
        self.overhead_info_display.update(self.game_info, self.mario)


    def update_all_sprites(self, keys):
        """Updates the location of all sprites on the screen."""
        self.fire_group1.update(self.game_info)
        self.mario.update(keys, self.game_info)
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

        if self.mario.in_transition_state == False:
            self.mario.rect.y += round(self.mario.y_vel)
            self.check_mario_y_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = (self.viewport.x + 5)


    def check_mario_x_collisions(self):
        """Check for collisions after Mario is moved on the x axis"""
        collider = pg.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        fire = pg.sprite.spritecollideany(self.mario, self.fire_group1)
        finish = pg.sprite.spritecollideany(self.mario, self.finishpoint)

        if collider:
            self.adjust_mario_for_x_collisions(collider)
        elif fire:
            self.mario.start_death_jump(self.game_info)
            self.state = "frozen"
        elif finish:
            self.state = "flag_and_fireworks"

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
            self.mario.state = "walk"
        elif collider.rect.top < self.mario.rect.top:
            self.mario.y_vel = 7
            self.mario.rect.top = collider.rect.bottom
            self.mario.state = "fall"


    def test_if_mario_is_falling(self):
        """Changes Mario to a FALL state if more than a pixel above a pipe,
        ground, step or box"""
        self.mario.rect.y += 1
        test_collide_group = pg.sprite.Group(self.ground_step_pipe_group)


        if pg.sprite.spritecollideany(self.mario, test_collide_group) is None:
            if self.mario.state != "jump":
                self.mario.state = 'fall'

        self.mario.rect.y -= 1


    def check_to_add_flag_score(self):
        """Adds flag score if at top"""
        if self.flag_score.y_vel == 0:
            self.game_info["score"] += self.flag_score_total
            self.flag_score_total = 0


    def check_for_mario_death(self):
        """Restarts the level if Mario is dead"""
        if self.mario.rect.y > main.SCREEN_HEIGHT:
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
                and not self.mario.dead:
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
        self.overhead_info_display.update(self.game_info, self.mario)

        self.end_game()


    def end_game(self):
        """End the game"""
        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_game_info_values()
            self.next = "game_over"
            if self.sound_manager:
                self.sound_manager.stop_music()
            self.done = True


    def blit_everything(self, surface):
        """Blit all sprites to the main surface"""
        self.level.blit(self.background, self.viewport, self.viewport)
        if self.flag_score:
            self.flag_score.draw(self.level)
        #self.check_point_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)
        self.fire_group1.draw(self.level)
        surface.blit(self.level, (0,0), self.viewport)
        self.overhead_info_display.draw(surface)
