from app import app, mysql
from repository import LoginRepository
from service import LoginService
from controller import LoginController
 
login_repository = LoginRepository(mysql)
login_service = LoginService(login_repository)
login_controller = LoginController(login_service)

@app.route('/register', methods=['POST'])
def register():
    return login_controller.register()

@app.route('/login', methods=['POST'])
def login():
    return login_controller.login()

if __name__ == '__main__':
    app.run(host="localhost", port=8081, debug=True)