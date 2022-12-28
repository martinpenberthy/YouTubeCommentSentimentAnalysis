import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def doAnalysis(commentsList) -> float:
    sia = SentimentIntensityAnalyzer()

    scores_total = 0
    for comment in commentsList:
        #print(sia.polarity_scores(comment))
        positive_score = sia.polarity_scores(comment)["pos"]
        negative_score = sia.polarity_scores(comment)["neg"]
        compound_score = sia.polarity_scores(comment)["compound"]
        #print("Neg: " + str(negative_score))
        #print("Comp: " + str(compound_score))
        #print("Pos: " + str(positive_score))
        scores_total += positive_score
        scores_total -= negative_score
        #print(compound_scores_total)
    return scores_total
