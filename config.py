class Config(object):
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://game_user:12345@192.168.43.247:5432/game'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
