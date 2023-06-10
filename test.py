from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('test.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    ssl_context = ('/home/monica/certificate.pem', '/home/monica/key.pem')
    socketio.run(app, host='0.0.0.0', port=4002, debug=True, ssl_context=ssl_context)
