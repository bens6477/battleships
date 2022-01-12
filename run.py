from ship import Ship
import random

board_size = 5
num_ships = 5

def generate_random_guess():
    """
    Returns random target coordinates as a tuple.
    """
    valid_guess = False
    while not valid_guess:
        random_row = random.randrange(board_size)
        random_column = random.randrange(board_size)
        random_pair = (random_row, random_column)

        if random_pair not in user.previous_guesses:
            print("Fresh guess")
            valid_guess = True
    user.previous_guesses.append(random_pair)

    return random_pair


def is_guess_in_array(current_guess, location_array, append, delete):
    """
    Checks if current coordinates have already been selected
    for function of choice.
    Appends cuurent guess to guess array if it has not been
    selected previously.
    """
    if current_guess not in location_array:
        if append:
            location_array.append(current_guess)
        return False
    else:
        if delete:
            location_array.remove(current_guess)
        return True


aircraft_carrier = Ship("Aircraft Carrier", 5, "A", board_size)
battleship = Ship("Battleship", 4, "B", board_size)
cruiser = Ship("Cruiser", 3, "C", board_size)
submarine = Ship("Submarine", 3, "S", board_size)
destroyer = Ship("Destroyer", 2, "D", board_size)


ship_tuple = (aircraft_carrier, battleship, cruiser, submarine, destroyer)
aircraft_carrier.print_ship()
battleship.print_ship()
cruiser.print_ship()
submarine.print_ship()
destroyer.print_ship()



class Board():
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, name):
        self.name = name
        self.previous_guesses = []
        self.board = self.create_board()
        self.ships_present = self.update_board()[0]
        self.ship_locations = self.update_board()[1]

    def create_board(self):
        """
        Creates a new, empty board for the player.
        """
        self.board = []
        for row in range(board_size):
            self.board.append([])
            for column in range(board_size):
                self.board[row].append('-')

        return self.board

    
    def is_ship_already_here(self, ship, direction, location):
        """
        Checks if ship div is already present at passed coordinates.
        Returns True if ship is present and False if not present.
        """
        if direction == "right":
            for div in range(ship.ship_length):
                cell = self.board[location[0]][div + location[1]]
                if cell != '-':
                    return True
            return False
        elif direction == "down":
            for div in range(ship.ship_length):
                cell = self.board[div + location[0]][location[1]]
                if cell != '-':
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
            random_index = random.randrange(board_size)
            if random_direction == "right":
                random_placement_tuple = (random_index, random_placement_index)
            elif random_direction == "down":
                random_placement_tuple = (random_placement_index, random_index)
            else:
                print("** Invalid input **")
            ship_present = self.is_ship_already_here(ship, random_direction, random_placement_tuple)

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
                self.add_ship_to_board(ship, random_location[1], random_location[0])
                placed = True

    
    def update_board(self):
        """
        Updates board data including ship locations and
        ship types remaining.
        """
        ship_symbols = ["A", "B", "C", "D", "S"]
        ship_locations = []
        ships_present = []
        for row in range(board_size):
            for column in range(board_size):
                if self.board[row][column] in ship_symbols:
                    ship_locations.append((row, column))
                    ships_present.append(self.board[row][column])
        ships_present = list(dict.fromkeys(ships_present))
        self.ships_present = ships_present
        self.ship_locations = ship_locations

        return (ships_present, ship_locations)


def game_introduction():
    """
    Welcomes user to the game and requests their name.
    """
    print("Welcome to the game!\n")
    print("Enter your name:")
    user_name = input("")
    print("")

    return user_name


def reset_board():
    """
    Re-initialises boards ready for the start of a new game 
    """
    user_copy = Board(user_name)
    computer_copy = Board("computer")
    user = user_copy
    computer = computer_copy

    return [user, computer]


user_name = ""
players = reset_board()
user = players[0]
computer = players[1]



def print_instructions():
    """
    Prints gameplay instructions to the user.
    """
    print("Here are the instructions...\n")


def print_boards():
    """
    Displays both player board in a clean and formatted structure.
    """
    board_str = f"{user_name}'s Board:"
    board_str += " " * (17 - len(user_name))
    board_str += "Enemy's Board:\n\n"
    board_str += " " * 4
    for index in range(board_size):
        board_str += f"{index}  "
    board_str += " " * 11
    for index in range(board_size):
        board_str += f"{index}  "
    board_str += "\n"
    board_str += "  \u2198 "
    board_str += "   " * board_size
    board_str += " " * 11
    board_str += "   " * (board_size)
    board_str += "\n"
    for row in range(board_size):
        row_str = f"{chr(65 + row)}  "
        for column in range(board_size):
            column_str = f" {user.board[row][column]} "
            row_str += column_str
        row_str += f"   |   {chr(65 + row)}   "
        for column in range(board_size):
            column_str = f" {computer.board[row][column]} "
            if column == board_size - 1:
                column_str += "\n"
            row_str += column_str
        board_str += row_str
    print(board_str)


