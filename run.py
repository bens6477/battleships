import random
import os
from classes.ship import BOARD_SIZE, aircraft_carrier, battleship, cruiser, destroyer, submarine
from classes.board import Board


def colour_text(text, colour):
    """
    Wraps text in escape characters for colouring
    terminal text.
    """
    if colour == "green":
        colour_code = '\33[92m'
    elif colour == "red":
        colour_code = '\33[91m'
    elif colour == "yellow":
        colour_code = '\33[93m'
    elif colour == "blue":
        colour_code = '\33[96m'
    string = colour_code + text + '\33[0m'
    return string


# Code taken from https://www.delftstack.com/howto/python/python-clear-console/
def clear_console():
    """
    Clears console of all text.
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def generate_random_guess():
    """
    Returns random target coordinates as a tuple.
    """
    valid_guess = False
    while not valid_guess:
        random_row = random.randrange(BOARD_SIZE)
        random_column = random.randrange(BOARD_SIZE)
        random_pair = (random_row, random_column)

        if random_pair not in user.previous_guesses:
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


def get_user_name():
    """
    Requests and checks validity of user name.
    """
    clear_console()
    valid_name = False
    while not valid_name:
        print(colour_text("Enter your name:", "green"))
        name_input = input("")
        try:
            if len(name_input) == 0:
                raise ValueError(
                    "Name cannot be blank"
                )
            elif len(name_input) > 10:
                raise ValueError(
                    "Name too long. Provide a shorter name"
                )
            elif name_input.lower() == "computer":
                raise ValueError(
                    "Name cannot be the same as the Computer"
                )
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
        else:
            valid_name = True
        
    return name_input


def game_introduction():
    """
    Welcomes user to the game and requests their name.
    """
    print("Welcome to Battleships!\n")
    print("""Both players have a fleet of 5 ships, each occupying a certain
number of cell blocks, as shown below.""")
    print(f"Ships are randomly placed on a {BOARD_SIZE}x{BOARD_SIZE} grid.\n")
    aircraft_carrier.print_ship()
    battleship.print_ship()
    cruiser.print_ship()
    submarine.print_ship()
    destroyer.print_ship()
    input(colour_text("\nPress Enter to continue.\n", "blue"))
    clear_console()
    print("""Players choose coordinates each round to fire a cannon at their
opponent's ship.""")
    print("""The symbols below indicate whether the cannonball hits or misses a
ship.\n""")
    print(colour_text("X", "red") + " - Direct hit")
    print(colour_text("\u2300", "yellow") + " - Shot missed")
    print(colour_text("~", "blue") + " - Blank/hidden cell")
    print("""\nDestroy the computer's fleet before your ships are
destroyed to win the battle.\n""")
    input(colour_text("Press Enter to continue.\n", "blue"))


def reset_board():
    """
    Re-initialises boards ready for the start of a new game.
    """
    user_copy = Board(user_name)
    computer_copy = Board("computer")
    user = user_copy
    computer = computer_copy

    return [user, computer]


def print_boards():
    """
    Displays both player board in a clean and formatted structure.
    """
    clear_console()
    board_str = "\n" + " " * 10 + f"{user_name}'s Board"
    board_str += " " * (24 - len(user_name))
    board_str += "Computer's Board\n\n"
    board_str += " " * 14
    for index in range(BOARD_SIZE):
        board_str += f"{index}  "
    board_str += " " * 10
    for index in range(BOARD_SIZE):
        board_str += f"{index}  "
    board_str += "\n"
    board_str += " " * 12 + "\u2198 "
    board_str += "   " * BOARD_SIZE
    board_str += " " * 8 + "\u2198"
    board_str += "   " * (BOARD_SIZE)
    board_str += "\n"
    for row in range(BOARD_SIZE):
        row_str = " " * 10 + f"{chr(65 + row)}  "
        for column in range(BOARD_SIZE):
            column_str = f" {user.board[row][column]} "
            row_str += column_str
        row_str += " " * 7 + f"{chr(65 + row)}  "
        for column in range(BOARD_SIZE):
            column_str = f" {computer.hidden_board[row][column]} "
            if column == BOARD_SIZE - 1:
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
        print(colour_text("Enter your target in the form 'A4' or 'a4':",
              "green"))
        guess = input("")
        try:
            if len(guess) != 2:
                raise ValueError(
                    f"Two characters were not provided in your guess '{guess}'"
                )
            elif not guess[0].isalpha():
                raise ValueError(
                    f"First character is not a letter in your guess '{guess}'"
                )
            elif not guess[1].isdigit():
                raise ValueError(
                    f"""Second character is not a decimal number in your guess
'{guess}'"""
                )
            elif (ord(guess[0].lower()) < 97 or
                    ord(guess[0].lower()) > (96 + BOARD_SIZE)):
                raise ValueError(
                    f"""First character is out of bounds of the board in your
guess '{guess}'. It should be a letter between A and {chr(64 + BOARD_SIZE)}"""
                )
            elif (int(guess[1]) > BOARD_SIZE - 1):
                raise ValueError(
                    f"""Second character is out of bounds of the board in your
guess '{guess}'"""
                )
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
        else:
            num_row = ord(guess[0].lower()) - 97
            num_column = int(guess[1])
            num_guess = (num_row, num_column)

            try:
                if num_guess in computer.previous_guesses:
                    raise ValueError(
                        f"""You have already guessed the coordinates of
'{guess}'"""
                    )
            except ValueError as e:
                print(f"""Invalid data: {e}, please choose coordinates in the
form 'A4' or 'a4'.\n""")
            else:
                print("Valid input\n")
                computer.previous_guesses.append(num_guess)
                valid_guess = True

    return num_guess


