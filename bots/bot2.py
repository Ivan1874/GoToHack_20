from random import randint

poligon = [['.'] * 10 for i in range(10)]

my_color = '*'

coord_x = coord_y = 0;
flagX = flagY = False


def Tick(coord_x, coord_y):
    return move(randint(1, 2))


def move(x):
    global poligon, coord_x, coord_y, flagX, flagY, my_color
    if x == 1:
        if coord_x > 0 and get_pixel(coord_x - 1, coord_y) != my_color and flagX and (0 <= coord_y <= len(poligon) - 1):
            coord_x -= 1
            return 'move_left()'
        elif coord_x < len(poligon[coord_y]) - 1 and get_pixel(coord_x + 1, coord_y) != my_color and not flagX and (
                0 <= coord_y <= len(poligon) - 1):
            coord_x += 1
            return 'move_right()'
    elif x == 2:
        if coord_y > 0 and get_pixel(coord_x, coord_y - 1) != my_color and (
                0 <= coord_x <= len(poligon[coord_y]) - 1) and flagY:
            coord_y -= 1
            return 'move_up()'
        elif coord_y < len(poligon) - 1 and get_pixel(coord_x, coord_y + 1) != my_color and (
                0 <= coord_x <= len(poligon[coord_y]) - 1) and not flagY:
            coord_y += 1
            return 'move_down()'

    if coord_x == len(poligon[coord_y]) - 1:
        flagX = True
    if coord_x == 0:
        flagX = False
    if coord_y == len(poligon) - 1:
        flagY = True
    if coord_y == 0:
        flagY = False


def get_pixel(coord_x, coord_y):
    global poligon
    return poligon[coord_y][coord_x]


i = 0
while i < 60:
    Tick(coord_x, coord_y)
    poligon[coord_y][coord_x] = '*'
    i += 1
print(*poligon, sep='\n')
