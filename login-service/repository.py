from app import bcrypt
from user import User

class LoginRepository:
    def __init__(self, mysql):
        self.mysql = mysql
        self.conn = None
        self.cursor = None
    
    def add_user(self, user) -> bool:
        self._start_connection()
        try:
            pw_hash = bcrypt.generate_password_hash(user.password).decode('utf-8')
            self.cursor.execute('''INSERT INTO users VALUES(%s,%s)''',(user.username, pw_hash))
            self.conn.commit()
            status = True
        except:
            status = False
        finally:
            self._end_connection()
            return status

    def check_credentials(self, user) -> bool:
        status = False
        self._start_connection()
        self.cursor.execute('''SELECT * FROM users WHERE username=%s''', (user.username,))
        row = self.cursor.fetchone()
        if row and self._check_hash(row[1], user.password):
            status = True
        self._end_connection()
        return status
    
    def _check_hash(self, pw_hash, pw_input) -> bool:
        return bcrypt.check_password_hash(pw_hash, pw_input)

    def _start_connection(self):
        self.conn = self.mysql.connection
        self.cursor = self.conn.cursor()

    def _end_connection(self):
        if self.cursor:
            self.cursor.close()