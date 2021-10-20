import tkinter as tk
import tkinter.font as font
import pytesseract as pt
from PIL import Image

wn = tk.Tk()
wn.attributes("-fullscreen", True)

screenWidth, screenHeight = 1920, 1080 #wn.winfo_screenwidth(), wn.winfo_screenheight()
print(screenWidth)

monoFont = font.Font(family ="NotoSansMono Nerd Font", size = 20)


def wrapper(s):
    return lambda: print(s)

def createButtonFrame(string):
    string = string.replace("\n", " \n")
    data = string.split(" ")

    out = tk.Frame(wn)

    lineIndex = 0
    line = tk.Frame(out)
    column = 0

    width = 0

    for i in range(len(data)):
        if data[i].startswith("\n"):
            data[i] = data[i][1:]
            width = screenWidth

        if data[i] == "":
            continue


        w = len(data[i])*16 + 28

        if width + w > screenWidth:
            print(data[i])
            line.grid(column=0, row=lineIndex, sticky="nw")
            lineIndex += 1
            line = tk.Frame(out)
            column = 0
            width = 0

        f = wrapper(data[i])
        button = tk.Button(line, text=data[i], font=monoFont, command=f)



        button.grid(column=column, row=0)
        width += w
        column += 1

    line.grid(column=0, row=lineIndex, sticky="nw")
    return out

def readFromImage(img):
    return pt.image_to_string(img)

topBar = tk.Frame(wn, height = 64, width = screenWidth)

settings = tk.Button(topBar, text = "settings", font = monoFont)
settings.pack(side = "right")

topBar.pack()
topBar.pack_propagate(0)

string = readFromImage(Image.open("testImg.png"))

ButtonFrame = createButtonFrame(string)
ButtonFrame.pack(side = "top")

tk.mainloop()