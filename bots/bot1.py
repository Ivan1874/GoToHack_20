poligon = [['.'] * 9 for i in range(9)]

my_color = '*'
flag = True; flagX = flagY = True

coord_x = coord_y = 0

def Tick(coord_x, coord_y):
    return move()

def move():
    global poligon, my_color, flag, flagX, flagY, coord_x, coord_y
    if flag:
        if coord_x > 0 and my_color != get_pixel(coord_x - 1, coord_y) and flagX:
            coord_x -= 1
            return 'move_left()'
        elif coord_x < len(poligon[coord_y]) - 1 and my_color != get_pixel(coord_x + 1, coord_y) and not flagX:
            coord_x += 1
            return 'move_right()'
        elif coord_y > 0 and my_color != get_pixel(coord_x, coord_y - 1) and flagY:
            coord_y -= 1
            return 'move_up()'
        elif coord_y < len(poligon) - 1 and my_color != get_pixel(coord_x, coord_y + 1) and not flagY:
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

    if coord_x < len(poligon[coord_y]) - 1 and my_color == get_pixel(coord_x + 1, coord_y):
        flag = False
        relaxe()
    elif coord_x > 0 and my_color == get_pixel(coord_x - 1, coord_y):
        flag = False
        relaxe()
    elif coord_y > 0 and my_color == get_pixel(coord_x, coord_y - 1):
        flag = False
        relaxe()
    elif coord_y < len(poligon) and my_color == get_pixel(coord_x, coord_y  + 1):
        flag = False
        relaxe()

def relaxe():
    global coord_y, coord_x, flag
    if check_better(coord_x, coord_y) == 'go_left()':
        while coord_x > 0 and my_color == get_pixel(coord_x, coord_y):
            coord_x -= 1
            return 'move_left()'
    elif check_better(coord_x, coord_y) == 'go_right()':
        while coord_x < len(poligon[coord_y]) and my_color == get_pixel(coord_x, coord_y):
            coord_x += 1
            return 'move_right()'
    elif check_better(coord_x, coord_y) == 'go_up()':
        while coord_y > 0 and my_color == get_pixel(coord_x, coord_y):
            coord_y -= 1
            return 'move_up()'
    elif check_better(coord_x, coord_y) == 'go_down()':
        while coord_y < len(poligon) and my_color == get_pixel(coord_x, coord_y):
            coord_y += 1
            return 'move_down()'
    if coord_x < len(poligon[coord_y]) - 1 and my_color != get_pixel(coord_x + 1, coord_y):
        flag = True
    elif coord_x > 0 and my_color != get_pixel(coord_x - 1, coord_y):
        flag = True
    elif coord_y < len(poligon) and my_color != get_pixel(coord_x, coord_y):
        flag = True
    elif coord_y > 0 and my_color != get_pixel(coord_x, coord_y):
        flag = True
    else:
        if 0 < coord_x:
            coord_x -= 1
            move()
        elif coord_x < len(poligon[coord_y]) - 1:
            coord_x += 1
            move()
        elif coord_y > 0:
            coord_y -= 1
            move()
        elif coord_y < len(poligon) - 1:
            coord_y += 1
            move()




def check_better(coord_x, coord_y):
    Lcoord_x = Dcoord_y = Rcoord_x = Ucoord_y = 0
    old_coords = (coord_x, coord_y)
    while coord_x > 0 and get_pixel(coord_x, coord_y) == my_color:
        coord_x -= 1; Lcoord_x += 1
    coord_x = old_coords[0]
    while coord_x < len(poligon[coord_y]) and get_pixel(coord_x, coord_y) == my_color:
        coord_x += 1; Rcoord_x += 1
    coord_x = old_coords[0]
    while coord_y > 0 and get_pixel(coord_x, coord_y):
        coord_y -= 1; Ucoord_y += 1
    coord_y = old_coords[1]
    while coord_y < len(poligon) and get_pixel(coord_x, coord_y):
        coord_y += 1; Dcoord_y += 1
    coord_y = old_coords[1]
    print(Lcoord_x, Rcoord_x, Ucoord_y, Dcoord_y, 'its coords', coord_y, coord_x)
    if min(Lcoord_x, Rcoord_x, Ucoord_y, Dcoord_y) == Lcoord_x:
        return 'go_left()'
    elif min(Lcoord_x, Rcoord_x, Ucoord_y, Dcoord_y) == Rcoord_x:
        return 'go_right()'
    elif min(Lcoord_x, Rcoord_x, Ucoord_y, Dcoord_y) == Ucoord_y:
        return 'go_up()'
    elif min(Lcoord_x, Rcoord_x, Ucoord_y, Dcoord_y) == Dcoord_y:
        return 'go_down()'


def get_pixel(coord_x, coord_y):
    global poligon
    return poligon[coord_y][coord_x]

i = 0

while i < 90:
    Tick(coord_x, coord_y)
    poligon[coord_y][coord_x] = '*'
    i += 1

print(*poligon, sep='\n')