import input
import time
from os import system
import bricks
import numpy as np
import random
import colorama
import powerups
from colorama import Back, Fore, Style
import bullet
import boss
import bombs
import sound

ch = 'a'
row = 30
column = 81
game_array = []
game_row = []
score = 0
init_time = time.time()
init_time1 = time.time()
lives = 3
new_level = True
levels = 0
store_score = 0
end = False
bst = -1
health = 6
spawned1 = False
spawned2 = False


def spawn_layer(layer):
    no_of_bricks = 9
    for i in range(no_of_bricks):
        x = layer + 2
        y = i * 9
        random_score = random.randint(1, 3)
        brick = bricks.bricks(x, y, random_score)
        brick_list.append(brick)


def collide_brick(brick_width, brick_height, brick_x, brick_y, x, y, xvel,
                  yvel):
    # top face
    flag = 0
    if ((x == (brick_x - brick_height - 1))
            and ((y >= brick_y - 1) and (y <= (brick_y + brick_width)))
            and (xvel > 0)):
        xvel *= -1
        flag = 1
        sound.play_sound()

    #bottom face
    elif ((x == brick_x) and ((y >= brick_y - 1) and (y <=
                                                      (brick_y + brick_width)))
          and (xvel < 0)):
        xvel *= -1
        flag = 1
        sound.play_sound()

    #left face
    elif ((y == brick_y - 1)
          and ((x >= (brick_x - brick_height - 1)) and (x <= brick_x))
          and (yvel > 0)):
        yvel *= -1
        flag = 1
        sound.play_sound()

    #right face
    elif ((y == (brick_y + brick_width))
          and ((x >= (brick_x - brick_height - 1)) and (x <= brick_x))
          and (yvel < 0)):
        yvel *= -1
        flag = 1
        sound.play_sound()

    l = []
    l.append(xvel)
    l.append(yvel)
    l.append(flag)
    return l


class ball:
    def __init__(self, x, y, xvel, yvel):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.xleft = xvel
        self.yleft = yvel
        self.initx = x
        self.inity = y
        self.initxvel = xvel
        self.inityvel = yvel

    def reset(self):
        self.xleft = self.xvel
        self.yleft = self.yvel

    def big_reset(self, paddle_y):
        self.x = self.initx
        self.y = random.randint(paddle_y - 5, paddle_y + 5)
        self.xvel = self.initxvel
        self.yvel = self.inityvel
        self.xleft = self.xvel
        self.yleft = self.yvel

    def move(self):
        # Right wall

        if (self.xvel != 0):
            xdir = int(self.xvel / abs(self.xvel))

        else:
            xdir = 0
        if (self.yvel != 0):
            ydir = int(self.yvel / abs(self.yvel))
        else:
            ydir = 0

        if ((self.y + ydir) >= 79):
            self.yvel *= -1
            ydir *= -1
            self.reset()

        #left wall
        elif ((self.y + ydir) <= 0):
            self.yvel *= -1
            ydir *= -1
            self.reset()
        #top wall
        if (self.x <= 0):
            self.xvel *= -1
            xdir *= -1
            self.reset()

        elif (self.x >= 29):
            self.xvel *= -1
            xdir *= -1
            self.reset()

        if (self.xleft == 0 and self.yleft == 0):
            self.reset()

        self.x += xdir
        self.xleft -= xdir
        self.y += ydir
        self.yleft -= ydir

    def collide(self, paddle_y):  # paddle_y is the
        # print("yeet")
        if (self.yvel >= 0):
            if self.y == paddle_y:
                self.xvel *= -1
                sound.play_sound2()
            elif self.y < paddle_y:
                displacement = paddle_y - self.y
                self.xvel *= -1
                self.yvel = -int(displacement / 2)
                sound.play_sound2()

            elif self.y > paddle_y:
                displacement = self.y - paddle_y
                self.xvel *= -1
                self.yvel = int(displacement / 2)
                sound.play_sound2()

        elif (self.yvel < 0):
            if self.y == paddle_y:
                self.xvel *= -1
                sound.play_sound2()

            elif self.y > paddle_y:
                displacement = self.y - paddle_y
                self.xvel *= -1
                self.yvel *= -1
                self.yvel = int(displacement / 2)
                sound.play_sound2()

            elif self.y < paddle_y:
                displacement = paddle_y - self.y
                self.xvel *= -1
                self.yvel = -int(displacement / 2)
                sound.play_sound2()

        l = [self.xvel, self.yvel]
        return l


