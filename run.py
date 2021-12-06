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
        self.board = self.create_board()

    
    def create_board(self):
        """
        Creates a board for the player passed into the function.
        """
        print(self.name)
        self.board = []
        for row in range(self.board_size):
            self.board.append([]) 
            for column in range(self.board_size):
                self.board[row].append("-")
        return self.board

user = Board(board_size, num_ships, user_name)
computer = Board(board_size, num_ships, "computer")


print(user.board)


