scores = {"computer": 0, "player": 0}
print(scores)

size = 5
num_ships = 5
player_name = "Ben"

class Board:
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, size, num_ships, name):
        self.size = size
        self.num_ships = num_ships
        self.name = name


player_board = Board(size, num_ships, player_name)
print(player_board.name)

computer_board = Board(size, num_ships, "computer")
print(computer_board.name)