class Paddle:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

    def move(self, ch):
        if (ch == 'd' and self.y + self.width <= 81):
            self.y += 1
        elif (ch == 'a' and self.y > int(self.width / 2)):
            self.y -= 1


for i in range(row):
    game_row = []
    for j in range(column):
        game_row.append(' ')
    game_array.append(game_row)

    paddle = Paddle(28, 35, 8)
    ufo = boss.ufo(2, paddle.y, paddle.width)
    start = random.randint(35, 45)
    gameball = ball(27, 35, -1, 1)

    # brick = bricks.bricks(10, 100, 2, 4, 4)
    # brick1 = bricks.bricks(25, 80, 2, 4, 4)
    def create_final_board():
        brick_list = []
        count = 0
        i = 8
        j = 0
        exp = 0
        while (i < 12):
            count_per_line = 0
            j = 1
            if (count_per_line > 3):
                continue
            while (j + 9 < 75):
                if (count_per_line > 3):
                    break
                random_y = random.randint(j, j + 5)
                j = random_y
                random_score = 100000000
                brick = bricks.bricks(i, random_y, random_score)
                if (random_score == 100000000):
                    count += 1
                brick_list.append(brick)
                count_per_line += 1
                j += 15
            i += 2
        return ([brick_list, count])

    def reset_board():
        brick_list = []
        w, h = 31, 201
        brick_positions = [[0 for x in range(h)] for y in range(w)]
        count = 0
        i = 2
        j = 0
        exp = 0
        while (i < 20):
            count_per_line = 0
            j = 1
            if (count_per_line > 6):
                continue
            while (j + 9 < 75):
                random_y = random.randint(j, j + 5)
                j = random_y
                random_score = random.randint(1, 4)
                if (random_score == 4):
                    random_c = random.randint(1, 3)
                    if (random_c == 3):
                        random_score = 100000000
                    else:
                        random_score = random.randint(1, 3)
                choice = random.randint(0, 3)
                if (random_y + 48 > 79 and choice == 2):
                    choice = 1
                if (choice == 1):
                    pick = random.randint(0, 4)
                    if (pick <= 3):
                        brick = bricks.bricks(i, random_y, random_score)
                        if (random_score == 100000000):
                            count += 1
                        brick_list.append(brick)
                        count_per_line += 1
                        j += 9
                    else:
                        brick = bricks.Rainbow_bricks(i, random_y,
                                                      random_score)
                        brick_list.append(brick)
                        count_per_line += 1
                        j += 9
                elif (choice == 2 and exp < 1 and i > 10):
                    for k in range(6):
                        brick = bricks.Exploding_bricks(i, j, -1)
                        brick_list.append(brick)
                        j += 9
                        exp += 1
                        count_per_line += 6

            i += 2

        for brick in brick_list:
            for t in range(brick.x - brick.height, brick.x):
                for p in range(brick.y, brick.y + brick.width):
                    brick_positions[t][p] = "b"

        return ([brick_list, count])

    bullet1 = bullet.bullet(paddle.x - 1, paddle.y)
    bomb = bombs.yeet(ufo.x + 1, ufo.y)

