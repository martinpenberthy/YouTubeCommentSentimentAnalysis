import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import YouTubeData


def searchClicked(search_term):
    data_collected = 1
    search_term_string = str(search_term)
    print("CLICKED" + search_term_string)
    YouTubeData.getDataFromYouTube(search_term_string)



def getText():
    user_entry = entry.get()
    print("USER ENTRY: " + user_entry)
    searchClicked(user_entry)

user_entry = ""
data_collected = 0

window = tk.Tk()
window.minsize(400, 400)

frame = tk.Frame()
label = tk.Label(master=frame, text="YouTube Comment Sentiment Analysis", bg="#00aaff")
label.pack()

label2 = tk.Label(master=frame, text="Enter a search term below!")
label2.pack()

entry = tk.Entry(master=frame)
entry.pack()

button = tk.Button(
    master=frame,
    text="Analyze",
    width=10,
    height=3,
    bg="black",
    command=getText
)
button.pack()

filename = "SentimentResult" + user_entry + ".png"
frame.pack()

"""
if data_collected:
    image1 = Image.open(filename)
    test = ImageTk.PhotoImage(image1)

    label1 = tk.Label(image=test)
    label1.image = test
    label1.pack()
    #label1.place(0, 0)
    data_collected = 0
"""


window.mainloop()
