from server import socket_io

app_namespace = '/app'


@socket_io.on('connect', namespace=app_namespace)
def on_connect():
    print('app connected')


@socket_io.on('serial connect', namespace=app_namespace)
def handle_message(message):
    print message
