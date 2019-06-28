from board import board, drawBoard, isWinner

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

gameOver = False
for x in range(len(board)):
    drawBoard()
    player = "X" if x % 2 == 0 else "O"
    print("You are player", player)
    while True:
        try:
            place = int(input("Where would you like to place? "))
            while(board[place].getValue() == "X" or board[place].getValue() == "O"):
                place = int(input("That square is already taken. Select another square: "))
            board[place].setValue(player)
            print("===================")
            if (isWinner(player, place)):
                drawBoard()
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
    drawBoard()
    print("Good game! That was a draw.")
    
