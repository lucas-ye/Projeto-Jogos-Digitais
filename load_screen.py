import state
from .. import constants as c
# import game_sound
import info

BLACK = (0, 0, 0)
class LoadScreen(state._State):
    def __init__(self):
        state._State.__init__(self)
        self.current_state = "load_screen"
    def startup(self, current_time, persist):
        self.start_time = current_time
        print(persist)
        self.persist = persist
        self.game_info = self.persist
        self.next = self.set_next_state()

        info_state = self.set_overhead_info_state()

        self.overhead_info = info.OverheadInfo(self.game_info, info_state)
        # self.sound_manager = game_sound.Sound(self.overhead_info)


    def set_next_state(self):
        """Sets the next state"""
        return "level1"

    def set_overhead_info_state(self):
        """sets the state to send to the overhead info object"""
        return "load_screen"


    def update(self, surface, keys, current_time):
        """Updates the loading screen"""
        if (current_time - self.start_time) < 2400:
            surface.fill(BLACK)
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)

        elif (current_time - self.start_time) < 2600:
            surface.fill(BLACK)

        elif (current_time - self.start_time) < 2635:
            surface.fill((106, 150, 252))

        else:
            self.done = True




class GameOver(LoadScreen):
    """A loading screen with Game Over"""
    def __init__(self):
        super().__init__()


    def set_next_state(self):
        """Sets next state"""
        return "main_menu"

    def set_overhead_info_state(self):
        """sets the state to send to the overhead info object"""
        return "game_over"

    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.sound_manager.update(self.persist, None)

        if (self.current_time - self.start_time) < 7000:
            surface.fill()
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)
        elif (self.current_time - self.start_time) < 7200:
            surface.fill(BLACK)
        elif (self.current_time - self.start_time) < 7235:
            surface.fill((106, 150, 252))
        else:
            self.done = True


class TimeOut(LoadScreen):
    """Loading Screen with Time Out"""
    def __init__(self):
        super().__init__()
        print(self.persist)

    def set_next_state(self):
        """Sets next state"""
        if self.persist['lives'] == 0:
            return "game_over"
        else:
            return "load_screen"

    def set_overhead_info_state(self):
        """Sets the state to send to the overhead info object"""
        return "time_out"

    def update(self, surface, keys, current_time):
        self.current_time = current_time

        if (self.current_time - self.start_time) < 2400:
            surface.fill(BLACK)
            self.overhead_info.update(self.game_info)
            self.overhead_info.draw(surface)
        else:
            self.done = True









