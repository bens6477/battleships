from parameters import *
from ship import *
from board import Board
import random
import os


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
        random_row = random.randrange(board_size)
        random_column = random.randrange(board_size)
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


def game_introduction():
    """
    Welcomes user to the game and requests their name.
    """
    print("Welcome to the game!\n")
    aircraft_carrier.print_ship()
    battleship.print_ship()
    cruiser.print_ship()
    submarine.print_ship()
    destroyer.print_ship()
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


def print_instructions():
    """
    Prints gameplay instructions to the user.
    """
    print("Here are the instructions...\n")


def print_boards():
    """
    Displays both player board in a clean and formatted structure.
    """
    clear_console()
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
            column_str = f" {computer.hidden_board[row][column]} "
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
        print("Enter your target in the form 'A4' or 'a4'.")
        guess = input("")
        print("")
        print("Checking validity of your target coordinates...")

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
            num_row = ord(guess[0].lower()) - 97
            num_column = int(guess[1])
            num_guess = (num_row, num_column)

            try:
                if num_guess in computer.previous_guesses:
                    raise ValueError(
                        f"You have already guessed the coordinates of '{guess}'"
                    )
            except ValueError as e:
                print(f"Invalid data: {e}, please choose coordinates in the the form 'A4' or 'a4'.\n")
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
    user_hit = ["user", is_guess_in_array(user_guess, computer.ship_locations, False, True), user_guess]
    computer_hit = ["computer", is_guess_in_array(computer_guess, user.ship_locations, False, True), computer_guess]

    return (user_hit, computer_hit)


def edit_board(hit_array, player):
    """
    Edits the game board depending on the outcome of the
    player guesses.
    """
    if player == user:
        guess = hit_array[0]
    else:
        guess = hit_array[1]
    guess_tuple = (guess[2][0], guess[2][1])
    if guess[1]:
        print(f"{guess[0]}: hit opponent\n")
        player.board[guess_tuple[0]][guess_tuple[1]] = "X"
    else:
        print(f"{guess[0]}: missed opponent\n")
        player.board[guess_tuple[0]][guess_tuple[1]] = "m"
    player.update_board()




def print_outcome(hit_array, player):
    """
    Prints the outcome from the guesses of both players.
    """
    if player == user:
        print("Your cannon fires...")
        if hit_array[0][1]:
            input("Direct hit! They took damage! Press Enter to continue.\n")
        else:
            input("Unlucky! You missed! Press Enter to continue.\n")
    else:
        print("Computer's cannon fires...")
        if hit_array[1][1]:
            input("Ouch! They hit our ship! Press Enter to continue.\n")
        else:
            input("Phew! They missed our ship, but stay alert! Press Enter to continue.\n")


def single_round():
    """
    Game script running a single blast attempt from each player.
    """
    print_instructions()
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
    clear_console()
    global user_name
    global user
    global computer
    user_name = game_introduction()
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
