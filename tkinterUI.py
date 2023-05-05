import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import YouTubeData


# Gets a string with the search term entered from getText()
def searchClicked(search_term, vid_count, comment_count):
    data_collected = 1
    search_term_string = str(search_term)
    print("CLICKED" + search_term_string)
    # Call function to get videos and comments from YouTube
    YouTubeData.getDataFromYouTube(search_term_string, int(vid_count), int(comment_count))


# Called when user clicks search button
def getValues():
    user_entry = entry.get()
    vid_result_count = combo_vid_count.get()
    comment_count = combo_com_count.get()
    print("USER ENTRY: " + user_entry)
    print("VID COUNT: " + str(vid_result_count))
    # Call searchClicked function
    searchClicked(user_entry, vid_result_count, comment_count)


# String for save user entry
user_entry = ""
vid_result_count = 0
comment_count = 0
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

###########VIDEO COUNT###########
label3 = tk.Label(#master=frame,
                  text="Video count")
label3.place(x=20, y=90)

combo_vid_count = ttk.Combobox(
    #master=frame,
    state="readonly",
    values=["5", "10", "15", "20", "25", "30", "35", "40", "45", "50"],
    width=5,
    justify="center"
)
combo_vid_count.current(4)
combo_vid_count.place(x=30, y=110)


###########COMMENT COUNT###########
label3 = tk.Label(#master=frame,
                  text="Comment count")
label3.place(x=280, y=90)

combo_com_count = ttk.Combobox(
    #master=frame,
    state="readonly",
    values=["10", "25", "50", "75", "100"],
    width=5,
    justify="center"
)
combo_com_count.current(4)
combo_com_count.place(x=305, y=110)

# Search button which calls getText()

button = tk.Button(
    window,
    text="Analyze",
    width=10,
    height=3,
    #fg="red",
    #bg="black",
    command=getValues
)
button.place(x=155, y=120)
#button.pack()

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