def get_valid_guess():
    """
    Request coordinates from user and checks it is of 
    valid format for processing.
    Throws relevant errors if data is in invalid format.
    """
    valid_guess = False
    while not valid_guess:
        print("Enter your target, E.G. of the form A4.")
        guess = input("")
        print("")
        print("Checking validity of your target coordinates...")

        player = computer

        num_row = ord(guess[0].lower()) - 97
        num_column = int(guess[1])
        num_guess = (num_row, num_column)

        try:
            if num_guess in player.previous_guesses:
                raise ValueError(
                    f"You have already guessed the coordinates of '{guess}'"
                )
            elif not guess[0].isalpha():
                raise ValueError(
                    f"First character is not a letter in your guess '{guess}'"
                )
            elif not guess[1].isdigit():
                raise ValueError(
                    f"Second character is not a decimal number in your guess '{guess}'"
                )
            elif ord(guess[0].lower()) < 97 or ord(guess[0].lower()) > (96 + board_size):
                raise ValueError(
                    f"First character is out of bounds of the board in your guess '{guess}'. It should be a letter between A and {chr(64 + board_size)}"
                )
            elif (int(guess[1]) > board_size - 1):
                raise ValueError(
                    f"Second character is out of bounds of the board in your guess '{guess}'"
                )
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
        else:
            print("Valid input\n")
            player.previous_guesses.append(num_guess)
            valid_guess = True
    print("Escaped while loop")
    return num_guess


def check_player_guesses(user_guess, computer_guess):
    """
    Checks if the guesses of both players match ship locations of
    their opponent.
    """
    user_hit = ["user", is_guess_in_array(user_guess, computer.ship_locations, False, True), user_guess]
    computer_hit = ["computer", is_guess_in_array(computer_guess, user.ship_locations, False, True), computer_guess]

    return (user_hit, computer_hit)


def edit_board(hit_array):
    """
    Edits the game board depending on the outcome of the
    player guesses.
    """
    for guess in hit_array:
        if guess[0] == "user":
            opponent = computer
        else:
            opponent = user
        guess_tuple = (guess[2][0], guess[2][1])
        if guess[1]:
            print(f"{guess[0]}: hit opponent\n")
            opponent.board[guess_tuple[0]][guess_tuple[1]] = "X"
        else:
            print(f"{guess[0]}: missed opponent\n")
            opponent.board[guess_tuple[0]][guess_tuple[1]] = "m"
    user.update_board()
    computer.update_board()


def print_outcome(hit_array):
    """
    Prints the outcome from the guesses of both players.
    """
    print("Your cannon fires...")
    if hit_array[0][1]:
        print("Direct hit! They took damage!\n")
    else:
        print("Unlucky! You missed!\n")
    print("Computer's cannon fires...")
    if hit_array[1][1]:
        print("Ouch! They hit our ship!\n")
    else:
        print("Phew! They missed our ship, but stay alert!\n")


def single_round():
    """
    Game script running a single blast attempt from each player.
    """
    print_instructions()
    print_boards()
    user_guess = get_valid_guess()    
    computer_guess = generate_random_guess()
    hit_array = check_player_guesses(user_guess, computer_guess)
    edit_board(hit_array)
    print_boards()
    print_outcome(hit_array)


def check_remaining_ships():
    """
    Checks the number of ships remaining for each player
    and determines if the game is finished or still active.
    """
    while True:
        user_ships = user.ships_present
        computer_ships = computer.ships_present
        print("User ships remaining: ", len(user_ships))
        print("Computer ships remaining: ", len(computer_ships), "\n")
        if len(user_ships) < 5 and len(computer_ships) < 5:
            print("Its a draw! You both struck out on this round!\n")
            return False
        elif len(computer_ships) < 5:
            print("Congratulations! You win!\n")
            print("Game over\n")
            return False
        elif len(user_ships) < 5:
            print("Unlucky! You lose!\n")
            print("Game over\n")
            return False
        else:
            single_round()


def play_again():
    """
    Asks user if they would like to play again and restarts the game.
    """
    print("Would you like to play again? Enter 'Y' to play again or 'N' to quit.")
    another_game = input("")
    print("")

    if ord(another_game.lower()) == 121:
        print("Playing again...")
        print("-" * 35, "\n")
        main()
    elif ord(another_game.lower()) == 110:
        print("Ending game...\n")
        print("-" * 35, "\n")
    else:
        print("Invalid input\n")


def main():
    """
    Main game function.
    """
    global user_name
    global user
    global computer
    user_name = game_introduction()
    players = reset_board()
    user = players[0]
    computer = players[1]

    user.randomise_all_ship_locations()
    computer.randomise_all_ship_locations()

    user.update_board()
    computer.update_board()

    single_round()
    check_remaining_ships()

    play_again()


main()
