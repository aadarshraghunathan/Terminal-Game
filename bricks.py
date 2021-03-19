import time
import powerups
import random

l1 = powerups.powerups


class bricks:  # (x,y) is the bottom left corner of the block and score is the number of hits the block can tolerate
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.height = 1
        self.width = 9
        self.score = score
        self.exist = True
        self.yeet_colour = False

    # def push_to_array(self, x):
    #     for i in range(self.x - self.height + 1, self.x + 1):
    #         for j in range(self.y, self.y + self.width + 2):
    #             x[i][j] = 1

    def hit(self, arr, k, arr1, xvel, yvel, level):
        if (self.score != 100000000):
            self.score = self.score - 1
            self.yeet_colour = True

    def destroy(self, arr, k, arr1, xvel, yvel, level):
        if (self.score > 0):
            self.score = 0
        x = arr[k].x
        y = arr[k].y
        for i in range(x - arr[k].height, x):
            for j in range(y, y + arr[k].width):
                arr1[i][j] = ' '

        if (level != 3):
            id = random.randint(1, 4)
            choice = random.randint(1, 2)
            if (choice == 1):
                p = powerups.Powerups(x, y, id, xvel, yvel)
                powerups.powerup_list.append(p)
        self.exist = False

    def change_score(score):
        pass


class Rainbow_bricks(bricks):
    def __init__(self, x, y, score):
        super().__init__(x, y, score)

    def change_score(self):
        score = self.score
        if (self.yeet_colour == False):
            score = (score + 1) % 3 + 1
            self.score = score


class Exploding_bricks(bricks):
    def __init__(self, x, y, score):
        super().__init__(x, y, score)

    def destroy(self, arr, k, arr1, xvel, yvel, level):
        x = arr[k].x
        y = arr[k].y
        for i in range(x - arr[k].height, x):
            for j in range(y, y + arr[k].width):
                arr1[i][j] = ' '
        self.exist = False

        self.score = 0
        l = len(arr)
        j = 0
        while (j < l):
            if (arr[j].exist == True):

                # #

                # if ((arr[j].y + arr[j].width + 1) == self.y
                #         and (arr[j].x == self.x or (arr[j].x == self.x-1))):
                #     arr[j].destroy(arr, j)
                # elif (arr[j].y == (self.y + self.width)
                #       and ((arr[j].x <= self.x) and
                #            (arr[j].x >= self.x - self.height))):
                #     arr[j].destroy(arr, j)
                # elif (arr[j].x == self.x
                #       and ((arr[j].y >= self.y) and
                #            (arr[j].y <= self.y + self.width))):
                #     arr[j].destroy(arr, j)
                # elif (arr[j].x == (self.x - self.height)
                #       and ((arr[j].y >= self.y) and
                #            (arr[j].y <= self.y + self.width))):
                #     arr[j].destroy(arr, j)

                if ((abs(arr[j].x - self.x) <= self.height)
                        and (abs(arr[j].y - self.y) <= self.width + 1)):
                    arr[j].destroy(arr, j, arr1, xvel, yvel, level)

            j += 1

    def hit(self, arr, k, arr1, xvel, yvel, level):
        self.destroy(arr, k, arr1, xvel, yvel, level)
