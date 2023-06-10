class BoardsService:
    def __init__(self, boards_repository):
        self.boards_repository = boards_repository
    
    def get_user_boards(self, user):
        return self.boards_repository.get_user_boards(user)

    def create_board(self, board, members):
        self.boards_repository.create_board(board, members)
