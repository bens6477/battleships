import random

scores = {"computer": 0, "user": 0}

board_size = 5
num_ships = 5
user_name = "Ben"


def generate_random_guess():
    """
    Returns random target coordinates for as a tuple.
    """
    random_row = random.randrange(board_size)
    random_column = random.randrange(board_size)
    random_pair = (random_row, random_column)
    return random_pair


def is_guess_in_array(current_guess, location_array, append):
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
        print("Location in array")
        return True


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
            random_pair = generate_random_guess()
            valid_location = is_guess_in_array(random_pair, ship_locations, True)            
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


user = Board(board_size, num_ships, user_name)
computer = Board(board_size, num_ships, "computer")


def print_instructions():
    """
    Prints gameplay instructions to the user.
    """
    print("Here are the instructions...")


def print_boards():
    """
    Displays both player board in a clean and formatted structure.
    """
    board_str = "   Your Board              Enemy's Board\n"
    board_str += "   0  1  2  3  4           0  1  2  3  4\n"
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

    return board_str


def request_user_guess():
    """
    Requests user to input guess and returns guess.
    """
    print("Enter your target, E.G. of the form A4.")
    current_guess = input()

    return current_guess


def check_guess_validity(guess):
    """
    Checks user guess is of valid format for processing.
    Throws relevant errors if data is in invalid format.
    """
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
        print("Valid input")


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
    user_hit = ["user", is_guess_in_array(user_guess, computer.ship_locations, False), user_guess]
    computer_hit = ["computer", is_guess_in_array(computer_guess, user.ship_locations, False), computer_guess]

    return (user_hit, computer_hit)


def edit_board(hit_array):
    """
    Edits the game board depending on the outcome of the
    player guesses.
    """
    for guess in hit_array:
        if guess[0] == "user":
            opponent = user
        else:
            opponent = computer
        guess_tuple = (guess[2][0], guess[2][1])
        print(guess_tuple)
        if guess[1]:
            print("hit")
            opponent.board[guess_tuple[0]][guess_tuple[1]] = "X"
        else:
            print("miss")
            opponent.board[guess_tuple[0]][guess_tuple[1]] = "m"


def main():
    """
    Main game function.
    """
    print("Welcome to the game!")
    print_instructions()
    game_boards = print_boards()
    print(game_boards)
    current_guess = request_user_guess()
    check_guess_validity(current_guess)
    user_guess = convert_guess(current_guess)
    computer_guess = generate_random_guess()
    print(user.ship_locations)
    print(computer.ship_locations)
    hit_array = check_player_guesses(user_guess, computer_guess)
    print(hit_array)
    edit_board(hit_array)
    game_boards = print_boards()
    print(game_boards)


main()
