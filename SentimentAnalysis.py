import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


def doAnalysis(commentsList) -> float:
    sia = SentimentIntensityAnalyzer()

    #list_no_stop = []
    stopwords = nltk.corpus.stopwords.words("english")
    commentsList_token = []
    for comment in commentsList:
        commentsList_token.append(nltk.word_tokenize(comment))

    commentsList_token_stops = []
    for comment in commentsList_token:
        commentsList_token_stops.append([w for w in comment if w.lower() not in stopwords])

    commentsList_final = []
    for comment in commentsList_token_stops:
        commentsList_final.append(' '.join(comment))

    """for comment in commentsList:
        no_stop = [w for w in comment if w.lower() not in stopwords]
        list_no_stop.append(no_stop)"""


    scores_total = 0
    for comment in commentsList_final:
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
