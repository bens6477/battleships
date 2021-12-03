scores = {"computer": 0, "player": 0}
print(scores)

class Board:
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, size, num_ships, name):
        self.size = size
        self.num_ships = num_ships
        self.name = name