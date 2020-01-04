from math import pi

from browser import document, window
from javascript import JSON

COLORS = {'A': '#c62828',
          'B': '#283593',
          'C': '#43a047',
          'D': '#f57c00',
          '0': '#aaaaaa'}
PIXEL_WIDTH = 30
GAME_WIDTH = 0
GAME_HEIGHT = 0


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Game(Singleton):
    canvas = document.getElementById('game')
    ctx = canvas.getContext('2d')

    current_field = []
    updates = []
    bots = []
    new_bots = []
    socket = window.io()
    req_update = False

    def init(self):
        self.socket.on('connect', lambda: print('Connected'))
        self.socket.on('initial', self.on_initial)
        self.socket.on('update', self.on_update)

        def on_disconnect(arg):
            print('Disconnected')
            Game().socket = window.io()
            Game().init()

        self.socket.on('disconnect', on_disconnect)

    @staticmethod
    def draw(_):
        game = Game()
        for update in game.updates:
            x = update[0]
            y = update[1]
            data = update[2]
            game.ctx.fillStyle = COLORS[data]
            game.ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
            # game.ctx.beginPath()
            # game.ctx.rect(update['x'] * PIXEL_WIDTH, update['y'] * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
            # game.ctx.stroke()
            game.current_field[y][x] = data
        for i in range(len(game.bots)):
            bot = game.bots[i]
            game.ctx.fillStyle = COLORS[game.current_field[bot[1]][bot[0]]]

            game.ctx.fillRect(bot[0] * PIXEL_WIDTH, bot[1] * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)

            bot = game.new_bots[i]
            game.ctx.beginPath()
            game.ctx.arc(((bot[0] * 2 + 1) * PIXEL_WIDTH) / 2, ((bot[1] * 2 + 1) * PIXEL_WIDTH) / 2, PIXEL_WIDTH / 4, 0,
                           2 * pi, False)
            game.ctx.fillStyle = '#263238'
            game.ctx.closePath()
            game.ctx.fill()
        game.bots = game.new_bots

    @staticmethod
    def on_initial(data):
        global GAME_WIDTH, GAME_HEIGHT
        data = JSON.parse(data)
        GAME_WIDTH = data['width']
        GAME_HEIGHT = data['height']
        Game().current_field = data['field']
        Game().canvas.attrs['height'] = GAME_WIDTH * PIXEL_WIDTH
        Game().canvas.attrs['width'] = GAME_HEIGHT * PIXEL_WIDTH
        for y in range(GAME_WIDTH):
            for x in range(GAME_HEIGHT):
                Game().ctx.fillStyle = COLORS[Game().current_field[y][x]]
                Game().ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.beginPath()
                # Game().ctx.rect(i * PIXEL_WIDTH, j * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.stroke()

    @staticmethod
    def on_update(data):
        data = JSON.parse(data)
        Game().updates = data['updates']
        Game().new_bots = data['bots']
        window.requestAnimationFrame(Game().draw)
        Game().req_update = False


game = Game()
game.init()
