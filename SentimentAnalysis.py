import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


# This function does sentiment analysis for all comments in one video
# Takes a list of strings of comments
# Returns a float which is the sentiment score for the video
def doAnalysis(commentsList) -> float:
    # Instantiate the SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    # Get a corpus of English stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    commentsList_token = []
    # Tokenize words for each comment in the list for sentiment analysis
    for comment in commentsList:
        commentsList_token.append(nltk.word_tokenize(comment))

    commentsList_token_stops = []
    # Remove all stopwords from each comment
    for comment in commentsList_token:
        commentsList_token_stops.append([w for w in comment if w.lower() not in stopwords])

    commentsList_final = []
    # Rejoin comments in list
    for comment in commentsList_token_stops:
        commentsList_final.append(' '.join(comment))

    scores_total = 0
    # For each comment, do analysis
    for comment in commentsList_final:
        # print(sia.polarity_scores(comment))
        positive_score = sia.polarity_scores(comment)["pos"]
        negative_score = sia.polarity_scores(comment)["neg"]
        compound_score = sia.polarity_scores(comment)["compound"]
        # print("Neg: " + str(negative_score))
        # print("Comp: " + str(compound_score))
        # print("Pos: " + str(positive_score))
        scores_total += positive_score
        scores_total -= negative_score
        # print(compound_scores_total)

    # Return the total score for one video's worth of comments
    return scores_total
