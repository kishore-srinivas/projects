from tkinter import *

window = Tk() 
window.geometry('350x200') 

destLabel = Label(window, text="Destination", font=("Arial Bold", 18))
destLabel.grid(column=0, row=0)

destX = Entry(window,width=10) 
destX.insert(END, 'x')
destX.grid(column=0, row=1)
destX.focus()
destY = Entry(window,width=10) 
destY.insert(END, 'y')
destY.grid(column=1, row=1)
 
def submit():
    print('destination: (', destX.get(), ', ', destY.get(), ')')
    # lbl.configure(text=txt.get())
 
submit = Button(window, text="Submit", command=submit) 
submit.grid(column=0, row=2)

vectors = []
vectorInputs = []
def displayAdd():
    vector = Entry(window, width=10)
    vector.grid(column=2, row=len(vectorInputs)+2)
    vectorInputs.append(vector)
def submitVectors():
    vectors = []
    for v in vectorInputs:
        try:
            vectors.append(int(v.get()))
        except:
            continue
    print(vectors)

displayAdd = Button(window, text="+", command=displayAdd)
displayAdd.grid(column=2, row=0)
submitVectors = Button(window, text="Submit Vectors", command=submitVectors)
submitVectors.grid(column=2, row=1)

chk_state = BooleanVar() 
chk_state.set(False) #set check state 
animationMode = Checkbutton(window, text='Animation', var=chk_state) 
animationMode.grid(column=4, row=0)
 
window.mainloop()
