from pprint import pprint

scores = {"computer": 0, "user": 0}

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
        self.board = []
        counter = 0
        for row in range(self.board_size):
            self.board.append([])
            for column in range(self.board_size):
                self.board[row].append(counter)
                counter += 1
        
        return self.board
    
    def display_board(self):
        """
        Displays user board in a clean and formatted structure.
        """
        board_str = f""
        for row in range(board_size):
            row_str = f"{self.board[row][0]} {self.board[row][1]} {self.board[row][2]} {self.board[row][3]} {self.board[row][4]}\n"
            board_str += row_str
        
        return board_str



user = Board(board_size, num_ships, user_name)
computer = Board(board_size, num_ships, "computer")

print(user.display_board())
