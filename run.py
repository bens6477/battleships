import random


board_size = 5
num_ships = 5

class Mixin:
    """
    Sets parameters that can be used in other classes.
    """
    def test_function(self, ship):
        print(ship.ship_type, self.board)


def generate_random_guess():
    """
    Returns random target coordinates for as a tuple.
    """
    random_row = random.randrange(board_size)
    random_column = random.randrange(board_size)
    random_pair = (random_row, random_column)
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
        print("Location in array")
        return True


class Ship(Mixin):
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
aircraft_carrier.print_ship()
battleship.print_ship()
cruiser.print_ship()
submarine.print_ship()
destroyer.print_ship()



class Board(Mixin):
    """
    Main board class. Sets all parameters for each player's board.
    """
    def __init__(self, name):
        self.name = name
        self.board = self.create_board()
        # self.ship_locations = self.assign_ship_locations()
        self.styled_board = self.display_board()

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

    def assign_ship_locations(self):
        """
        Assigns random locations for ships on the player's board.
        """
        ship_locations = []
        ships = 0
        while ships < num_ships:
            random_pair = generate_random_guess()
            valid_location = is_guess_in_array(random_pair, ship_locations, True, False)            
            if not valid_location:
                self.board[random_pair[0]][random_pair[1]] = "S"
                ships += 1

        return ship_locations

    def display_board(self):
        """
        Displays player board in a clean and formatted structure.
        """
        board_str = ""
        for row in range(board_size):
            row_str = ""
            for column in range(board_size):
                column_str = f" {self.board[row][column]} "
                if column == board_size - 1:
                    column_str += "\n"
                row_str += column_str
            board_str += row_str

        return board_str


def game_introduction():
    """
    Welcomes user to the game and requests their name.
    """
    print("Welcome to the game!\n")
    print("Enter your name:")
    user_name = input()
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


print(user.test_function(destroyer))

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
    board_str += " " * (15 - len(user_name))
    board_str += "Enemy's Board:\n\n"
    board_str += "   "
    for index in range(board_size):
        board_str += f"{index}  "
    board_str += " " * 9
    for index in range(board_size):
        board_str += f"{index}  "
    board_str += "\n"
    for row in range(board_size):
        row_str = f"{chr(65 + row)} "
        for column in range(board_size):
            column_str = f" {user.board[row][column]} "
            row_str += column_str
        row_str += f"   |   {chr(65 + row)} "
        for column in range(board_size):
            column_str = f" {computer.board[row][column]} "
            if column == board_size - 1:
                column_str += "\n"
            row_str += column_str
        board_str += row_str
    print(board_str)


def request_user_guess():
    """
    Requests user to input guess and returns guess.
    """
    print("Enter your target, E.G. of the form A4.")
    current_guess = input()
    print("")

    return current_guess


def check_guess_validity(guess):
    """
    Checks user guess is of valid format for processing.
    Throws relevant errors if data is in invalid format.
    """
    print("Checking validity of your target coordinates...")
    try:
        if not guess[0].isalpha():
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


def convert_guess(guess):
    """
    Converts user input string into respective indices on board array.
    """
    user_row = ord(guess[0].lower()) - 97
    user_column = int(guess[1])
    user_guess = (user_row, user_column)

    return user_guess


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


def single_blast():
    """
    Game script running a single blast attempt from each player.
    """
    print_instructions()
    print_boards()
    current_guess = request_user_guess()
    check_guess_validity(current_guess)
    user_guess = convert_guess(current_guess)
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
        print("User ships remaining: ", len(user.ship_locations))
        print("Computer ships remaining: ", len(computer.ship_locations), "\n")
        if len(user.ship_locations) < 5 and len(computer.ship_locations) < 5:
            print("Its a draw! You both struck out on this round!\n")
            return False
        elif len(computer.ship_locations) < 5:
            print("Congratulations! You win!\n")
            print("Game over\n")
            return False
        elif len(user.ship_locations) < 5:
            print("Unlucky! You lose!\n")
            print("Game over\n")
            return False
        else:
            single_blast()


def play_again():
    """
    Asks user if they would like to play again and restarts the game.
    """
    print("Would you like to play again? Enter 'Y' to play again or 'N' to quit.")
    another_game = input()
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
    single_blast()
    check_remaining_ships()
    play_again()


