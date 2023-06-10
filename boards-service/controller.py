from flask import request, jsonify
from board import Board

class BoardsController:
    def __init__(self, boards_service):
        self.boards_service = boards_service
        
    def boards(self):
        user = request.args.get('user')
        if user:
            boards = self.boards_service.get_user_boards(user)
            json_boards = [board.__dict__ for board in boards]
            return jsonify({'boards': json_boards})

        return self._message_response('No user parameter', 400)

    def create(self):
        json = request.get_json()
        title = json.get('title')
        description = json.get('description')
        board = Board(0, title, description)
        members = json.get('members')

        if title and members:
            self.boards_service.create_board(board, members)
            return self._message_response('Success', 200)

        return self._message_response('Not all fields', 400)
    
    def _message_response(self, message, status):
        resp = jsonify({'message': message})
        resp.status_code = status
        return resp