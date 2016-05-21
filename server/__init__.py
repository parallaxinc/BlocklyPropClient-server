# Import properties files utils
import logging
from ConfigParser import ConfigParser

import eventlet
from flask_socketio import SocketIO

from FakeSecHead import FakeSecHead
from os.path import expanduser, isfile

# Import Flask
from flask import Flask

# Define the WSGI application object
from raven.contrib.flask import Sentry

app = Flask(__name__)

# Load basic configurations
# app.config.from_object('config')

# ---------------------------------------------- Monkey patching eventlet ---------------------------------------
eventlet.monkey_patch()

# --------------------------------------------- Application configurations --------------------------------------
defaults = {
            'master': 'http://127.0.0.1:8082',
            'message_queue': 'redis://',
            'sentry-dsn': None,
}

configfile = expanduser("~/blocklypropclient-server.properties")
print('Looking for config file: %s' % configfile)
if isfile(configfile):
    configs = ConfigParser(defaults)
    configs.readfp(FakeSecHead(open(configfile)))

    app_configs = {}
    for (key, value) in configs.items('section'):
        app_configs[key] = value
    app.config['SERVER_PROPERTIES'] = app_configs
else:
    app.config['SERVER_PROPERTIES'] = defaults


# -------------------------------------- Module initialization -------------------------------------------------
logging.basicConfig(level=logging.DEBUG)

if app.config['SERVER_PROPERTIES']['sentry-dsn'] is not None:
    logging.info("Initializing Sentry")
    sentry = Sentry(app,
                    dsn=app.config['SERVER_PROPERTIES']['sentry-dsn'],
                    logging=True,
                    level=logging.ERROR
                    )
else:
    logging.info("No Sentry configuration")

logging.info('Using message queue: %s', app.config['SERVER_PROPERTIES']['message_queue'])
socket_io = SocketIO(app, message_queue=app.config['SERVER_PROPERTIES']['message_queue'])

# -------------------------------------------- Services --------------------------------------------------------
logging.info("Initializing services")
# from app.WebSocket_Apps import controllers
from server.WebSocket_Clients import controllers
# from app.AuthToken.controllers import auth_token_app

# app.register_blueprint(auth_token_app)
