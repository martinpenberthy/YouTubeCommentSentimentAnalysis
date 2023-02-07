import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap

def plotResults(titles_clean, list_scores, search_term):
    print("titles: " + str(len(titles_clean)))
    print("list_scores: " + str(len(list_scores)))

    result_count=len(list_scores)
    result_position = list(range(1, result_count+1))


    xpoints = result_position
    ypoints = list_scores

    print("xpoints: " + str(xpoints))
    print("ypoints: " + str(ypoints))

    #xpoints = ['\n'.join(wrap(title, 15)) for title in xpoints]
    #plt.figure(figsize=(12, 10))

    plt.xlabel("Search Position")
    plt.ylabel("Sentiment Score", fontsize=15)
    plt.title(search_term, fontsize=15)

    plt.xticks(np.arange(1, result_count+1, 1), fontsize=7, rotation=90)
    #plt.tight_layout()
    #plt.bar(xpoints, ypoints)
    plt.scatter(xpoints, ypoints, c="blue")
    plt.grid()
    #plt.legend(loc="best")
    #plt.subplots_adjust(top=2)s
    #plt.subplots_adjust(bottom=.1)

    #plt.margins()
    plt.savefig("SentimentResult" + search_term)
    plt.show()
