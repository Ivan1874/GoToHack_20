import traceback

from app import db
from app.models import User
from helper import Singleton, Dict
from sqlalchemy.orm import sessionmaker

colors = 'ABCD0'


class Move:
    Left = (-1, 0)
    Right = (1, 0)
    Up = (0, -1)
    Down = (0, 1)


class Bot:
    dict: Dict

    def __init__(self, *, x, y, data, color, code, user, score=0, crashed=False):
        self.dict = Dict(x=x, y=y, data=data, color=color, code=code, user_id=user.id, score=score, crashed=crashed)

    def frontend(self):
        d = dict(self.dict)
        del d['data']
        del d['code']
        return d


class Game(Singleton):
    field = []
    width = 0
    height = 0
    bots = []
    initialized = False
    bot_color_map = {}
    bot_user_map = {}
    started = False
    time_remaining = 0

    class GameDefenition:
        width: int
        height: int

        def __init__(self, width, height):
            self.width = width
            self.height = height

    def tick(self):
        if self.time_remaining <= 0:
            self.started = False
            return
        game_def = self.GameDefenition(self.width, self.height)
        for i in range(len(self.bots)):
            bot: Bot = self.bots[i]
            if bot.dict.crashed:
                continue
            execstr = bot.dict.code + '\n\n\n' \
                                      f'tick.__globals__[\'my_data\'] = data\n' \
                                      f'tick.__globals__[\'game\'] = game\n' \
                                      f'tick.__globals__[\'get_pixel\'] = get_pixel\n' \
                                      f'tick.__globals__[\'my_color\'] = \'{bot.dict.color}\'\n' \
                                      f'result = tick({bot.dict.x}, {bot.dict.y})\n' \
                                      f'data = str(tick.__globals__[\'data\'])'
            namespace = {'get_pixel': self.get_pixel,
                         'game': game_def,
                         'data': eval(bot.dict.data),
                         'Move': Move}
            try:
                exec(execstr, namespace, namespace)
            except Exception as e:
                print('Bot crashed')
                session = sessionmaker(bind=db.engine)()
                user = session.query(User).filter_by(id=bot.dict.user_id)
                user.last_exception = str(e) + '\n' + traceback.format_exc()
                bot.dict.crashed = True
                session.commit()
                session.close()
                continue
            move = namespace['result']
            new_x = bot.dict.x + move[0]
            new_y = bot.dict.y + move[1]
            if new_y >= self.height or new_x >= self.width or new_y < 0 or new_x < 0:
                print('Wall crashed')
                session = sessionmaker(bind=db.engine)()
                user = session.query(User).filter_by(id=bot.dict.user_id)
                bot.dict.crashed = True
                user.last_exception = 'Бот врезался в стену..........'
                print(user.last_exception)
                session.commit()
                session.close()
                continue
            bot.dict.data = namespace['data']
            bot.dict.x = new_x
            bot.dict.y = new_y
            if self.field[bot.dict.y][bot.dict.x] != bot.dict.color:
                bot.dict.score += 1
                if self.field[bot.dict.y][bot.dict.x] != '0':
                    self.bot_color_map[self.field[bot.dict.y][bot.dict.x]].score -= 1
            self.field[bot.dict.y][bot.dict.x] = bot.dict.color
        self.time_remaining -= 1

    def init(self, width, height, time):
        if not self.initialized:
            self.width = width
            self.height = height
            self.time_remaining = time
            self.field = [['0'] * self.width for x in range(self.height)]
            self.initialized = True

    def init_bots(self):
        for bot in self.bots:
            self.field[bot.dict.y][bot.dict.x] = bot.dict.color

    def add_bot(self, bot: Bot):
        self.bots.append(bot)
        self.bot_color_map[bot.dict.color] = bot
        if bot.dict.user_id != -1:
            self.bot_user_map[bot.dict.user_id] = bot

    def reset(self):
        self.initialized = False
        self.bots = []
        self.field = []

    def get_pixel(self, x, y):
        return self.field[y][x]
