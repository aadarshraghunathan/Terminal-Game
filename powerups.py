import time
import random
powerups = ["lp"]

powerup_list = []


class Powerups:
    def __init__(self, x, y, id, xvel, yvel):
        self.x = x
        self.y = y
        self.start_time = 0
        self.xvel = -1 * xvel
        self.yvel = yvel
        self.id = id

    def move(self, arr1, paddle_width, mod):
        self.x += self.xvel
        self.y += self.yvel
        if (self.y >= 80):
            self.y = 79
            self.yvel *= -1
        elif (self.y < 0):
            self.y = 0
            self.yvel *= -1
        if (self.x <= 0):
            self.x = 0
            self.xvel *= -1

        # gravity
        p = random.randint(1, 2)

        if (self.xvel <= 0 and p == 1):
            self.xvel += 1
        if (self.id == 1):
            if (self.x <= 28 and arr1[self.x + 1][self.y] == '-'):
                paddle_width += 4
                self.start_time = time.time()
                return paddle_width
        elif (self.id == 2):
            if (self.x <= 28 and arr1[self.x + 1][self.y] == '-'):
                paddle_width -= 4
                self.start_time = time.time()
                return paddle_width
        elif (self.id == 3):
            if (self.x <= 28 and arr1[self.x + 1][self.y] == '-'):
                self.start_time = time.time()
                mod = 1
                return mod

        elif (self.id == 4):

            bullet_seperation_time = -1
            if (self.x <= 28 and arr1[self.x + 1][self.y] == '-'):
                self.start_time = time.time()
                bullet_seperation_time = 3
                has_hit = True
            return bullet_seperation_time

        elif (self.x >= 29):
            self.x = 28
            self.xvel = 0

        if (self.id == 3):
            return mod
        return paddle_width
