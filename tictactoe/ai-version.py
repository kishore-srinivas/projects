from board import Board
import numpy as np

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

player = input("Would you like to be X or O? ")
if (player.lower() == "x"):
    computer = "O"
    player = "X"
elif (player.lower() == "o"):
    computer = "X"
    player = "O"
else:
    print("Invalid input")

def normalize(distribution):
    total = np.sum(distribution)
    for i in range(len(distribution)):
        distribution[i] = distribution[i] / total
    return distribution

def predictPlayersMove(board):
    dist = np.ones(board.getSize())
    for i in range(len(dist)):
        if (not board.get(i).isEmpty()):
            dist[i] = 0
    dist = normalize(dist)

    # if the player has only placed one square so far 
    if (len(board.getAllSquares(player)) == 1):
        print()

    # check for two in a row and predict that player will place the third one in that row
    for square in board.getAllSquares(player):
        mn = square.getMatchingNeighbors()
        for n in mn:
            direction = n[1].getOpposite()
            likelySquare = square.getNeighbor(direction)
            if likelySquare is not None:
                location = likelySquare[0].getLocation()
                dist[location] = dist[location] + 1
    # dist = normalize(dist)

    # check for two squares separated by a gap and predict the player will fill the gap
    for square in board.getAllSquares(player):
        en = square.getEmptyNeighbors()
        for n in en:
            direction = n[1]
            firstNeighbor = square.getNeighbor(direction)
            secondNeighbor = None
            if firstNeighbor is not None:
                secondNeighbor = firstNeighbor[0].getNeighbor(direction)
            if (secondNeighbor is not None) and (secondNeighbor[0].getValue() == player):
                location = firstNeighbor[0].getLocation()
                dist[location] = dist[location] + 0.5

    for i in range(len(dist)):
        if (not board.get(i).isEmpty()):
            dist[i] = 0
    # dist = normalize(dist)

    # print("playerDist:", dist)
    return dist

def nextBestMove(board):
    playerDist = predictPlayersMove(board)
    print("playerDist:", playerDist)

    computerDist = np.zeros(len(playerDist))
    # try to get the center square
    if board.get(4).getValue() == " ":
        computerDist[4] = 2
    # check for two in a row and return the third square
    for square in board.getAllSquares(computer):
        mn = square.getMatchingNeighbors()
        for n in mn:
            direction = n[1].getOpposite()
            winningSquare = square.getNeighbor(direction)
            if (winningSquare is not None) and (winningSquare[0].getValue() == " "):
                location = winningSquare[0].getLocation()
                print("winning location:", location)
                computerDist[location] = computerDist[location] + 1
    # try to get two in a row such that the third square is empty
    for square in board.getAllSquares(computer):
        en = square.getEmptyNeighbors()
        for n in en:
            direction = n[1]
            n2 = n[0].getNeighbor(direction)
            if (n2 is not None) and (n2[0].getValue() != player):
                location = n[0].getLocation()
                computerDist[location] = computerDist[location] + 0.5

    print("computerDist:", computerDist)
    dist = (playerDist + computerDist)
    print("dist:", dist)
    return np.where(dist == np.amax(dist))[0]

board = Board(3, 3)
gameOver = False

for x in range(board.getSize()):
    board.draw()
    if (x % 2 == 0):
        while True:
            try:
                place = int(input("Where would you like to place? "))
                while(not board.get(place).isEmpty()):
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
    else:
        print("computer's turn")
        while(not board.get(place).isEmpty()):
            place = nextBestMove(board)[0]
        print("place:", place)
        board.get(place).setValue(computer)
        if (board.isWinner(computer, place)):
            board.draw()
            print("<<<<< Computer has won! >>>>>")
            gameOver = True
    if (gameOver):
        break

