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
    time_el = document.getElementById('time')
    ctx = canvas.getContext('2d')

    current_field = []
    updates = []
    bots = []
    new_bots = []
    socket = window.io()
    width = 0
    height = 0
    score = 0
    time = 0
    started = False

    @staticmethod
    def connect(_):
        Game().socket.disconnect()
        Game().socket.connect()

    def init(self):
        window.bind('visibilitychange', self.visibilitychange)
        window.bind('show', self.connect)
        window.bind('fade', self.socket.disconnect)
        self.init_socket()

    @staticmethod
    def init_socket():
        def on_connect():
            if document.hidden:
                Game().socket.disconnect()
                print('Connected, disconnecting')
            else:
                print('Connected')

        def on_disconnect(arg):
            print('Disconnected')
            if not document.hidden:
                Game().socket.disconnect()
                Game().socket = window.io()
                Game().socket.connect()
                Game().init_socket()

        Game().socket.on('connect', on_connect)
        Game().socket.on('initial', Game().on_initial)
        Game().socket.on('update', Game().on_update)
        Game().socket.on('disconnect', on_disconnect)

    @staticmethod
    def visibilitychange(*_):
        if document.hidden:
            Game().socket.disconnect()
        else:
            Game().connect(None)

    @staticmethod
    def draw_bots():
        game = Game()
        if not game.started:
            return
        for bot in game.bots:
            game.ctx.fillStyle = COLORS[game.current_field[bot['y']][bot['x']]]
            game.ctx.fillRect(bot['x'] * PIXEL_WIDTH, bot['y'] * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)

        for bot in game.new_bots:
            game.ctx.beginPath()
            game.ctx.arc(((bot['x'] * 2 + 1) * PIXEL_WIDTH) / 2, ((bot['y'] * 2 + 1) * PIXEL_WIDTH) / 2,
                         PIXEL_WIDTH / 4, 0, 2 * pi, False)
            game.ctx.fillStyle = '#263238'
            game.ctx.fill()
            if bot['crashed']:
                game.ctx.lineWidth = 2
                game.ctx.beginPath()
                game.ctx.moveTo(bot['x'] * PIXEL_WIDTH + PIXEL_WIDTH / 4, bot['y'] * PIXEL_WIDTH + PIXEL_WIDTH / 4)
                game.ctx.lineTo(bot['x'] * PIXEL_WIDTH + PIXEL_WIDTH / 4 + PIXEL_WIDTH / 2,
                                bot['y'] * PIXEL_WIDTH + PIXEL_WIDTH / 4 + PIXEL_WIDTH / 2)
                game.ctx.stroke()
                game.ctx.lineWidth = 2
                game.ctx.beginPath()
                game.ctx.moveTo(bot['x'] * PIXEL_WIDTH + PIXEL_WIDTH / 4 + PIXEL_WIDTH / 2,
                                bot['y'] * PIXEL_WIDTH + PIXEL_WIDTH / 4)
                game.ctx.lineTo(bot['x'] * PIXEL_WIDTH + PIXEL_WIDTH / 4, bot['y'] * PIXEL_WIDTH + PIXEL_WIDTH / 4 + PIXEL_WIDTH / 2)
                game.ctx.stroke()
        game.bots = game.new_bots
        game.new_bots = []

    @staticmethod
    def draw_score():
        Game().score_el.innerHTML = 'Счет:<br>'
        for bot in Game().bots:
            if bot['user_id'] == window.user_id:
                Game().score_el.innerHTML += '<b>'
            Game().score_el.innerHTML += f'{COLORS_HUMAN[bot["color"]]}: {bot["score"]}'
            if bot['user_id'] == window.user_id:
                Game().score_el.innerHTML += '</b>'
        Game().time_el.innerHTML = f'Осталось времени: <br>{Game().time} сек'

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
        Game().draw_score()

    @staticmethod
    def on_initial(data):
        data = JSON.parse(data)
        Game().width = data['width']
        Game().height = data['height']
        Game().bots = data['bots']
        Game().current_field = data['field']
        Game().canvas.attrs['height'] = Game().width * PIXEL_WIDTH
        Game().canvas.attrs['width'] = Game().height * PIXEL_WIDTH
        Game().started = data['started']
        for y in range(Game().width):
            for x in range(Game().height):
                Game().ctx.fillStyle = COLORS[Game().current_field[y][x]]
                Game().ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.beginPath()
                # Game().ctx.rect(i * PIXEL_WIDTH, j * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
                # Game().ctx.stroke()
        Game().draw_bots()

    @staticmethod
    def on_update(data, ack):
        data = JSON.parse(data)
        Game().updates = data['updates']
        Game().new_bots = data['bots']
        Game().time = data['time']
        Game().started = data['started']
        window.requestAnimationFrame(Game().draw)
        ack()


game = Game()
game.init()
