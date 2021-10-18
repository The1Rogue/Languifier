import tkinter as tk
import tkinter.font as font

wn = tk.Tk()
wn.attributes("-fullscreen", True)

screenWidth, screenHeight = wn.winfo_screenwidth(), wn.winfo_screenheight()

helv = font.Font(family = "Helvetica", size = 20)

file = open("testtext.txt")
string = file.read()
file.close()

def wrapper(s):
    return lambda: print(s)

def createButtonFrame(string):
    string = string.replace("\n", " \n")
    data = string.split(" ")

    out = tk.Frame(wn)

    line = tk.Frame(out)
    lineIndex = 0
    column = 0

    for i in range(len(data)):
        if data[i].startswith("\n"):
            line.grid(column=0, row=lineIndex, sticky="nw")
            lineIndex += 1
            line = tk.Frame(out)
            column = 0
            data[i] = data[i][1:]

        if data[i] == "":
            continue

        f = wrapper(data[i])
        tk.Button(line, text = data[i], font = helv, command = f).grid(column = column, row = 0)
        column += 1

    line.grid(column=0, row=lineIndex, sticky="nw")
    return out


topBar = tk.Frame(wn, height = 64, width = screenWidth)

settings = tk.Button(topBar, text = "settings", font = helv)
settings.pack(side = "right")

topBar.pack()
topBar.pack_propagate(0)

ButtonFrame = createButtonFrame(string)
ButtonFrame.pack(side = "top")

tk.mainloop()