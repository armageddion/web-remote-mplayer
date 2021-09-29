import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    PROJECTOR_1 = '192.168.1.200'
    PROJECTOR_2 = '192.168.1.201'
    PROJECTOR_3 = '192.168.1.202'

    USER_HOME = os.path.expanduser("~")