import arcade.key
from random import randint, random
import time

GRAVITY = -1
MAX_VX = 10
ACCX = 0.5
JUMP_VY = 15

PANDA_RADIUS = 50
PLATFORM_MARGIN = 15

COIN_RADIUS = 35
COIN_Y_OFFSET = 20
COIN_MARGIN = 12
COIN_HIT_MARGIN = 23

SKULL_RADIUS = 36
SKULL_Y_OFFSET = 22
SKULL_MARGIN = 15
SKULL_HIT_MARGIN = 15


class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0


class Panda(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
        self.is_jump = False
        self.platform = None
        self.super = False
        self.timer = 0

    def start_super(self):
        self.super = True
        self.timer = time

    def end_super(self):
        self.timer = 0
        self.super = False

    def check_super_time(self):
        if self.super == True:
            if time.time() - self.timer > 3.5:
                self.end_super()
                return
        return

    def jump(self):
        if not self.platform:
            return

        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def update(self, delta):
        if self.vx < MAX_VX:
            self.vx += ACCX

        self.x += self.vx

        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0

    def top_y(self):
        return self.y + (PANDA_RADIUS // 2)

    def bottom_y(self):
        return self.y - (PANDA_RADIUS // 2)

    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + (PANDA_RADIUS // 2)

    def is_on_platform(self, platform, margin=PLATFORM_MARGIN):
        if not platform.in_top_range(self.x):
            return False

        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False

        if self.bottom_y() - self.vy > platform.y > self.bottom_y():
            return True

        return False

    def find_touching_platform(self):
        platforms = self.world.platforms
        for p in platforms:
            if self.is_falling_on_platform(p):
                return p
        return None

    def die(self):
        if self.top_y() < 0:
            return True
        return False

class Skull:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_collected = False
        if random() > 1.5:
            self.effect = True

    def skull_hit(self,panda):
        panda.die()
        return ((abs(self.x - panda.x) < SKULL_HIT_MARGIN) and
                (abs(self.y - panda.y) < SKULL_HIT_MARGIN))



class Coin:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_collected = False
        self.effect = False
        if random() > 0.975:
            self.effect = True

    def coin_hit(self, panda):
        return ((abs(self.x - panda.x) < COIN_HIT_MARGIN) and
                (abs(self.y - panda.y) < COIN_HIT_MARGIN))



class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_top_range(self, x):
        return self.x <= x <= self.x + self.width

    def right_most_x(self):
        return self.x + self.width

    def spawn_coins(self):
        coins = []
        x = self.x + COIN_MARGIN

        while x + COIN_MARGIN <= self.right_most_x():
            coins.append(Coin(x+300 , self.y + COIN_Y_OFFSET +15 , COIN_RADIUS+20 , COIN_RADIUS+20))
            x += COIN_MARGIN + COIN_RADIUS + 200

            # coins.append(Coin(x, self.y + COIN_Y_OFFSET + 60, COIN_RADIUS + 20, COIN_RADIUS + 20))
            # x += COIN_MARGIN + COIN_RADIUS + 1234

        return coins

    def spawn_skull(self):
        skulls = []
        x = self.x + SKULL_MARGIN
        while x + SKULL_MARGIN <= self.right_most_x():
            skulls.append(Coin(x, self.y + SKULL_Y_OFFSET, SKULL_RADIUS, SKULL_RADIUS))
            x += SKULL_MARGIN + SKULL_RADIUS
        return skulls



class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.panda = Panda(self, 0, 120)
        self.init_platforms()

        self.panda.set_platform(self.platforms[0])

        self.score = 0

        self.state = World.STATE_FROZEN

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_started(self):
        return self.state == World.STATE_STARTED

    def init_platforms(self):
        self.platforms = [
            Platform(self, 0, 100, 500, 60),
            Platform(self, 600, 150, 500, 30),
            Platform(self, 1200, 200, 500, 40),
            Platform(self, 1800, 150, 300, 35),
            Platform(self, 2200, 100, 400, 50),
            Platform(self, 2500, 150, 350, 45),
            Platform(self, 2950, 200, 200, 55),
            Platform(self, 3200, 150, 420, 40 ),
            Platform(self, 3850, 100, 500, 35 ),
            Platform(self, 4200, 150, 300, 40)

        ]
        self.coins = []

        for p in self.platforms:

            self.coins += p.spawn_coins()


        self.skulls = []
        # for i in self.platforms:
        #     self.skulls += i.spawn_skull()

    def update(self, delta):
        if self.state == World.STATE_FROZEN:
            return
        self.panda.update(delta)
        self.recycle_platform()
        self.collect_coins()
        self.remove_old_coins()
        self.score_plus()


    def score_plus(self):
        self.score += 1

    def collect_coins(self):
        for c in self.coins:
            if (not c.is_collected) and (c.coin_hit(self.panda)):
                c.is_collected = True
                if c.effect == False:
                    self.score += 100

    def too_far_left_x(self):
        return self.panda.x - self.width

    def remove_old_coins(self):
        far_x = self.too_far_left_x()
        if self.coins[0].x >= far_x:
            return
        self.coins = [c for c in self.coins if c.x >= far_x]


    def recycle_platform(self):
        far_x = self.too_far_left_x()
        for p in self.platforms:
            if p.right_most_x() < far_x:
                last_x = max([pp.right_most_x() for pp in self.platforms])
                p.x = last_x + randint(50, 200)
                p.y = randint(100, 200)
                self.coins += p.spawn_coins()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.panda.jump()

