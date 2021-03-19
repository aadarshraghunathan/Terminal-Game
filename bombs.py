class yeet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xvel = 1

    def move(self, arr1):
        self.x += 1
        if (self.x <= 28 and arr1[self.x + 1][self.y] == '-'):
            
            return True
        return False

    def reset(self, x, y):
        self.x = x
        self.y = y
