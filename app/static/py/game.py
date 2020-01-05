from math import pi

from browser import document, window
from javascript import JSON

COLORS = {'A': '#c62828',
          'B': '#283593',
          'C': '#43a047',
          'D': '#f57c00',
          '0': '#aaaaaa'}
COLORS_HUMAN = {'A': 'Красный',
                'B': 'Синий',
                'C': 'Зелёный',
                'D': 'Оранжевый',
                '0': 'Серый'}
PIXEL_WIDTH = 20


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Game(Singleton):
    canvas = document.getElementById('game')
    score_el = document.getElementById('score')
    ctx = canvas.getContext('2d')

    current_field = []
    updates = []
    bots = []
    new_bots = []
    socket = window.io()
    width = 0
    height = 0
    score = 0

    def init(self):
        self.socket.on('connect', lambda: print('Connected'))
        self.socket.on('initial', self.on_initial)
        self.socket.on('update', self.on_update)

        def on_disconnect(arg):
            print('Disconnected')
            Game().socket = window.io()
            Game().init()

        self.socket.on('disconnect', on_disconnect)
        window.bind('visibilitychange', self.request_init)

    @staticmethod
    def draw_bots():
        game = Game()
        for bot in game.bots:
            game.ctx.fillStyle = COLORS[game.current_field[bot['y']][bot['x']]]
            game.ctx.fillRect(bot['x'] * PIXEL_WIDTH, bot['y'] * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)

        for bot in game.new_bots:
            game.ctx.beginPath()
            game.ctx.arc(((bot['x'] * 2 + 1) * PIXEL_WIDTH) / 2, ((bot['y'] * 2 + 1) * PIXEL_WIDTH) / 2,
                         PIXEL_WIDTH / 4, 0, 2 * pi, False)
            game.ctx.fillStyle = '#263238'
            game.ctx.closePath()
            game.ctx.fill()

    @staticmethod
    def draw_score():
        Game().score_el.innerHTML = 'Счет:<br>'
        for bot in Game().bots:
            Game().score_el.innerHTML += f'{COLORS_HUMAN[bot["color"]]}: {bot["score"]}<br>'

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
        Game().draw_bots()
        game.bots = game.new_bots
        Game().draw_score()

    @staticmethod
    def on_initial(data):
        data = JSON.parse(data)
        Game().width = data['width']
        Game().height = data['height']
        Game().current_field = data['field']
        Game().canvas.attrs['height'] = Game().width * PIXEL_WIDTH
        Game().canvas.attrs['width'] = Game().height * PIXEL_WIDTH
        for y in range(Game().width):
            for x in range(Game().height):
                Game().ctx.fillStyle = COLORS[Game().current_field[y][x]]
                Game().ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.beginPath()
                # Game().ctx.rect(i * PIXEL_WIDTH, j * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.stroke()
        Game().draw_bots()

    @staticmethod
    def request_init(*_):
        if document.hidden:
            return
        Game().socket.emit('request_initial')

    @staticmethod
    def on_update(data):
        data = JSON.parse(data)
        Game().updates = data['updates']
        Game().new_bots = data['bots']
        window.requestAnimationFrame(Game().draw)


game = Game()
game.init()
