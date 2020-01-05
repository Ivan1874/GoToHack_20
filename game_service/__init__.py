from helper import Singleton, Dict

colors = 'ABCD0'


class Move:
    Left = (-1, 0)
    Right = (1, 0)
    Up = (0, -1)
    Down = (0, 1)


class Bot(Dict):
    def __init__(self, *, x, y, data, color, code, score):
        super().__init__([], x=x, y=y, data=data, color=color, code=code, score=score)

    def frontend(self):
        d = dict(self)
        del d['data']
        del d['code']
        return d


class Game(Singleton):
    field = []
    width = 32
    height = 32
    bots = []
    initialized = False
    bot_color_map = {}

    class GameDefenition:
        width: int
        height: int

        def __init__(self, width, height):
            self.width = width
            self.height = height

    def tick(self):
        game_def = self.GameDefenition(self.width, self.height)
        for i in range(len(self.bots)):
            bot: Bot = self.bots[i]
            execstr = bot.code + '\n\n\n' \
                                 f'tick.__globals__[\'my_data\'] = data\n' \
                                 f'tick.__globals__[\'game\'] = game\n' \
                                 f'tick.__globals__[\'get_pixel\'] = get_pixel\n' \
                                 f'tick.__globals__[\'my_color\'] = \'{bot.color}\'\n' \
                                 f'result = tick({bot.x}, {bot.y})\n' \
                                 f'data = tick.__globals__[\'data\']'
            namespace = {'get_pixel': self.get_pixel,
                         'game': game_def,
                         'data': bot.data,
                         'Move': Move}
            exec(execstr, namespace, namespace)
            move = namespace['result']
            bot.data = namespace['data']
            bot.x += move[0]
            bot.y += move[1]
            if self.field[bot.y][bot.x] != bot.color:
                bot.score += 1
                if self.field[bot.y][bot.x] != '0':
                    self.bot_color_map[self.field[bot.y][bot.x]].score -= 1
            self.field[bot.y][bot.x] = bot.color

    def init(self, width, height):
        if not self.initialized:
            self.width = width
            self.height = height
            self.field = [['0'] * self.width for x in range(self.height)]
            self.bots.append(Bot(x=0, y=0, data=[False, False], color='A',
                                 code=open('game_service/default_bot_1.py', 'r').read(), score=1))
            self.bots.append(Bot(x=self.width - 1, y=self.height - 1, data=[False, False], color='B',
                                 code=open('bots/bot999.py', 'r').read(), score=1))
            for bot in self.bots:
                self.field[bot.y][bot.x] = bot.color
                self.bot_color_map[bot.color] = bot
            self.initialized = True

    def reset(self):
        self.initialized = False
        self.bots = []
        self.field = []

    def get_pixel(self, x, y):
        return self.field[y][x]


Game().init(32, 32)
