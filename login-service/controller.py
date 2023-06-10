from flask import request, jsonify
from user import User

class LoginController:
    def __init__(self, login_service):
        self.login_service = login_service
        
    def register(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')

        if username and password:
            user = User(username, password)
            if self.login_service.add_user(user):
                return self._message_response('Success!', 200)
            else:
                return self._message_response('Username is already used', 400)

        return self._message_response('Not all fields', 400)

    def login(self):
        json = request.get_json()
        username = json.get('username')
        password = json.get('password')

        if username and password:
            user = User(username, password)
            if self.login_service.check_credentials(user):
                return self._message_response('Success!', 200)
            else:
               return self._message_response('Invalid credentials', 400)

        return self._message_response('Not all fields', 400)
    
    def _message_response(self, message, status):
        resp = jsonify({'message': message})
        resp.status_code = status
        return resp