import random
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
        self.ship_locations = self.assign_ship_locations()
        self.styled_board = self.display_board()

    
    def create_board(self):
        """
        Creates a new, empty board for the player.
        """
        self.board = []
        for row in range(self.board_size):
            self.board.append([])
            for column in range(self.board_size):
                self.board[row].append('-')
        
        return self.board
    

    def assign_ship_locations(self):
        """
        Assigns random locations for ships on the player's board.
        """
        ship_locations = []
        ships = 0
        while ships < num_ships:
            random_row = random.randrange(board_size)
            random_column = random.randrange(board_size)
            random_pair = (random_row, random_column)
            if random_pair not in ship_locations:
                ship_locations.append(random_pair)
                self.board[random_row][random_column] = 1
                ships += 1

        return ship_locations


    def display_board(self):
        """
        Displays player board in a clean and formatted structure.
        """
        board_str = f""        
        for row in range(board_size):
            row_str = f""
            for column in range(board_size):
                column_str = f" {self.board[row][column]} "
                if column == board_size - 1:
                    column_str += f"\n"
                row_str += column_str
            board_str += row_str
        
        return board_str


user = Board(board_size, num_ships, user_name)
computer = Board(board_size, num_ships, "computer")


def print_instructions():
    """
    Prints gameplay instructions to the user.
    """
    print("Here are the instructions...")


def main():
    """
    Main game function.
    """
    print("Welcome to the game!")
    print_instructions()

main()