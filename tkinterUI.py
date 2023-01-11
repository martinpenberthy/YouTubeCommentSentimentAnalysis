import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import YouTubeData


def searchClicked(search_term):
    search_term_string = str(search_term)
    print("CLICKED" + search_term_string)
    YouTubeData.getDataFromYouTube(search_term_string)
    data_collected = 1


def getText():
    user_entry = entry.get()
    print("USER ENTRY: " + user_entry)
    searchClicked(user_entry)


data_collected = 0

window = tk.Tk()
window.minsize(400, 400)

frame = tk.Frame()
label = tk.Label(master=frame, text="WOOORRDDSSS")
label.pack()

entry = tk.Entry(master=frame)
entry.pack()

button = tk.Button(
    master=frame,
    text="Click me",
    width=25,
    height=5,
    bg="black",
    command=getText
)
button.pack()

if data_collected:
    image1 = Image.open("SentimentResultcringe.png")
    test = ImageTk.PhotoImage(image1)

    label1 = tk.Label(image=test, master=frame)
    label1.image = test
    label1.pack()

frame.pack()

window.mainloop()
