import tkinter as tk
from board import Board

m = tk.Tk()
m.title('Tic Tac Toe')
m.geometry("600x500")
squares = []

back = tk.Frame(m)
back.place(x=0, y=0, relwidth=1, relheight=1)

text = tk.StringVar()

def update(newText):
    text.set(newText)

board = Board(3, 3)

i = 0
def onClick(place):
    global i
    player = "X" if (i % 2 == 0) else "O"
    while(board.get(place).getValue() == "X" or board.get(place).getValue() == "O"):
        return True
    board.get(place).setValue(player)
    squares[place]['text'] = board.get(place).getValue()
    i = i + 1
    if (board.isWinner(player, place)):
        print("<<<<< Congratulations player", player, "you have won! >>>>>")

squares.append(tk.Button(m, text=board.get(0).getValue(), width=20, height=10, command=lambda:onClick(0)))
squares.append(tk.Button(m, text=board.get(1).getValue(), width=20, height=10, command=lambda:onClick(1)))
squares.append(tk.Button(m, text=board.get(2).getValue(), width=20, height=10, command=lambda:onClick(2)))
squares.append(tk.Button(m, text=board.get(3).getValue(), width=20, height=10, command=lambda:onClick(3)))
squares.append(tk.Button(m, text=board.get(4).getValue(), width=20, height=10, command=lambda:onClick(4)))
squares.append(tk.Button(m, text=board.get(5).getValue(), width=20, height=10, command=lambda:onClick(5)))
squares.append(tk.Button(m, text=board.get(6).getValue(), width=20, height=10, command=lambda:onClick(6)))
squares.append(tk.Button(m, text=board.get(7).getValue(), width=20, height=10, command=lambda:onClick(7)))
squares.append(tk.Button(m, text=board.get(8).getValue(), width=20, height=10, command=lambda:onClick(8)))
squares[0].grid(row=0, column=0)
squares[1].grid(row=0, column=1)
squares[2].grid(row=0, column=2)
squares[3].grid(row=1, column=0)
squares[4].grid(row=1, column=1)
squares[5].grid(row=1, column=2)
squares[6].grid(row=2, column=0)
squares[7].grid(row=2, column=1)
squares[8].grid(row=2, column=2)

m.mainloop()