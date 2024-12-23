import math
import random
import time
import os


class Player:
    """
    Startup a player class.
    Each player in the game will be represented with X or O.
    get_move function will allow all players to get their next move.
    """
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class ComputerPlayer(Player):
    """
    This represents the computer"s move and choice.
    """
    def get_move(self, game):
        """
        Computer chooses a random cell from the board.
        """
        cell = random.choice(game.available_moves())
        return cell


class HumanPlayer(Player):
    """
    Specific class for the human player.
    """
    def get_move(self, game):
        """
        Checks if the value input is valid,
        checks if the cell on the board has already been used,
        if invalid or already used, will return an error.
        """
        valid_cell = False
        value = None
        while not valid_cell:
            cell = input(self.letter + "'s turn.Input (0-8) or 'q' to quit:\n")
            if cell.lower() == 'q':
                print("Player has quit the game.")
                exit()
            try:
                value = int(cell)
                if value not in game.available_moves():
                    raise ValueError
                valid_cell = True  # if no error found -> then must be valid
            except ValueError:
                print("Invalid cell. Try again a cell number from 0-8.")
        return value


def mockup_board():
    """
    Create board and ensure visibility throughout the board
    """
    num_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
    for row in num_board:
        print("| " + " | ".join(row) + " |")


class TicTacToe:
    """
    Class that explains the kind of game
    """
    def __init__(self):
        """
        Single list that represents a 3x3 board, each number = cell
        and keeps track of who wins
        """
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        """
        Group of three spaces row1 = 0,1,2 / row2 = 3,4,5 / row3 = 6,7,8
        and print a vertical line to seperate each row
        """
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        """
        Show the number correspondent to the cells and prints separators
        """
        print('')
        num_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in num_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        """
        Defines which moves are still available in a list of indeces
        """
        moves = []
        for (i, cell) in enumerate(self.board):
            if cell == " ":
                moves.append(i)
        return moves

    def empty_cells(self):
        """
        Returns True if there are empty cells in the board.
        """
        return " " in self.board

    def num_empty_cells(self):
        """
        Count how many empty cells are in the board
        """
        return self.board.count(" ")

    def make_move(self, cell, letter):
        """
        If the move is valid, then make the move and assign cell to letter
        then return True. If not valid, return False.
        Function also checks for the winner after player has made a move.
        """
        if self.board[cell] == " ":
            self.board[cell] = letter
            if self.winner(cell, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, cell, letter):
        """
        Checks if there is a winner.
        Checks for 3 in a row, column or diagonal.
        """
        # checks rows first
        row_index = math.floor(cell / 3)
        row = self.board[row_index*3: (row_index + 1)*3]
        # If all this is true or else comes out as false
        # checks if that letter is in 3 spots in a row
        if all([spot == letter for spot in row]):
            return True

        # If not true then we keep going
        # checks columns
        col_index = cell % 3
        column = [self.board[col_index+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # checks diagonals
        # checks if cell is an even number (0, 2, 4, 6, 8)
        # these are the only moves possible to win a diagonal
        if cell % 2 == 0:  # if it's even
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # left to right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # right to left
            if all([spot == letter for spot in diagonal2]):
                return True

        # if all this checks fail then there is no possible winner
        return False


def clear_screen(numlines=100):
    """
    Clears the console to simplify UI and clear visual clutter.
    numlines is an optional argument used only as a fall-back.
    """
    if os.name == "posix":
        # for OS => Unix / Linux / MacOS / BSD / etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        #  for OS => DOS / Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print('\n' * numlines)


def play(game, x_player, o_player, print_game=True):
    """
    Main function to play the game.
    Iterate while the game has empty cells.
    When winner is returned, breaks the loop.
    Returns the winner if there is one or None for a tie.
    """
    if print_game:
        print('')
        print("To select one of the cells:")
        print("Type the number in the spot of your choice!")
        print('')
        print("Board layout for your reference:")
        game.print_board_nums()
        print('')

    letter = "X"  # starting letter

    while game.empty_cells():
        # get the move from the correct player
        if letter == "O":
            cell = o_player.get_move(game)
        else:
            cell = x_player.get_move(game)

        # make a move
        if game.make_move(cell, letter):
            if print_game:
                print('')
                print('')
                print(f"{letter} makes a move to cell {cell}")
                game.print_board()
                print("")  # empty line to separate visually
                print("Reference board:")
                mockup_board()
                print("")  # empty line to separate visually

            if game.current_winner:
                if print_game:
                    print(letter + " wins! \n")
                    print('')
                return letter  # returns the winner of the game

            # after the move, alternate letters
            if letter == "X":
                letter = "O"
            else:
                letter = "X"

        # add pause to allow user to read computer moves
        time.sleep(0.8)

    if print_game:
        print("That's a tie!")
        return None


def explain_game():
    print("")
    print("Tic-tac-toe is a game in which two players take turns in drawing")
    print("either an 'O' or an 'X' in one square of a grid")
    print("consisting of nine squares.")
    print("The winner is the first player to get three of the same symbols")
    print("in a row, vertically, horizontally or diagonally.")
    print("")
    print("Press 'p' to play or 'q' to quit the game!")


def start_the_game():
    """
    Gives the user menu for information, start the game or quit.
    """
    x_player = HumanPlayer("X")
    o_player = ComputerPlayer("O")
    t = TicTacToe()
    print('')
    print("You have the X symbol assigned to you to play,")
    print("while the computer has the symbol O")
    print('')
    print("To continue, select a command with one of the following:")
    print("'p' to play the game")
    print("'r' to read the rules")
    print("'q' To quit the game")
    while True:
        user_choice = input().strip().lower()
        if user_choice == 'r':  # read the rules of the game
            clear_screen()
            explain_game()
        elif user_choice == 'p':  # play the game
            clear_screen()
            play(t, x_player, o_player, print_game=True)
            return
        elif user_choice == 'q':  # quit the game
            clear_screen()
            print('')
            print("Thank you for playing!")
            print('')
            break
        else:
            print("Wrong input. Press 'p' to play or 'r' to read the rules.")


def main():
    """
    Function that calls the start and end of game.
    """
    clear_screen()
    print('')
    print("Hello, Welcome to Tic-Tac-Toe!")
    name = ""
    while not name.strip():     # Loop until the user provides a non-empty name
        name = input("Enter a name: ").strip()
        if not name:
            print("Empty input. Please try again.")
    print("------------------")
    print('')
    print(f"Welcome {name}!")
    print('')
    print("Would you like to play Tic-Tac-Toe?")
    print("Enter 'y' for YES or 'n' for NO:")
    user_choice = input().strip().lower()
    if user_choice == 'y':
        clear_screen()
        start_the_game()
        while True:
            print("Would you like to play again?")
            print("Enter 'y' for YES or 'n' for NO:")
            user_choice = input().strip().lower()
            if user_choice == 'y':
                clear_screen()
                start_the_game()
            elif user_choice == 'n':
                clear_screen()
                print("Thank you for playing Tic-Tac-Toe!")
                break
            else:
                print("Invalid command. Press 'y' to start and 'n' to quit.")
    elif user_choice == 'n':
        clear_screen()
        print("Thank you for playing!")
        print("Restart the game:")
        print("Press Run program above the terminal window.")
    else:
        print("Invalid command. Press 'y' to start and 'n' to quit.")


if __name__ == '__main__':
    while True:
        main()