system("stty -echo")  #reset
ticks = 0
mod = 3
started = False
while (True):
    if (new_level == True):
        levels += 1
        if (levels != 3):
            l = reset_board()
            brick_list = l[0]
            num_unb = l[1]
        elif (levels == 3):
            l = create_final_board()
            brick_list = l[0]
            num_unb = l[1]
            time.sleep(1)
        elif (levels == 5):
            break

        new_level = False
        started = False
        gameball.big_reset(paddle.y)

    if (started == False):
        for q in powerups.powerup_list:
            if (q.id == 1):
                paddle.width -= 4
            elif (q.id == 2):
                paddle.width += 4
            elif (q.id == 3):
                mod = 3
            elif (q.id == 4):
                bst = -1
            powerups.powerup_list.remove(q)

    for q in powerups.powerup_list:
        if (q.start_time != 0):
            if (time.time() - q.start_time > 8):
                if (q.id == 1):
                    paddle.width -= 4
                elif (q.id == 2):
                    paddle.width += 4
                elif (q.id == 3):
                    mod = 3
                elif (q.id == 4):
                    bst = -1
                powerups.powerup_list.remove(q)
    if (gameball.x >= 29):
        lives -= 1
        init_time1 = time.time()
        if (lives == 0):
            break
        gameball.big_reset(paddle.y)
        started = False
    t = time.time()
    for i in range(row):
        for j in range(column):
            if (j == 80):
                game_array[i][j] = '|'
            else:
                game_array[i][j] = ' '

    game_array[gameball.x][gameball.y] = 'o'
    if (bst != -1):
        game_array[bullet1.x][bullet1.y] = '*'
    for i in range(column):
        if (i >= (paddle.y -
                  (int(paddle.width) / 2))) and (i <=
                                                 (paddle.y +
                                                  (int(paddle.width / 2)))):
            game_array[paddle.x][i] = '-'
        else:
            game_array[paddle.x][i] = ' '

    if (levels == 3):
        for i in range(column):
            if (i >=
                (paddle.y -
                 (int(paddle.width) / 2))) and (i <=
                                                (paddle.y +
                                                 (int(paddle.width / 2)))):
                game_array[ufo.x][i] = 'u'
            else:
                game_array[ufo.x][i] = ' '

        if (started == False):
            bomb.x = ufo.x + 1
            bomb.y = paddle.y

        game_array[bomb.x][bomb.y] = 'b'

        if (started == True and ticks % 3 == 0):
            if (bomb.move(game_array)):
                lives -= 1
                init_time1 = time.time()
                if (lives == 0):
                    break
                gameball.big_reset(paddle.y)
                started = False
                bomb.reset(ufo.x + 1, ufo.y)
            elif (bomb.x >= 29):
                bomb.reset(ufo.x + 1, ufo.y)

            arr = ufo.collide_ball(gameball.x, gameball.y)
            health = arr[0]
            if (arr[1]):
                gameball.xvel *= -1
            if (health == 4 and spawned1 == False):
                spawn_layer(3)
                spawned1 = True
            if (health == 2 and spawned2 == False):
                spawn_layer(4)
                spawned2 = True
            if (health == 0):
                break

    for brick in brick_list:
        for i in range(brick.x - brick.height, brick.x):
            for j in range(brick.y, brick.y + brick.width):

                if (brick.exist == True):
                    game_array[i][j] = brick.score

# collision with paddle

    if ((gameball.x == paddle.x)
            and (abs(gameball.y - paddle.y) <= int(paddle.width / 2))):
        vel_list = gameball.collide(paddle.y)
        gameball.xvel = vel_list[0]
        gameball.yvel = vel_list[1]
        for brick in brick_list:
            bottom_flag = False
            if (t - init_time1 >= 500):
                brick.x += 1
                bottom_flag = False
                if (brick.x == 29):
                    bottom_flag = True
                    break

        if (bottom_flag == True):
            break

