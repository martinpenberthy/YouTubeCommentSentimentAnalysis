import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import YouTubeData


# Gets a string with the earch term entered from getText()
def searchClicked(search_term):
    data_collected = 1
    search_term_string = str(search_term)
    print("CLICKED" + search_term_string)
    # Call function to get videos and comments from YouTube
    YouTubeData.getDataFromYouTube(search_term_string)


# Called when user clicks search button
def getText():
    user_entry = entry.get()
    print("USER ENTRY: " + user_entry)
    # Call searchClicked function
    searchClicked(user_entry)


# String for save user entry
user_entry = ""
data_collected = 0
# Make a window
window = tk.Tk()
window.minsize(400, 200)

# Labels with text
frame = tk.Frame()
label = tk.Label(master=frame, text="YouTube Comment Sentiment Analysis", bg="#00aaff")
label.pack()

label2 = tk.Label(master=frame, text="Enter a search term below!")
label2.pack()

# Place for user to enter search term
entry = tk.Entry(master=frame)
entry.pack()
# Search button which calls getText()
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
