poligon = [['.'] * 9 for i in range(9)]

my_color = '*'
coord_x = coord_y = 0
data = [True, True, True]

def Tick(coord_x, coord_y):
    return move()

def get_pixel(coord_x, coord_y):
    global poligon
    return poligon[coord_y][coord_x]

def move():
    global coord_x, coord_y, my_color, data
    if data[2]:
        if coord_x < len(poligon) - 1:
            if coord_y < len(poligon) - 1 and data[0]:
                coord_y += 1
                return 'move_down()'
            if coord_y > 0 and not data[0]:
                coord_y -= 1
                return 'move_up()'
            if coord_y == 0:
                data[0] = True
                if coord_x < len(poligon) - 1:
                    coord_x += 1
                    return 'move_right()'
            if coord_y == len(poligon) - 1:
                data[0] = False
                if coord_x < len(poligon) - 1:
                    coord_x += 1
                    return 'move_right()'
        elif coord_x == len(poligon) - 1:
            if coord_y < len(poligon) - 1:
                coord_y += 1
                return 'move_down()'
            if coord_y == len(poligon) - 1:
                data[2] = False

    elif not data[2]:
        if coord_x > 0:
            if coord_y > 0 and data[1]:
                coord_y -= 1
                return 'move_up()'
            if coord_y < len(poligon) - 1 and not data[1]:
                coord_y += 1
                return 'move_down()'
            if coord_y == len(poligon) - 1:
                data[1] = True
                if coord_x > 0:
                    coord_x -= 1
                    return 'move_left()'
            if coord_y == 0:
                data[1] = False
                if coord_x > 0:
                    coord_x -= 1
                    return 'move_left()'
        elif coord_x == 0:
            if coord_y > 0:
                coord_y -= 1
                return 'move_up()'
            if coord_y == 0:
                data[2] = True





i = 0

while i < 166:
    poligon[coord_y][coord_x] = my_color
    Tick(coord_x, coord_y)
    i += 1

print(*poligon, sep='\n')