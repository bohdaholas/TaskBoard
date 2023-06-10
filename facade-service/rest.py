from app import app
from flask import request, jsonify, session, render_template
import requests

login_service_url = 'http://localhost:8081'
boards_service_url = 'http://localhost:8082'

@app.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    response = requests.post(f'{login_service_url}/register', json=json_data)
    return response.content, response.status_code, response.headers.items()

@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    response = requests.post(f'{login_service_url}/login', json=json_data)
    if response.status_code == 200:
        session['user'] = json_data.get('username')
    return response.content, response.status_code, response.headers.items()

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return jsonify({'message': 'You successfully logged out'})

@app.route('/boards', methods=['GET'])
def get_boards():
    if 'user' in session:
        response = requests.get(f'{boards_service_url}/boards', params={'user': session['user']})
        return response.content, response.status_code, response.headers.items()

    response = jsonify({'message': 'Unauthorized'})
    response.status_code = 401
    return response

@app.route('/create_board', methods=['POST'])
def create_board():
    if 'user' in session:
        json_data = request.get_json()
        members = json_data.get("members", [])
        members.append(session['user'])
        json_data["members"] = members
        response = requests.post(f'{boards_service_url}/create', json=json_data)
        return response.content, response.status_code, response.headers.items()

    response = jsonify({'message': 'Unauthorized'})
    response.status_code = 401
    return response

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)