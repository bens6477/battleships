scores = {"computer": 0, "user": 0}
print(scores)

board_size = 5
num_ships = 5
user_name = "Ben"

class Board:
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, board_size, num_ships, name):
        self.board_size = board_size
        self.num_ships = num_ships
        self.name = name


user_board = Board(board_size, num_ships, user_name)
computer_board = Board(board_size, num_ships, "computer")


def create_board(player):
    """
    Creates a board for the player passed into the function.
    """
    print(player.name)
    board = []
    for row in range(board_size):
        board.append([]) 
        for column in range(board_size):
            board[row].append("-")
    print(board)


create_board(user_board)