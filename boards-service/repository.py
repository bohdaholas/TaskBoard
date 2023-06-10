from board import Board

class BoardsRepository:
    def __init__(self, mysql):
        self.mysql = mysql
        self.conn = None
        self.cursor = None
    
    def get_user_boards(self, user) -> list:
        self._start_connection()
        self.cursor.execute('''
            SELECT * FROM boards
            JOIN members ON boards.board_id = members.board_id
            WHERE members.username = %s
        ''', (user,))
        rows = self.cursor.fetchall()
        boards = [Board(row[0], row[1], row[2]) for row in rows]
        self._end_connection()
        return boards

    def create_board(self, board, members):
        self._start_connection()
        self.cursor.execute('''INSERT INTO boards VALUES(%s,%s,%s)''',(0, board.title, board.description))
        board_id = self.cursor.lastrowid
        for member in members:
            self.cursor.execute('''INSERT INTO members VALUES(%s,%s,%s)''',(0, member, board_id))
        self.conn.commit()
        self._end_connection()

    def _start_connection(self):
        self.conn = self.mysql.connection
        self.cursor = self.conn.cursor()

    def _end_connection(self):
        if self.cursor:
            self.cursor.close()