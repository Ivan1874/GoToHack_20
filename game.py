from app import socketio, app
from app.models import *


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


socketio.run(app, host='0.0.0.0', port=8080)
