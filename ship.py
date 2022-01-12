class Ship():
    """
    Creates a ship with specified length and symbol depending on the ship
    type.
    """
    def __init__(self, ship_type, ship_length, symbol, board_size):
        self.ship_type = ship_type
        self.ship_length = ship_length
        self.symbol = symbol
        self.placement_range = board_size - self.ship_length

    def print_ship(self):
        """
        Prints an instance of the ship passed into the function.
        """
        print(f"{self.ship_type} ({self.ship_length}):  " + f" {self.symbol}" * self.ship_length)
