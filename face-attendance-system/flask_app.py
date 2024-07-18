from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from main import App

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app_instance = App()  # No need for db_uri and db_name here

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    message, success = app_instance.login(data['image'])
    return jsonify({'message': message, 'success': success})

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    message, success = app_instance.logout(data['image'])
    return jsonify({'message': message, 'success': success})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    message = app_instance.register_new_user(data['image'], data['name'])
    return jsonify({'message': message})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
