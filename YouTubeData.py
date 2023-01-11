import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import nltk
from cleantext import clean

import ResultPlot
import SentimentAnalysis

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def getDataFromYouTube(search_term):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC-wXmcxtxwUnmJLJSrb4jZ6pDP0-bkYYM"

    client_secrets_file = "client_secret_241273044011-fjfcd77opncv1rd2q04fcurmv5ptmbkq.apps.googleusercontent.com.json"

    ##############EXTRACT VIDEOIDS FROM SEARCH##############
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_search = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


    request_search = youtube_search.search().list(
        part="snippet",
        maxResults=20,
        q=search_term
    )
    response_search = request_search.execute()

    # Convert the response to a string
    response_search_string = json.dumps(response_search)
    f = open("json_out.json", "w")
    f.write(response_search_string)
    f.close()
    response_search_string_copy = response_search_string

    string_split_search = response_search_string.split('videoId')
    string_split_search_titles = response_search_string.split('title')
    """for string in string_split_search:
        print("\n")
        print(string)
        print("---------------------------")"""

    string_split_search_titles.pop(0)
    titles_clean = []
    print("TITLES: ")
    for title in string_split_search_titles:
        title_index = title.find("\",")
        titles_clean.append(clean(title[4:title_index], no_emoji=True))

    for title in titles_clean:
        print(title + "\n")

    string_split_search.pop(0)
    list_videos = []
    for string in string_split_search:
        text_index = string.find("}")
        list_videos.append(string[4:text_index - 1])
        # print(text_index)

    for string in list_videos:
        print(string)
        print("---------------------------")
    print("Video Id's successfully extracted")
    print("list_videos length: " + str(len(list_videos)))

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    list_scores = []
    video_index = 0
    for videoID in list_videos:
        try:
            # Gets the pinned comment and the 99 most recent comments in addition to their replies
            request = youtube.commentThreads().list(
                part="snippet,replies",
                # videoId="pRiGQWfiz2A",
                videoId=videoID,
                maxResults=25
            )
            response = request.execute()
            # Convert the response to a string
            response_string = json.dumps(response)

            # Split the response string at the 'textOriginal' tags
            string_split = response_string.split('textOriginal')

            list = []
            for string in string_split:
                text_index = string.find("authorDisplayName")
                list.append(clean(string[4:text_index - 4], no_emoji=True))
                # print(text_index)

            list.pop(0)
            """for item in list:
                print(item)
                print("\n")"""

            analysis_result = SentimentAnalysis.doAnalysis(list)
            print("Index: " + str(video_index))
            print("VideoID: " + str(videoID))
            print("Analysis Result: " + str(analysis_result))
            list_scores.append(analysis_result)
            video_index += 1

        except googleapiclient.errors.HttpError:
            print("-----------------Error with request------------------")
            print("for video id: " + str(videoID))
            list_scores.append(0)
            video_index += 1
    # END FOR

    print("All Scores: " + str(list_scores))
    total_scores = 0

    for score in list_scores:
        total_scores += score

    print("Scores Total: " + str(total_scores))

    ResultPlot.plotResults(titles_clean, list_scores, search_term)