from parameters import board_size

class Ship():
    """
    Creates a ship with specified length and symbol depending on the ship
    type.
    """
    def __init__(self, ship_type, ship_length, symbol):
        self.ship_type = ship_type
        self.ship_length = ship_length
        self.symbol = symbol
        self.placement_range = board_size - self.ship_length

    def print_ship(self):
        """
        Prints an instance of the ship passed into the function.
        """
        print(f"{self.ship_type} ({self.ship_length}):  " + f" {self.symbol}" * self.ship_length)


aircraft_carrier = Ship("Aircraft Carrier", 5, "A")
battleship = Ship("Battleship", 4, "B")
cruiser = Ship("Cruiser", 3, "C")
submarine = Ship("Submarine", 3, "S")
destroyer = Ship("Destroyer", 2, "D")
ship_tuple = (aircraft_carrier, battleship, cruiser, submarine, destroyer)
