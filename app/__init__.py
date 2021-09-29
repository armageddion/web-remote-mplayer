from flask import Flask
from conf import Config

import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

# set up logging directory
if not os.path.exists('logs'):
    os.mkdir('logs')

# set up log management
file_handler = RotatingFileHandler('logs/roz_logs.log', maxBytes=10240, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info("ROZ flask startup")

from app import routes