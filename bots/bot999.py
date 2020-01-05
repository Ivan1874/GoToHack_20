def toBorder(m):
    if m == 0:
        return Move.Right
    elif m == 1:
        return Move.Down
    elif m == 2:
        return Move.Left
    else:
        return Move.Up


def tick(x, y):
    lst = [game.width - 1 - x, game.height - 1 - y, x, y]
    m = min(lst)
    i = lst.index(m)
    dx = dy = 0
    if i == 0:
        dx = 1
    elif i == 1:
        dy = 1
    elif i == 2:
        dx = -1
    else:
        dy = -1
    if m != 0 and get_pixel(y + dy, x + dx) != my_color:
        return toBorder(i)
    else:
        if x < game.width - 1 - y:
            if y > 0 and get_pixel(y - 1, x) != my_color:
                return Move.Up
            elif x < game.width - 1 and get_pixel(y, x + 1) != my_color:
                return Move.Right
            else:
                ls = []
                ls.append(reversed(lst))
                ma = ls.index(max(ls))
                return toBorder(ma)
        else:
            if y < game.height - 1 and get_pixel(y + 1, x) != my_color:
                return Move.Down
            elif x > 0 and get_pixel(y, x - 1) != my_color:
                return Move.Left
            else:
                ls = []
                ls.append(reversed(lst))
                ma = ls.index(max(ls))
                return toBorder(ma)
