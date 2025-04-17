import tkinter as tk
from tkinter import messagebox

#Create the main window and the containers 
window = tk.Tk()
window.title("Game")
window.geometry("800x600")

frameBoard = tk.Frame(window, width=450, height=450)
frameBoard.pack_propagate(False)
frameBoard.place(x=50, y=50)

frameMenu = tk.Frame(window)
frameMenu.place(x=600, y=10)

crossImg = tk.PhotoImage(file="assets/cruz.png")
crossImg = crossImg.subsample(2,2) #100 x 100
circleImg = tk.PhotoImage(file="assets/circulo.png")
circleImg = circleImg.subsample(2,2)
boardImg = tk.PhotoImage(file="assets/board.png")
boardImg = boardImg.subsample(2,2) #450 x 450 

labelBoard = tk.Label(frameBoard, image=boardImg)
labelBoard.place(x=0, y=0)

buttons = []
turn = ""
board = [""]*9
playsLabel = []

#Set the symbol for the human and robot
HUMAN = "O"
ROBOT = "X"

winCombination = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)]

def start():
    print("Starting...")
    global turn
    firstPlayer = showPlayerSelection()
    print("Selected turn is: ", firstPlayer)
    createButtons(frameBoard)
    if firstPlayer == "Human":
        turn = HUMAN
    else:
        turn = ROBOT
        window.after(500, robotPlay)

def click(position): 
    global turn
    convertButtonToLabel(position)
    board[position] = turn
    winner = checkWinner()
    if winner:
        messagebox.showinfo("Game Over", f"🎉 ¡The winner is the {winner}!")
        reinit()
    elif "" not in board:
        messagebox.showinfo("Game Over", "Tie game")
        reinit()
    else:
        turn = ROBOT if turn == HUMAN else HUMAN
        if turn == ROBOT:
            window.after(500, robotPlay)

def checkWinner():
    for i,j,k in winCombination:
        if board[i] == board[j] == board[k] and board[i] != "":
            if board[i] == HUMAN:
                return "HUMAN"
            else:
                return "ROBOT"
    return None
    
def robotPlay():
    global turn, board
    if turn == ROBOT:
        posibles = [i for i, val in enumerate(board) if val == ""]
        if posibles:
            pos = getBestPlay(board)
            #send pos to the robot and 
            #wait until the robot send ok by serial port

            print("Robot select: " , pos)
            board[pos] = ROBOT
            click(pos) #Execute robot choice

def getBestPlay(board):
    def findPlay(player):
        for i, j, k in winCombination:
            line = [board[i], board[j], board[k]]
            if line.count(player) == 2 and line.count("") == 1:
                return [i, j, k][line.index("")]
        return None

    #Play to win
    play = findPlay(ROBOT)
    if play is not None:
        return play

    #Play to block
    play = findPlay(HUMAN)
    if play is not None:
        return play

    #Take center
    if board[4] == "":
        return 4

    #Corner first
    for i in [0, 2, 6, 8]:
        if board[i] == "":
            return i

    #Get sides
    for i in [1, 3, 5, 7]:
        if board[i] == "":
            return i

    return None  #No play availables

def reinit():
    #Set board clear, destroy labels and buttons
    global board
    board = [""]*9
    for label in playsLabel:
        label.destroy()
    for button in buttons:
        button.destroy()
    res = messagebox.askyesno("", "Do you want to play again?")
    start() if res else close()

def close():
    window.destroy()

def convertButtonToLabel(position):
    global turn
    if buttons:
        buttons[position].destroy()
    if turn == "X":
        label = tk.Label(frameBoard, image=crossImg)
    else: 
        label = tk.Label(frameBoard, image=circleImg)
    label.grid(row=position//3, column=position%3, padx=30, pady=20)
    playsLabel.append(label)

def createButtons(window):
    for i in range(9):
        if board[i] == "":
            button = tk.Button(window, text=str(i),font=('Arial', 20), 
                       command=lambda i = i:click(i))
            button.grid(row=i//3, column=i%3, padx=55, pady = 50)
            buttons.append(button)

def createMenu(window):
    buttonStart = tk.Button(window, text= "Start", font=('Arial', 12), 
                            command= start)
    buttonReinit = tk.Button(window, text="Reinit", font=('Arial', 12),command=reinit)
    buttonOut = tk.Button(window, text="Salir", font=('Arial', 14), command=close)
    buttonStart.pack(pady=10, fill= 'x')
    buttonReinit.pack(pady=10, fill='x')
    buttonOut.pack(pady=10, fill= 'x')
      
def showPlayerSelection():
    selection = {"Value" : ""}
    def HSelected():
        selection["Value"] = "Human"
        dialog.destroy()

    def RSelected():
        selection["Value"] = "Robot"
        dialog.destroy()


    dialog = tk.Toplevel(window)
    dialog.title("Select your player")
    dialog.geometry("300x150")
    dialog.grab_set()  #Blocks principal window

    tk.Label(dialog, text="Select your turn", font=("Arial", 12)).pack(pady=20)

    selectButtons = tk.Frame(dialog)
    selectButtons.pack()

    tk.Button(selectButtons, text="Human First", width=10, command=HSelected).pack(side="left", padx=10)
    tk.Button(selectButtons, text="Robot First", width=10, command=RSelected).pack(side="right", padx=10)

    window.wait_window(dialog)

    return selection["Value"]

createMenu(frameMenu)


#Show window
window.mainloop()