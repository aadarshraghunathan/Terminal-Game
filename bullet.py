class bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xvel = 1
        self.exist = True

    def move(self):
        if (self.x >= 1):
            self.x -= self.xvel


    def collide_brick(self, y, x, width, height):
        if (self.y >= y and self.y <= (y + width)
                and (self.x <= x and self.x >= x - height)):
            return True
