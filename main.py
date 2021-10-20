import tkinter as tk
import tkinter.font as font
import pytesseract as pt
from PIL import Image

wn = tk.Tk()
wn.attributes("-fullscreen", True)

screenWidth, screenHeight = 1920, 1080 #wn.winfo_screenwidth(), wn.winfo_screenheight()

monoFont = font.Font(family ="NotoSansMono Nerd Font", size = 20)


def wrapper(s):
    return lambda: print(s)

mouseData = [False, 0, 0]
def motion(event):
    if mouseData[0]:
        delta = mouseData[1] - event.y + mouseData[2]
        ButtonFrame.yview_scroll(delta, tk.UNITS)
        mouseData[2] = delta
    else:
        mouseData[0] = True
    mouseData[1] = event.y

def release(event):
    mouseData[0] = False

def createButtonFrame(string):
    string = string.replace("\n", " \n")
    data = string.split(" ")

    out = tk.Canvas(wn, yscrollincrement = 1)
    frame = tk.Frame(out)

    frame.bind(
        "<Configure>",
        lambda e: out.configure(
            scrollregion=out.bbox("all")
        )
    )


    out.create_window((0, 0), window=frame, anchor="nw")

    lineIndex = 0
    line = tk.Frame(frame)
    column = 0

    width = 0

    for i in range(len(data)):
        if data[i].startswith("\n"):
            data[i] = data[i][1:]
            width = screenWidth

        if data[i] == "":
            continue

        w = len(data[i])*16 + 16

        if width + w > screenWidth:
            line.grid(column=0, row=lineIndex, sticky="nw")
            lineIndex += 1
            line = tk.Frame(frame)
            column = 0
            width = 0

        f = wrapper(data[i])
        button = tk.Button(line, text=data[i], font=monoFont, command=f, relief = tk.FLAT, padx = 5, pady = 0)

        button.grid(column=column, row=0)
        width += w
        column += 1

    line.grid(column=0, row=lineIndex, sticky="nw")
    out.configure(scrollregion = (0,0,lineIndex*16,0))

    wn.bind("<B1-Motion>", motion)
    wn.bind("<ButtonRelease-1>", release)
    return out

def readFromImage(img):
    return pt.image_to_string(img)

topBar = tk.Frame(wn, height = 64, width = screenWidth)

topBar.pack(side = "top", fill = "x")



string = readFromImage(Image.open("testImg.png"))


ButtonFrame = createButtonFrame(string)
ButtonFrame.pack(side = "bottom", fill = "both", expand = True)

settingsFrame = tk.Frame(wn, bd = 1, relief = tk.RAISED, padx = 20, pady = 20)
tk.Label(settingsFrame, text = "this will be the settings page", font = monoFont).grid(row = 0, column = 0, sticky = "nw")
tk.Button(settingsFrame, text = "X", font = monoFont, command = settingsFrame.pack_forget).grid(row = 0, column = 1, sticky = "ne")

settingsButton = tk.Button(topBar, text="settings", font=monoFont, command = lambda: settingsFrame.pack( side="top"))
settingsButton.grid(sticky="e")

tk.mainloop()