# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import YouTubeData
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


def searchClicked(search_term):
    print("CLICKED")
    #YouTubeData.getDataFromYouTube(search_term)

def main():
    data_collected = 0
    search_term = ""

    window = tk.Tk()
    window.minsize(400, 400)

    frame = tk.Frame()
    label = tk.Label(master=frame, text="WOOORRDDSSS")
    label.pack()

    def showMessage():
        messagebox.showinfo("Message", "This is a message")

    button = tk.Button(
        master=frame,
        text="Click me",
        width=25,
        height=5,
        bg="black",
        command=searchClicked(search_term)
    )
    button.pack()

    entry = tk.Entry(master=frame)
    entry.pack()


    if data_collected:
        image1 = Image.open("SentimentResultcringe.png")
        test = ImageTk.PhotoImage(image1)

        label1 = tk.Label(image=test)
        label1.image = test
        label1.pack()
    frame.pack()



    window.mainloop()
if __name__ == "__main__":
    main()
