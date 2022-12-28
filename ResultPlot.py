import matplotlib.pyplot as plt
import numpy as np


def plotResults(list_videos, list_scores, search_term):
    #print("list_videos: " + str(len(list_videos)))
    #print("list_scores: " + str(len(list_scores)))
    xpoints = list_videos
    ypoints = list_scores

    plt.xlabel("Video IDs")
    plt.ylabel("Sentiment Score")
    plt.title(search_term)
    plt.xticks(fontsize=8, rotation=90)
    plt.bar(xpoints, ypoints)

    plt.show()

    plt.savefig("SentimentResult" + search_term)
