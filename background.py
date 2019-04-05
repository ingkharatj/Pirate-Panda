import arcade
from models import World
import pyglet.gl as gl

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class DotRunWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("pic/image1.png")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dot_sprite = ModelSprite('pic/Panda.png',
                                      model=self.world.dot)

        self.normal_coin = arcade.load_texture('pic/skull-model.jpg')

    def reset(self):
        self.background = arcade.load_texture("pic/image1.png")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dot_sprite = ModelSprite('pic/Panda.png',
                                      model=self.world.dot)


    def update(self, delta):
        self.world.update(delta)
        if self.world.dot.die():
            self.world.freeze()

    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_rectangle_filled(p.x + p.width // 2,
                                         p.y - p.height // 2,
                                         p.width, p.height,
                                         arcade.color.DARK_SCARLET)

    def draw_coins(self, coins):
        for c in coins:
            if not c.is_collected:
                if c.effect == False:
                    arcade.draw_texture_rectangle(c.x, c.y, c.width, c.height,
                                                  self.normal_coin)

    def on_draw(self):
        arcade.set_viewport(self.world.dot.x - SCREEN_WIDTH // 2,
                            self.world.dot.x + SCREEN_WIDTH // 2,
                            0, SCREEN_HEIGHT)

        arcade.start_render()
        arcade.draw_texture_rectangle(self.dot_sprite.center_x, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH + 50, SCREEN_HEIGHT, self.background)
        self.draw_platforms(self.world.platforms)
        self.draw_coins(self.world.coins)
        arcade.draw_text("Space to Start", -100, self.height // 2, arcade.color.GREEN, 30)
        self.dot_sprite.draw()
        arcade.draw_text(str(self.world.score),
                         self.world.dot.x + (SCREEN_WIDTH // 2) - 60,
                         self.height - 30,
                         arcade.color.WHITE, 20)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if not self.world.is_started():
                self.world.start()
            self.world.on_key_press(key, key_modifiers)
        if key == arcade.key.R:
            self.reset()


if __name__ == '__main__':
    window = DotRunWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
