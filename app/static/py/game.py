import json

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
        for update in Game().updates:
            x = update[0]
            y = update[1]
            data = update[2]
            Game().ctx.fillStyle = COLORS[data]
            Game().ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
            # Game().ctx.beginPath()
            # Game().ctx.rect(update['x'] * PIXEL_WIDTH, update['y'] * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
            # Game().ctx.stroke()
            Game().current_field[x][y] = data

    @staticmethod
    def on_initial(data):
        global GAME_WIDTH, GAME_HEIGHT
        data = JSON.parse(data)
        GAME_WIDTH = data['width']
        GAME_HEIGHT = data['height']
        Game().current_field = data['field']
        Game().canvas.attrs['height'] = GAME_WIDTH * PIXEL_WIDTH
        Game().canvas.attrs['width'] = GAME_HEIGHT * PIXEL_WIDTH
        for j in range(GAME_WIDTH):
            for i in range(GAME_HEIGHT):
                Game().ctx.beginPath()
                Game().ctx.rect(i * PIXEL_WIDTH, j * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                Game().ctx.fillStyle = COLORS[Game().current_field[i][j]]
                Game().ctx.fill()
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
