import tkinter as tk
import tkinter.font as font
import pytesseract as pt
from PIL import Image
# import picamera as pc
# from gpiozero import Button as btn
import requests
from bs4 import BeautifulSoup as bs

wn = tk.Tk()
wn.attributes("-fullscreen", True)

mainFrame = tk.Frame(wn)
mainFrame.pack()

screenWidth, screenHeight = wn.winfo_screenwidth(), wn.winfo_screenheight()

monoFont = font.Font(family ="NotoSansMono Nerd Font", size = 20)

#bttn = btn(21)

def wrapper(word, parent):
    return lambda: setMainFrame(getWordFrame(word, parent))


def setMainFrame(frame):
    global mainFrame
    old = mainFrame
    mainFrame.pack_forget()
    mainFrame = frame
    mainFrame.pack(side="bottom", fill="both", expand=True)
    return old

mouseData = [False, 0, 0]
def motion(event):
    if mouseData[0]:
        delta = mouseData[1] - event.y + mouseData[2]
        mainFrame.yview_scroll(delta, tk.UNITS)
        mouseData[2] = delta
    else:
        mouseData[0] = True
    mouseData[1] = event.y

def release(event):
    mouseData[0] = False

def createButtonFrame():
    string = readFromImage(Image.open("tmp.png"))
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

        f = wrapper(data[i], out)
        button = tk.Button(line, text=data[i], font=monoFont, command=f, relief = tk.FLAT, padx = 5, pady = 0)

        button.grid(column=column, row=0)
        width += w
        column += 1

    line.grid(column=0, row=lineIndex, sticky="nw")
    out.configure(scrollregion = (0,0,lineIndex*16,0))

    wn.bind("<B1-Motion>", motion)
    wn.bind("<ButtonRelease-1>", release)

    old = setMainFrame(out)
    old.destroy()

    return out

def readFromImage(img):
    return pt.image_to_string(img)

# def camera():
#     global ButtonFrame
#     with pc.PiCamera() as cam:
#         cam.start_preview()
#         bttn.wait_for_press()
#         cam.stop_preview()
#         cam.capture("tmp.png")
#     ButtonFrame = createButtonFrame()

def scrape(word):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(word))
    soup = bs(response.text, 'html')

    synonyms = []
    n = 0
    for header in soup.findAll(class_="ew5makj1"):
        synonyms += header.strong.text.split(", ")
        n += 1
    for i in range(n):
        c = 0
        for syns in soup.findAll(class_="e1ccqdb60")[i]:
            for syn in syns.findAll(class_="css-1kg1yv8"):
                syn = syn.text.strip()
                response2 = requests.get('https://www.dictionary.com/browse/{}'.format(syn))
                soup2 = bs(response2.text, 'html')
                if soup2.find(class_="e1d9ace80") is not None:
                    level = soup2.find(class_="e1d9ace80").span.span.text[2:]
                    if level == "Elementary Level":
                        synonyms.append(syn)
                        c += 1
                        if c >= 5:
                            break
            if c>=5:
                break

    return synonyms

def getSettingsFrame():
    out = tk.Frame(wn, bd=1, relief=tk.RAISED, padx=20, pady=20)
    tk.Label(out, text="this will be the settings page", font=monoFont).grid(row=0, column=0, sticky="nw")
    tk.Button(out, text="X", font=monoFont, command=out.pack_forget).grid(row=0, column=1, sticky="ne")
    return out

def getWordFrame(word, parent):
    syns = scrape(word)

    out = tk.Frame(wn, bd=1, relief=tk.RAISED, padx=20, pady=20)
    tk.Button(out, text="X", font=monoFont, command=lambda: setMainFrame(parent).destroy()).grid(row=0, column=1, sticky="ne")
    tk.Label(out, text=f"synonyms for {word} are:", font=monoFont).grid(row=0, column=0, sticky="n")
    for i in range(len(syns)):
        tk.Label(out, text=syns[i], font=monoFont).grid(row=i+1, column=0, sticky="nw")

    return out






topBar = tk.Frame(wn, height = 64, width = screenWidth)
topBar.pack(side = "top", fill = "x")

settingsFrame = getSettingsFrame()

settingsButton = tk.Button(topBar, text="settings", font=monoFont, command = lambda: settingsFrame.pack( side="top"))
settingsButton.grid(row = 0, column = 0, sticky="e")

cameraButton = tk.Button(topBar, text="camera", font=monoFont, command = createButtonFrame)#camera)
cameraButton.grid(row = 0, column = 1, sticky = "e")


#camera()
createButtonFrame()

tk.mainloop()
