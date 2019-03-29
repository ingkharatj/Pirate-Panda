import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


class PandaGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background  = arcade.Sprite('pic/image2.png')
        self.background.set_position(450,300)
        self.panda = arcade.Sprite('pic/Panda.png')
        self.panda.set_position(200,200)


    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.panda.draw()

    def update(self, delta):
        self.panda.set_position(self.panda.center_x + 3, self.panda.center_y )


if __name__ == '__main__':
    window = PandaGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()