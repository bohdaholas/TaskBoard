from app import app, mysql
from repository import BoardsRepository
from service import BoardsService
from controller import BoardsController
 
boards_repository = BoardsRepository(mysql)
boards_service = BoardsService(boards_repository)
boards_controller = BoardsController(boards_service)

@app.route('/boards', methods=['GET'])
def boards():
    return boards_controller.boards()

@app.route('/create', methods=['POST'])
def create():
    return boards_controller.create()

if __name__ == '__main__':
    app.run(host="localhost", port=8082, debug=True)