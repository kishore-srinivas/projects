from tkinter import *
import numpy as np
# import joint_motion

window = Tk() 
window.geometry('650x300') 

Label(window, text="Destination", font=("Arial Bold", 18)).grid(row=0, column=0, sticky=W, columnspan=2)
Label(window, text="x:", font=("Arial", 8)).grid(row=1, column=0, sticky=E, padx=5)
destX = Entry(window, width=10)
destX.grid(row=1, column=1, sticky=W)
Label(window, text="y:", font=("Arial", 8)).grid(row=2, column=0, sticky=E, padx=5)
destY = Entry(window, width=10)
destY.grid(row=2, column=1, sticky=W)

Label(window, text="Vectors", font=("Arial Bold", 18)).grid(row=0, column=2, sticky=W, columnspan=2, padx=50)
vectors = []
vectorInputs = []
r = 2
def displayAdd():
    global r
    vector = Entry(window, width=10)
    vector.grid(row=r, column=2, sticky=N)
    r = r + 1
    vectorInputs.append(vector)
Button(window, text="+", command=displayAdd).grid(row=1, column=2, sticky=E, padx=60)

bool1 = BooleanVar()
Checkbutton(window, text='Animation', font=("Arial Bold", 18), variable=bool1).grid(row=0, column=4, sticky=W, padx=20)

def submitCalculation():
    print('check state:', bool1.get())
    print('submitting...')
    try:
        x = float(destX.get())
        y = float(destY.get())
        vectorLengths = []
        for v in vectorInputs:
            vectorLengths.append(float(v.get()))
    except:
        x = 0
        y = 0
        vectorLengths = []
    destination = np.array([x, y])
    iterations = 50
    print('check state:', bool1.get())
    window.destroy()
    from joint_motion import calculate
    calculate(destination, vectorLengths, bool1.get(), iterations)

Button(window, text='Calculate', font=("Arial Bold", 16), justify=CENTER, command=submitCalculation).grid(row=0, column=5, sticky=N)


# frame4 = Frame(window)
# frame4.pack(side=BOTTOM, fill=X, pady=10)
# frame1 = Frame(window)
# frame1.pack(side=LEFT, fill=Y)
# frame2 = Frame(window)
# frame2.pack(side=LEFT, fill=Y, padx=50)
# frame3 = Frame(window)
# frame3.pack(side=LEFT, fill=Y)

# vectorsLabel = Label(frame2, text="Vectors", font=("Arial Bold", 18))
# vectorsLabel.pack(fill=X, side=TOP)
# vectors = []
# vectorInputs = []
# def displayAdd():
#     vector = Entry(frame2, width=10)
#     vector.pack(side=TOP)
#     # vector.grid(column=2, row=len(vectorInputs)+2)
#     vector.pack()
#     vectorInputs.append(vector)

# displayAdd = Button(frame2, text="+", command=displayAdd)
# displayAdd.pack(side=TOP)

# def submitCalculation():
#     print('check state:', animation.get())
#     print('submitting...')
#     try:
#         x = float(destX.get())
#         y = float(destY.get())
#         vectorLengths = []
#         for v in vectorInputs:
#             vectorLengths.append(float(v.get()))
#     except:
#         x = 0
#         y = 0
#         vectorLengths = []
#     destination = np.array([x, y])
#     iterations = 50
#     print('check state:', animation.get())
#     window.destroy()
#     joint_motion.calculate(destination, vectorLengths, animation.get(), iterations)

# animation = BooleanVar() 
# animationMode = Checkbutton(frame3, text='Animation', font=("Arial Bold", 18), var=animation) 
# animationMode.pack()

# calculateButton = Button(frame4, text='Calculate', font=("Arial Bold", 12), command=submitCalculation)
# calculateButton.pack(side=BOTTOM, fill=X, padx=10)
 
mainloop()
