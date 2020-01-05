def tick(x, y):
    from random import randint
    # get_pixel(x, y)
    # my_color
    move = randint(1, 2)
    if move == 1:
        if x > 0 and data[0] and (0 <= y <= game.height - 1):
            x -= 1
            return Move.Left
        elif x < game.width - 1 and not data[0] and (
                0 <= y <= game.height - 1):
            x += 1
            return Move.Right
    elif move == 2:
        if y > 0 and (0 <= x <= game.width - 1) and data[1]:
            y -= 1
            return Move.Up
        elif y < game.height - 1 and (0 <= x <= game.width - 1) and not data[1]:
            y += 1
            return Move.Down

    if x == game.width - 1:
        data[0] = True
        return Move.Left
    if x == 0:
        data[0] = False
        return Move.Right
    if y == game.height - 1:
        data[1] = True
        return Move.Up
    if y == 0:
        data[1] = False
        return Move.Down