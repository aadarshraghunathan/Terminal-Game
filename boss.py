class ufo:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.height = 1
        self.width = width
        self.health = 6

    def move(self, paddle_y):
        self.y = paddle_y

    # def collide_brick(self, y, x, width, height):
    #     if (self.y >= y and self.y <= (y + width)
    #             and (self.x <= x and self.x >= x - height)):
    #         return True

    def collide_ball(self, x, y):
        if_hit = False

        if ((x == (self.x - self.height - 1))
                and ((y >= self.y - 1) and (y <= (self.y + self.width)))):
            self.health -= 1
            if_hit = True
        elif ((x == self.x)
              and ((y >= self.y - 1) and (y <= (self.y + self.width)))):
            self.health -= 1
            if_hit = True

        return [self.health, if_hit]
