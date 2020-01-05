import copy
import json
from threading import Timer

import eventlet
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import emit
from werkzeug.urls import url_parse

from app import app, socketio
from app.forms import LoginForm, RegisterForm, ConfigForm, AddBotForm
from app.models import *
from game_service import Game, Bot

current_user: User
eventlet.monkey_patch()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль!')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('redirect')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Вход успешен!')
        return redirect(next_page)
    return render_template('user/login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы!')
    return redirect(url_for('index'))


default_code = '''def tick(x, y):
    return Move.Up'''


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=False, score=0, code=default_code,
                    default_data=json.dumps([]))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = AddBotForm()
    if form.validate_on_submit():
        color = None
        if len(Game().bots) == 0:
            x, y = 0, 0
            color = 'A'
        elif len(Game().bots) == 1:
            x, y = width - 1, height - 1
            color = 'B'
        elif len(Game().bots) == 2:
            x, y = width - 1, 0
            color = 'C'
        elif len(Game().bots) == 3:
            x, y = 0, height - 1
            color = 'D'
        else:
            flash('Максимальное количество игроков!')
        if color is not None:
            Game().add_bot(
                Bot(x=x, y=y, data=current_user.default_data, color=color, code=current_user.code, user=current_user))
        flash('Бот добавлен!')
        return redirect(url_for('game'))
    show_form = True
    placeholder_text = ''
    if current_user.code == default_code:
        show_form = False
        placeholder_text = 'Измените код вашего бота для продолжения'
    if Game().started:
        show_form = False
        placeholder_text = 'Игра уже началась, нажмите <a href="/game">здесь</a>, чтобы посмотреть'
    return render_template('index.html', show_form=show_form, placeholder_text=placeholder_text, form=form)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = ConfigForm()
    if form.validate_on_submit():
        current_user.code = form.code.data
        current_user.default_data = form.data.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.language.data = 0
        form.code.data = current_user.code
        form.data.data = current_user.default_data
    return render_template('user.html', form=form)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/game')
@login_required
def game():
    return render_template('game.html', user=current_user)


width = 16
height = 16


@app.route('/start_game')
def start_game():
    Game().init(width, height, 40)
    Game().init_bots()
    Game().started = True
    socketio.emit('initial', json.dumps({'height': Game().height, 'width': Game().width, 'field': Game().field,
                                         'bots': [bot.frontend() for bot in Game().bots], 'started': Game().started}))
    for client in clients:
        clients[client]['field'] = copy.deepcopy(Game().field)
    return 'OK'


clients = {}


def ack():
    data = clients[request.sid]
    q = data['queue']
    for i in q:
        data['field'][i[1]][i[0]] = i[2]


def do_update():
    game = Game()
    if game.started:
        game.tick()
        bots_frontend = [bot.frontend() for bot in game.bots]
        try:
            for user in clients:
                data = clients[user]
                updates = []
                for y in range(len(data['field'])):
                    for x in range(len(data['field'][y])):
                        if game.field[y][x] != data['field'][y][x]:
                            updates.append((x, y, game.field[y][x]))

                def _callback_wrapper(*args):
                    return socketio._handle_event(ack, None, '/', user, *args)

                socketio.server.emit('update', json.dumps(
                    {'updates': updates, 'bots': bots_frontend, 'time': game.time_remaining,
                     'started': Game().started}), namespace='/',
                                     room=user, skip_sid=None, callback=_callback_wrapper)
                data['queue'] += updates
        except RuntimeError:
            print('Err')
    Timer(1, lambda: eventlet.spawn(do_update)).start()


@socketio.on('connect')
def handle_message():
    emit('initial', json.dumps({'height': Game().height, 'width': Game().width, 'field': Game().field,
                                'bots': [bot.frontend() for bot in Game().bots], 'started': Game().started}))
    clients[request.sid] = {'field': copy.deepcopy(Game().field), 'queue': []}


@socketio.on('request_initial')
def handle_message():
    emit('initial', json.dumps({'height': Game().height, 'width': Game().width, 'field': Game().field,
                                'bots': [bot.frontend() for bot in Game().bots], 'started': Game().started}))


@socketio.on('disconnect')
def handle_disconnect():
    del clients[request.sid]


Timer(1, lambda: eventlet.spawn(do_update)).start()