def check_player_guesses(user_guess, computer_guess):
    """
    Checks if the guesses of both players match ship locations of
    their opponent.
    """
    user_check = is_guess_in_array(user_guess, computer.ship_locations,
                                   False, True)
    computer_check = is_guess_in_array(computer_guess, user.ship_locations,
                                       False, True)
    user_hit = ["user", user_check, user_guess]
    computer_hit = ["computer", computer_check, computer_guess]

    return (user_hit, computer_hit)


def edit_board(hit_array, player):
    """
    Edits the game board depending on the outcome of the
    player guesses.
    """
    if player == user:
        guess = hit_array[1]
    else:
        guess = hit_array[0]
    guess_tuple = (guess[2][0], guess[2][1])
    if guess[1]:
        print(f"{guess[0]}: hit opponent\n")
        player.board[guess_tuple[0]][guess_tuple[1]] = player.hit_symbol
    else:
        print(f"{guess[0]}: missed opponent\n")
        player.board[guess_tuple[0]][guess_tuple[1]] = player.miss_symbol
    player.update_board()


def print_outcome(hit_array, player):
    """
    Prints the outcome from the guesses of both players.
    """
    if player == user:
        print("Your cannon fires...")
        if hit_array[0][1]:
            input(colour_text("Direct hit! ", "red")
                  + colour_text("Press Enter to continue.\n", "blue"))
        else:
            input(colour_text("Splash! You missed! ", "yellow")
                  + colour_text("Press Enter to continue.\n", "blue"))
    else:
        print("Computer's cannon fires...")
        if hit_array[1][1]:
            input(colour_text("Ouch! Direct hit! ", "red")
                  + colour_text("Press Enter to continue.\n", "blue"))
        else:
            input(colour_text("Splash! They missed, but stay alert! ",
                  "yellow")
                  + colour_text("Press Enter to continue.\n", "blue"))


def single_round():
    """
    Game script running a single blast attempt from each player.
    """
    print_boards()
    user_guess = get_valid_guess()
    computer_guess = generate_random_guess()
    hit_array = check_player_guesses(user_guess, computer_guess)
    edit_board(hit_array, computer)
    computer.hide_ships()
    print_boards()
    print_outcome(hit_array, user)
    edit_board(hit_array, user)
    print_boards()
    print_outcome(hit_array, computer)


def check_remaining_ships():
    """
    Checks the number of ships remaining for each player
    and determines if the game is finished or still active.
    """
    
    ships_remaining = True
    while ships_remaining:
        clear_console()
        print_boards()
        user_ships = user.ships_present
        computer_ships = computer.ships_present
        print(f"{user_name}'s ships remaining: ", len(user_ships))
        print("Computer's ships remaining: ", len(computer_ships), "\n")

        if len(user_ships) < 5 and len(computer_ships) < 5:
            print(colour_text("""Its a draw! You both destroyed your
opponent's last ship on this round!\n""", "yellow"))
            ships_remaining = False
        elif len(computer_ships) < 5:
            print(colour_text("""Congratulations! You destroyed all of the computer's
ships, you win!\n""", "green"))
            ships_remaining = False
        elif len(user_ships) < 5:
            print(colour_text("""Unlucky! All of your ships have been destroyed, you lose.
\n, you win!\n""", "red"))
            ships_remaining = False
        else:
            input(colour_text("Press Enter to continue.\n", "blue"))
            single_round()


def play_again():
    """
    Asks user if they would like to play again and restarts the game.
    """
    valid_input = False
    valid_options = (110, 121)
    while not valid_input:
        print('\33[92m' + """Would you like to play again? Enter 'Y' to play again or 'N' to
quit:""" + '\33[0m')
        another_game = input("")
        try:
            if len(another_game) == 0:
                raise ValueError(
                    "Input cannot be blank"
                )
            elif len(another_game) > 1:
                raise ValueError(
                    "Input too long"
                )
            elif ord(another_game.lower()) not in valid_options:
                print(ord(another_game.lower()))
                raise ValueError(
                    "Y/N input not given"
                )
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
        else:
            if ord(another_game.lower()) == 121:
                print("-" * 35, "\n")
                main()
            else:
                print("Game finished.\n")
                print("-" * 35, "\n")
            valid_input = True


def main():
    """
    Main game function.
    """
    clear_console()
    global user_name
    global user
    global computer
    game_introduction()
    user_name = get_user_name()
    players = reset_board()
    user = players[0]
    computer = players[1]
    user.randomise_all_ship_locations()
    computer.randomise_all_ship_locations()
    computer.hide_ships()
    user.update_board()
    computer.update_board()
    single_round()
    check_remaining_ships()
    play_again()


user_name = ""
players = reset_board()
user = players[0]
computer = players[1]

main()
