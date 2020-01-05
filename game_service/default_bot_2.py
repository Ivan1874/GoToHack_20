def tick(x, y):
    if data[2]:
        if x < game.width - 1:
            if y < game.height - 1 and data[0]:
                y += 1
                return Move.Down
            if y > 0 and not data[0]:
                y -= 1
                return Move.Up
            if y == 0:
                data[0] = True
                if x < game.width - 1:
                    x += 1
                    return Move.Right
            if y == game.height - 1:
                data[0] = False
                if x < game.width - 1:
                    x += 1
                    return Move.Right
        elif x == game.width - 1:
            if y < game.height - 1:
                y += 1
                return Move.Down
            if y == game.height - 1:
                data[2] = False

    elif not data[2]:
        if x > 0:
            if y > 0 and data[1]:
                y -= 1
                return Move.Up
            if y < game.height - 1 and not data[1]:
                y += 1
                return Move.Down
            if y == game.height - 1:
                data[1] = True
                if x > 0:
                    x -= 1
                    return Move.Left
            if y == 0:
                data[1] = False
                if x > 0:
                    x -= 1
                    return Move.Left
        elif x == 0:
            if y > 0:
                y -= 1
                return Move.Up
            if y == 0:
                data[2] = True
