global field
from random import randint

field = ['0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000',
         '0000000000000000']
field = [list(x) for x in field]
width = 16
height = 16
bots_position = []


def tick():
    global field
    move = bot_tick(bots_position[0][0], bots_position[0][1], 'A')
    bots_position[0][0] += move[0]
    bots_position[0][1] += move[1]
    field[bots_position[0][1]][bots_position[0][0]] = 'A'


bots_position.append([0, 0])


def get_pixel(x, y):
    return field[y][x]


class Move:
    Left = (-1, 0)
    Right = (1, 0)
    Up = (0, -1)
    Down = (0, 1)


flagX = flagY = False


def bot_tick(x, y, my_color):
    global flagX, flagY
    move = randint(1, 2)
    if move == 1:
        if x > 0 and flagX and (0 <= y <= height - 1):
            x -= 1
            return Move.Left
        elif x < width - 1 and not flagX and (
                0 <= y <= height - 1):
            x += 1
            return Move.Right
    elif move == 2:
        if y > 0 and (0 <= x <= width - 1) and flagY:
            y -= 1
            return Move.Up
        elif y < height - 1 and (0 <= x <= width - 1) and not flagY:
            y += 1
            return Move.Down

    if x == width - 1:
        flagX = True
        return Move.Left
    if x == 0:
        flagX = False
        return Move.Right
    if y == height - 1:
        flagY = True
        return Move.Up
    if y == 0:
        flagY = False
        return Move.Down
