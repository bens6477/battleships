import random
import copy
from .ship import BOARD_SIZE, ship_tuple


class Board():
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, name):
        self.name = name
        self.previous_guesses = []
        self.blank_symbol = '\33[96m' + '~' + '\33[0m'
        self.miss_symbol = '\33[93m' + '\u2300' + '\33[0m'
        self.hit_symbol = '\33[91m' + 'X' + '\33[0m'
        self.board = self.create_board()
        self.hidden_board = []
        self.ships_present = self.update_board()[0]
        self.ship_locations = self.update_board()[1]

    def create_board(self):
        """
        Creates a new, empty board for the player.
        """
        self.board = []
        for row in range(BOARD_SIZE):
            self.board.append([])
            for column in range(BOARD_SIZE):
                self.board[row].append(self.blank_symbol)

        return self.board

    def hide_ships(self):
        """
        Hides all ships from view but showing previously guessed
        hit and missed coordinates.
        """
        ship_symbols = ["A", "B", "C", "D", "S"]
        self.hidden_board = copy.deepcopy(self.board)
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.hidden_board[row][column] in ship_symbols:
                    self.hidden_board[row][column] = self.blank_symbol

        return self.hidden_board

    def is_ship_already_here(self, ship, direction, location):
        """
        Checks if ship div is already present at passed coordinates.
        Returns True if ship is present and False if not present.
        """
        if direction == "right":
            for div in range(ship.ship_length):
                cell = self.board[location[0]][div + location[1]]
                if cell != self.blank_symbol:
                    return True
            return False
        elif direction == "down":
            for div in range(ship.ship_length):
                cell = self.board[div + location[0]][location[1]]
                if cell != self.blank_symbol:
                    return True
            return False
        else:
            print("\nCheck not performed correctly\n")
            return True

    def generate_random_ship_location(self, ship):
        """
        Generates random ship location depending on the ship's
        placement range by randomising direction and valid index.
        """
        ship_present = True
        while ship_present:
            direction_array = ["right", "down"]
            random_direction = random.choice(direction_array)
            placement_array = [num for num in range(ship.placement_range + 1)]
            random_placement_index = random.choice(placement_array)
            random_index = random.randrange(BOARD_SIZE)
            if random_direction == "right":
                random_placement_tuple = (random_index, random_placement_index)
            elif random_direction == "down":
                random_placement_tuple = (random_placement_index, random_index)
            else:
                print("** Invalid input **")
            ship_present = (self.is_ship_already_here(ship, random_direction,
                            random_placement_tuple))

        return [random_direction, random_placement_tuple]

    def add_ship_to_board(self, ship, location, direction):
        """
        Add ship to player's board.
        """
        if direction == "right":
            for div in range(ship.ship_length):
                self.board[location[0]][div + location[1]] = ship.symbol
        elif direction == "down":
            for div in range(ship.ship_length):
                self.board[div + location[0]][location[1]] = ship.symbol
        else:
            print("\n *** Invalid direction ***\n")
        return self.board

    def randomise_all_ship_locations(self):
        """
        Randomises the location of all ships on the board.
        """
        for ship in ship_tuple:
            placed = False
            while not placed:
                random_location = self.generate_random_ship_location(ship)
                (self.add_ship_to_board(ship, random_location[1],
                                        random_location[0]))
                placed = True

    def update_board(self):
        """
        Updates board data including ship locations and
        ship types remaining.
        """
        ship_symbols = ["A", "B", "C", "D", "S"]
        ship_locations = []
        ships_present = []
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if self.board[row][column] in ship_symbols:
                    ship_locations.append((row, column))
                    ships_present.append(self.board[row][column])
        ships_present = list(dict.fromkeys(ships_present))
        self.ships_present = ships_present
        self.ship_locations = ship_locations

        return (ships_present, ship_locations)