#collision with brick
#brick_width,brick_height,brick_x,brick_y,x,y,xvel,yvel
    if (ticks % mod == 0):
        for k in range(len(brick_list)):

            box = brick_list[k]
            if (box.exist == True):
                list1 = collide_brick(box.width, box.height, box.x, box.y,
                                      gameball.x, gameball.y, gameball.xvel,
                                      gameball.yvel)
                gameball.xvel = list1[0]
                # print(gameball.xvel)
                gameball.yvel = list1[1]

                if (list1[2] == 1):
                    box.hit(brick_list, k, game_array, gameball.xvel,
                            gameball.yvel, levels)
                    if (box.score == 0):
                        box.destroy(brick_list, k, game_array, gameball.xvel,
                                    gameball.yvel, levels)
                    # break
                    continue

        #bullet collide with bricks
    if (ticks % 3 == 0):
        for k in range(len(brick_list)):

            box = brick_list[k]
            if (box.exist == True):
                truth = bullet1.collide_brick(box.y, box.x, box.width,
                                              box.height)
            if (truth):
                box.hit(brick_list, k, game_array, bullet1.xvel, 0, levels)
                bst = -1
                bullet1.x = paddle.x
                if (box.score == 0):
                    box.destroy(brick_list, k, game_array, bullet1.xvel, 0,
                                levels)
                # break
                continue

    for i in powerups.powerup_list:
        if (i.x < 28 and i.id == 1):
            game_array[i.x][i.y] = 'p'
        elif (i.x < 28 and i.id == 2):
            game_array[i.x][i.y] = 's'
        elif (i.x < 28 and i.id == 3):
            game_array[i.x][i.y] = 'f'
        elif (i.x < 28 and i.id == 4):
            game_array[i.x][i.y] = 't'

    for i in range(row):
        for j in range(column):
            if (game_array[i][j] == 3):
                print(Fore.RED + Back.RED, end="")
                print(' ', end="")
                print(Style.RESET_ALL, end="")
            elif (game_array[i][j] == 2):
                print(Fore.YELLOW + Back.YELLOW, end="")
                print(' ', end="")
                print(Style.RESET_ALL, end="")
            elif (game_array[i][j] == 1):
                print(Fore.GREEN + Back.GREEN, end="")
                print(' ', end="")
                print(Style.RESET_ALL, end="")
            elif (game_array[i][j] == 100000000):
                print(Fore.BLUE + Back.BLUE, end="")
                print(' ', end="")
                print(Style.RESET_ALL, end="")
            elif (game_array[i][j] == -1):
                print(Fore.WHITE + Back.WHITE, end="")
                print(' ', end="")
                print(Style.RESET_ALL, end="")
            else:
                print(game_array[i][j], end="")
        print("")

    ch = input.input_to()
    if (ch == 'l'):
        new_level = True
        store_score = score
    if (ch != None):
        time.sleep(0.05)
    if (ticks % 3 == 0):
        if (started == True):
            gameball.move()
            if (bst != -1):
                bullet1.move()
            for i in powerups.powerup_list:
                if (i.id < 3):
                    paddle.width = i.move(game_array, paddle.width, mod)
                elif (i.id == 3):
                    mod = i.move(game_array, paddle.width, mod)
                elif (i.id == 4):
                    temp = -1
                    if (bst != -1):
                        temp = bst

                    bst = i.move(game_array, paddle.width, mod)
                    if (bst != -1):

                        bullet1.x = paddle.x
                        bullet1.y = paddle.y
                    if (bullet1.x == 0):
                        bst = -1
                    elif (bst == -1):
                        bst = temp
    if (started == True):
        paddle.move(ch)
        ufo.move(paddle.y)
    if ch == 'x':
        break
    ticks += 1
    cnt = 0
    for i in brick_list:
        if (not i.exist):
            cnt += 1
    score = cnt + store_score

    if (cnt == (len(brick_list) - num_unb) and (levels != 3)):
        new_level = True
        store_score = score
    for i in brick_list:
        i.change_score()

    t = round(t - init_time)
    print("score = ", score)
    print("time = ", t)
    print("lives = ", lives)
    print('\033[0;0H')
    if (levels == 3):
        print("Boss health = ", health)
    if (started == False):
        dist = paddle.y - gameball.y
        ch = input.input_to()
        if (ch == 'w'):
            started = True
            continue
        paddle.move(ch)
        gameball.y = paddle.y - dist
        continue

system("stty echo")
