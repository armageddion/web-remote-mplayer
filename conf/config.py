import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    PROJECTOR_1 = os.environ.get('PROJECTOR_1') or 'http://192.168.0.201:5001'
    PROJECTOR_2 = os.environ.get('PROJECTOR_2') or 'http://192.168.0.202:5001'
    PROJECTOR_3 = os.environ.get('PROJECTOR_3') or 'http://192.168.0.203:5001'
    ONBOARD_TV = os.environ.get('ONBOARD_TV') or 'http://192.168.0.205:5001'

    USER_HOME = os.path.expanduser("~")
