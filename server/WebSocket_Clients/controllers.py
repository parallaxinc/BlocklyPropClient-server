import logging

from flask_socketio import emit

from server import socket_io

namespace = '/client'


@socket_io.on('connect', namespace=namespace)
def on_connect():
    logging.info('client connected')
    emit('test', {'hello': 'test connect'}, namespace='/')  # , namespace=namespace)
    return {'hello': 'test'}


@socket_io.on('serial connect', namespace=namespace)
def handle_message(message):
    logging.info('serial connected')
    print(message)


@socket_io.on('test2')
def handle_message_test2(message):
    print(message)
    emit('test2', {'hello': 'test connect'})


@socket_io.on('connect')
def on_connect():
    logging.info('socket connected')


@socket_io.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('error', e)