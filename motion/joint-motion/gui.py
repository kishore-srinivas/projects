from tkinter import *
import numpy as np
import joint_motion

window = Tk() 
window.geometry('500x300') 
frame4 = Frame(window)
frame4.pack(side=BOTTOM, fill=X, pady=10)
frame1 = Frame(window)
frame1.pack(side=LEFT, fill=Y)
frame2 = Frame(window)
frame2.pack(side=LEFT, fill=Y, padx=50)
frame3 = Frame(window)
frame3.pack(side=LEFT, fill=Y)

destLabel = Label(frame1, text="Destination", font=("Arial Bold", 18))
destLabel.pack(fill=X, side=TOP)
destX = Entry(frame1, width=10) 
destX.insert(END, 'x')
destX.pack(side=TOP)
destX.focus()
destY = Entry(frame1, width=10) 
destY.insert(END, 'y')
destY.pack(side=TOP)

vectorsLabel = Label(frame2, text="Vectors", font=("Arial Bold", 18))
vectorsLabel.pack(fill=X, side=TOP)
vectors = []
vectorInputs = []
def displayAdd():
    vector = Entry(frame2, width=10)
    vector.pack(side=TOP)
    # vector.grid(column=2, row=len(vectorInputs)+2)
    vector.pack()
    vectorInputs.append(vector)

displayAdd = Button(frame2, text="+", command=displayAdd)
displayAdd.pack(side=TOP)

chk_state = BooleanVar() 
animationMode = Checkbutton(frame3, text='Animation', font=("Arial Bold", 18), var=chk_state) 
animationMode.pack()

def submitCalculation():
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
    print('check state:', chk_state.get())
    window.destroy()
    joint_motion.calculate(destination, vectorLengths, chk_state.get(), iterations)

calculateButton = Button(frame4, text='Calculate', font=("Arial Bold", 12), command=submitCalculation)
calculateButton.pack(side=BOTTOM, fill=X, padx=10)
 
window.mainloop()
