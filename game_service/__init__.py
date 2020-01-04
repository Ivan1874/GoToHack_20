global field
from random import randint, choice

field = ['AAAAAAAAAAAAAAAA',
         'BBBBBBBBBBBBBBBB',
         'CCCCCCCCCCCCCCCC',
         'DDDDDDDDDDDDDDDD',
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
    x, y = randint(0, 15), randint(0, 15)
    field[x][y] = choice('ABCD0')
