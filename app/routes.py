import copy
import json
from threading import Timer

import eventlet
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import emit
from werkzeug.urls import url_parse

from app import app, socketio
from app.forms import LoginForm, RegisterForm, IndexForm
from app.models import *
from game_service import Game

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=False, score=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = IndexForm()
    if form.validate_on_submit():
        return redirect(url_for('game'))
    elif request.method == 'GET':
        form.language = 0
    return render_template('index.html', form=form)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/game')
def game():
    return render_template('game.html')


clients = {}


def ack():
    data = clients[request.sid]
    q = data['queue']
    for i in q:
        data['field'][i[1]][i[0]] = i[2]


def do_update():
    game = Game()
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

            socketio.server.emit('update', json.dumps({'updates': updates, 'bots': bots_frontend}), namespace='/',
                                 room=user, skip_sid=None, callback=_callback_wrapper)
            data['queue'] += updates
    except RuntimeError:
        print('Err')
    Timer(0.1, lambda: eventlet.spawn(do_update)).start()


@socketio.on('connect')
def handle_message():
    emit('initial', json.dumps({'height': Game().height, 'width': Game().width, 'field': Game().field}))
    clients[request.sid] = {'field': copy.deepcopy(Game().field), 'queue': []}


@socketio.on('request_initial')
def handle_message():
    emit('initial', json.dumps({'height': Game().height, 'width': Game().width, 'field': Game().field}))


@socketio.on('disconnect')
def handle_disconnect():
    del clients[request.sid]


Timer(0.5, lambda: eventlet.spawn(do_update)).start()
