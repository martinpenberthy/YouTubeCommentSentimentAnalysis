import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap


# This function plots the results of the sentiment analysis
# It receives a list of video titles, scores for videos in corresponding order,
# and the search term used
def plotResults(titles_clean, list_scores, search_term):
    plt.clf()
    print("titles: " + str(len(titles_clean)))
    print("list_scores: " + str(len(list_scores)))

    # Determine how many results there are
    result_count = len(list_scores)
    result_position = list(range(1, result_count + 1))

    # Save the x axis data and y axis data
    xpoints = result_position
    ypoints = list_scores

    print("xpoints: " + str(xpoints))
    print("ypoints: " + str(ypoints))

    # Set the labels
    plt.xlabel("Search Position")
    plt.ylabel("Sentiment Score", fontsize=15)
    plt.title(search_term, fontsize=15)
    # Set the tick size
    plt.xticks(np.arange(1, result_count + 1, 1), fontsize=7, rotation=90)
    # plt.tight_layout()
    # plt.bar(xpoints, ypoints)
    # Create a scatter plot
    plt.scatter(xpoints, ypoints, c="blue")
    # Display a grid
    plt.grid()
    # plt.legend(loc="best")
    # plt.subplots_adjust(top=2)s
    # plt.subplots_adjust(bottom=.1)
    # plt.margins()
    # Save the resulting plot as an image
    plt.savefig("SentimentResult" + search_term)
    plt.show()
