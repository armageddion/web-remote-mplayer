import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    PROJECTOR_1 = 'http://192.168.1.102:5001'
    PROJECTOR_2 = 'http://192.168.1.18:5001'
    PROJECTOR_3 = 'http://192.168.1.202:5001'

    USER_HOME = os.path.expanduser("~")