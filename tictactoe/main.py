from board import Board

print("Welcome to TicTacToe!")
print("These are the locations on the board:")
print("  0 | 1 | 2")
print(" -----------")
print("  3 | 4 | 5")
print(" -----------")
print("  6 | 7 | 8")
print("Type the number of a square to place your symbol in that square\n")
input("Press <ENTER> when you are ready to play")
print("=========================================\n")

board = Board(3, 3)

gameOver = False
for x in range(board.getSize()):
    board.draw()
    player = "X" if x % 2 == 0 else "O"
    print("You are player", player)
    while True:
        try:
            place = int(input("Where would you like to place? "))
            while(board.get(place).getValue() == "X" or board.get(place).getValue() == "O"):
                place = int(input("That square is already taken. Select another square: "))
            board.get(place).setValue(player)
            print("===================")
            if (board.isWinner(player, place)):
                board.draw()
                print("<<<<< Congratulations player", player, "you have won! >>>>>")
                gameOver = True
            break
        except ValueError:
            print("Enter a number between 0 and 8")
        except IndexError:
            print("Enter a number between 0 and 8")
    if (gameOver):
        break

if (not gameOver):
    board.draw()
    print("Good game! That was a draw.")
    
