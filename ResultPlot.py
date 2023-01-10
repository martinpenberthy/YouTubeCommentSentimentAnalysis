import matplotlib.pyplot as plt
import numpy as np


def plotResults(titles_clean, list_scores, search_term):
    print("titles: " + str(len(titles_clean)))
    print("list_scores: " + str(len(list_scores)))
    xpoints = titles_clean
    ypoints = list_scores

    plt.xlabel("Video IDs")
    plt.ylabel("Sentiment Score")
    plt.title(search_term)
    plt.xticks(fontsize=8, rotation=90)
    plt.bar(xpoints, ypoints)
    plt.savefig("SentimentResult" + search_term)
    #plt.show()