def is_ship_already_here(player, ship, direction, location):
    """
    Checks if ship div is already present at passed coordinates.
    """
    print_boards()
    print("\nChecking if ship present\n")
    print(location)
    if direction == "right":
        for div in range(ship.ship_length):
            cell = player.board[location[0]][div + location[1]]
            if cell != '-':
                print("Ship here")
                return True
        print("No ships present")
        return False
    elif direction == "down":
        for div in range(ship.ship_length):
            cell = player.board[div + location[0]][location[1]]
            if cell != '-':
                print("Ship here")
                return True
        print("No ships present")
        return False
    else:
        print("\nCheck not performed correctly\n")
        return True

# is_ship_already_here(user, (0, 0))


def generate_random_ship_location(player, ship):
    """
    Generates random ship location depending on the ship's
    placement range by randomising direction and valid index.
    """
    ship_present = True
    while ship_present:
        direction_array = ["right", "down"]
        random_direction = random.choice(direction_array)
        print("placement_range: ", ship.placement_range)
        placement_array = [num for num in range(ship.placement_range + 1)]
        print("placement_array: ", placement_array)
        random_placement_index = random.choice(placement_array)
        random_index = random.randrange(board_size)
        if random_direction == "right":
            random_placement_tuple = (random_index, random_placement_index)
        elif random_direction == "down":
            random_placement_tuple = (random_placement_index, random_index)
        else:
            print("** Invalid input **")
        print([random_direction, random_placement_tuple])
        ship_present = is_ship_already_here(player, ship, random_direction, random_placement_tuple)
    print("Submitted data: ", [random_direction, random_placement_tuple])

    return [random_direction, random_placement_tuple]


def add_ship_to_board(player, ship, location, direction):
    """
    Add ship to player's board.
    """
    if direction == "right":
        for div in range(ship.ship_length):
            player.board[location[0]][div + location[1]] = ship.symbol
    elif direction == "down":
        for div in range(ship.ship_length):
            player.board[div + location[0]][location[1]] = ship.symbol
    else:
        print("\n *** Invalid direction ***\n")
    return player.board


# generate_random_ship_location(destroyer)


def randomise_all_ship_locations(player):
    """
    Randomises the location of all ships on the board.
    """
    for ship in ship_tuple:
        print(ship.ship_type)
        placed = False
        while not placed:
            random_location = generate_random_ship_location(player, ship)
            print(random_location[1])
            add_ship_to_board(player, ship, random_location[1], random_location[0])
            # Add logic to check if ship div already here
            placed = True
    print_boards()


randomise_all_ship_locations(user)
randomise_all_ship_locations(computer)


def input_ship_location(player, ship):
    """
    Request an input for the location and direction of the passed ship.
    """
    ship_present = True
    while ship_present:
        print(f"\n{ship.ship_type} ({ship.ship_length}):  " + f" {ship.symbol}" * ship.ship_length)
        print(f"Input the coordinates for bow of your {ship.ship_type}. Enter in the form A1.")
        location_input = input()
        location = convert_guess(location_input)
        print("")
        print(f"Input direction of you {ship.ship_type} from bow to stern (front to back). Enter (r)ight or (d)own.")
        direction_input = input()
        print("")
        if ord(direction_input[0].lower()) == 114:
            print(f"Ship placed horizontally across starting from {location}\n")
            direction = "right"
        elif ord(direction_input[0].lower()) == 100:
            print(f"Ship placed vertically downwards starting from {location}\n")
            direction = "down"
        else:
            print("\n *** Invalid direction ***\n")
        print("")
        ship_present = is_ship_already_here(player, ship, direction, location)
        # Stil need to run through input validation
    add_ship_to_board(player, ship, location, direction)
    print_boards()

    return (location, direction)


def user_manual_ship_input():
    """
    Single functions running the functions for user to place all five ships
    on their board.
    """
    input_ship_location(user, aircraft_carrier)
    input_ship_location(user, battleship)
    input_ship_location(user, cruiser)
    input_ship_location(user, submarine)
    input_ship_location(user, destroyer)


user_manual_ship_input()

# Quick placement:
# add_ship_to_board(user, aircraft_carrier, (0, 0), "down")
# add_ship_to_board(user, battleship, (1, 1), "down")
# add_ship_to_board(user, cruiser, (2, 2), "down")
# add_ship_to_board(user, destroyer, (3, 3), "down")
# add_ship_to_board(user, submarine, (2, 4), "down")



# main()
