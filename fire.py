import pygame as pg

class Fire(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.setup_fire(x, y)


    def setup_fire(self, x, y):
        """Sets up various values for fire"""
        self.sprite_sheet =  pg.image.load("./resources/graphics/fire_sprite.png")
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0

        self.setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

    def setup_frames(self):
        """Sets frame list"""
        self.frames.append(
            self.get_image(49, 149, 131, 151))
        self.frames.append(
            self.get_image(229, 149, 131, 151))
        self.frames.append(
            self.get_image(409, 149, 131, 151))
        self.frames.append(
            self.get_image(589, 149, 131, 151))


    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))


        image = pg.transform.scale(image,
                                   (int(rect.width*0.4),
                                    int(rect.height*0.4)))
        return image


    def animation(self):
        self.image = self.frames[self.frame_index]


    def update(self, game_info, *args):
        self.current_time = game_info["current_time"]
        if (self.current_time - self.animate_timer) > 125:
            if self.frame_index < 3:
                self.frame_index += 1
            elif self.frame_index == 3:
                self.frame_index = 0
            self.animate_timer = self.current_time
        self.animation()
