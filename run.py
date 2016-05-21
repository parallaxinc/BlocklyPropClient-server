from server import app, socket_io

# app.run(host='0.0.0.0', port=8081, debug=True)
socket_io.run(app, host='0.0.0.0', port=8081)