# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('test.html')

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('message')
# def handle_message(message):
#     print('Received message: ' + message)
#     emit('message', message, broadcast=True)

# if __name__ == '__main__':
#     ssl_context = ('/home/monica/certificate.pem', '/home/monica/key.pem')
#     socketio.run(app, host='0.0.0.0', port=4002, debug=True, ssl_context=ssl_context)

import json

# Write to JSON file
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Read from JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

file_path = 'wheelchair_profile.json'

wheelchair_id = 5
lang_selected = 'hindi'

data = {
    "1": "{'app_language':'english'}",
    "2": "{'app_language':'hindi'}",
    "3": "{'app_language':'tamil'}"
}

write_json(file_path, data)

data2 = read_json(file_path)
print(data2['1'])

# with open('wheelchair_profile.json', 'r') as json_file:
#     profile = json.load(json_file)
#     profile[wheelchair_id]=lang_selected

# with open('wheelchair_profile.json', 'w') as json_file:
#     json.dump(profile, json_file, indent=4)





'''
{
    "1": "{'app_language':'english'}",
    "2": "{'app_language':'tamil'}"
}

// {
//     "1": "{'app_language':'english'}",
//     "2": "{'app_language':'tamil'}"
// }
'''