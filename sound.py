import pygame as pg
import os

class Sound(object):
    """Handles all sound for the game"""
    def load_all_music(self):
        songs = {}
        for song in os.listdir("resources/music"):
            name = os.path.splitext(song)[0]
            songs[name] = os.path.join("resources/music", song)
        return songs

    def load_all_sfx(self):
        effects = {}
        for fx in os.listdir("resources/sound"):
            name= os.path.splitext(fx)[0]
            effects[name] = pg.mixer.Sound(os.path.join("resources/sound", fx))
        return effects

    def __init__(self, overhead_info):
        """Initialize the class"""
        self.sfx_dict = self.load_all_sfx()
        self.music_dict = self.load_all_music()
        self.overhead_info = overhead_info
        self.game_info = overhead_info.game_info
        self.set_music_mixer()



    def set_music_mixer(self):
        """Sets music for level"""
        if self.overhead_info.state == "level":
            pg.mixer.music.load(self.music_dict['main_theme'])
            pg.mixer.music.play()
            self.state = "normal"
        elif self.overhead_info.state == "game_over":
            pg.mixer.music.load(self.music_dict['game_over'])
            pg.mixer.music.play()
            self.state = "game_over"


    def update(self, game_info, mario):
        """Updates sound object with game info"""
        self.game_info = game_info
        self.mario = mario
        self.handle_state()

    def  handle_state(self):
        """Handles the state of the soundn object"""
        if self.state == "normal":
            if self.mario.dead:
                self.play_music('death', "mario_dead")
            elif self.overhead_info.time == 100:
                self.play_music('out_of_time', "time_warning")


        elif self.state == "time_warning":
            if pg.mixer.music.get_busy() == 0:
                self.play_music('main_theme_sped_up', "sped_up_normal")
            elif self.mario.dead:
                self.play_music('death', "mario_dead")

        elif self.state == "sped_up_normal":
            if self.mario.dead:
                self.play_music('death', "mario_dead")

        elif self.state == "world_clear":
            pass
        elif self.state == "mario_dead":
            pass
        elif self.state == "game_over":
            pass

    def play_music(self, key, state):
        """Plays new music"""
        pg.mixer.music.load(self.music_dict[key])
        pg.mixer.music.play()
        self.state = state

    def stop_music(self):
        """Stops playback"""
        pg.mixer.music.stop()



