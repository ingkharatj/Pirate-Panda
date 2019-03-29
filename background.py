import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


class PandaGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background  = arcade.Sprite('pic/image2.png')
        self.background.set_position(450,300)


    def on_draw(self):
        arcade.start_render()
        self.background.draw()


if __name__ == '__main__':
    window = PandaGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()