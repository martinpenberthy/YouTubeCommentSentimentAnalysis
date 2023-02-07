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
    f = open("json_out2.json", "w")
    f.write(response_search_string)
    f.close()

    count = response_search["pageInfo"]["resultsPerPage"]
    list_videos = []

    for i in range(count):
        print("LOOP")
        if response_search["items"][i]["id"]["kind"] == "youtube#video":
            print("if TRUE")
            string = response_search["items"][i]["id"]["videoId"]
            list_videos.append(string)

    print("VideoIds extracted")

    for string in list_videos:
        print(string)
        print("---------------------------")

    titles = []
    titles_clean = []
    for i in range(count):
        print(response_search["items"][i]["snippet"]["title"])
        if response_search["items"][i]["id"]["kind"] == "youtube#video":
            print("if TRUE")
            string = json.dumps(response_search["items"][i]["snippet"]["title"])
            titles.append(string)

    for string in titles:
        titles_clean.append(clean(string, no_emoji = True))

    """response_search_string_copy = response_search_string
    response_search_string_copy2 = response_search_string

    string_split_search = response_search_string.split('videoId')
    string_split_search_titles = response_search_string_copy.split('title')
    string_split_kind = response_search_string_copy2.split('kind')
    channel_index = 0

    for string in string_split_kind:
        print("\n")
        print("KIND: " + string)
        print("---------------------------")
        channel_index = string.find('youtube#channel')

    for string in string_split_search_titles:
        print("\n")
        print(string)
        print("---------------------------")

    string_split_search_titles.pop(0)
    titles_clean = []

    for title in string_split_search_titles:
        title_index = title.find("\",")
        titles_clean.append(clean(title[4:title_index], no_emoji=True))
    print("TITLES: ")
    for title in titles_clean:
        print(title + "\n")

    if channel_index == -1:
        titles_clean.pop(0)

    print("Channel Index: " + str(channel_index))

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
"""
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    list_scores = []
    video_index = 0
    for videoID in list_videos:
        try:
            # Gets the pinned comment and "maxResults" most recent comments in addition to their replies
            request = youtube.commentThreads().list(
                part="snippet,replies",
                # videoId="pRiGQWfiz2A",
                videoId=videoID,
                maxResults=25
            )
            response = request.execute()
            # Convert the response to a string
            response_string = json.dumps(response)

            f = open("json_outComments.json", "w")
            f.write(response_string)
            f.close()

            # Split the response string at the 'textOriginal' tags
            #string_split = response_string.split('textOriginal')

            comments_count = response["pageInfo"]["totalResults"]
            list = []
            for i in range(comments_count):
                string = response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                #print("JSONTETST")
                #print(string)
                list.append(clean(string, no_emoji= True))

            """for string in string_split:
                text_index = string.find("authorDisplayName")
                list.append(clean(string[4:text_index - 4], no_emoji=True))
                # print(text_index)

            list.pop(0)"""
            """for item in list:
                print(item)
                print("\n")"""

            analysis_result = SentimentAnalysis.doAnalysis(list)
            #print("Index: " + str(video_index))
            #print("VideoID: " + str(videoID))
            #print("Analysis Result: " + str(analysis_result))
            list_scores.append(analysis_result)
            video_index += 1

        except googleapiclient.errors.HttpError as e:
            print("-----------------Error with request------------------")
            print("for video id: " + str(videoID))
            print("ERROR: " + str(e.error_details[0]["reason"]))
            print("ERROR: " + str(e.error_details[0]["message"]))
            #print("ERROR: " + str(e.error_details["errors"]["message"]))
            list_scores.append(0)
            video_index += 1
        """else:
            list_scores.append(0)
            video_index += 1"""
    # END FOR

    print("All Scores: " + str(list_scores))
    total_scores = 0

    for score in list_scores:
        total_scores += score

    print("Scores Total: " + str(total_scores))

    file = open("SentimentResult_" + search_term + ".txt", "w")
    file.write("Search Term: " + search_term + "\n")

    count = 1
    for title in titles_clean:
        file.write("Search Position: " + str(count) + "\n")
        file.write("Title: " + title + "\n")
        file.write("Score: " + str(list_scores[count - 1]) + "\n\n")
        count += 1

    file.write("Score Total" + str(total_scores))
    file.close()

    ResultPlot.plotResults(titles_clean, list_scores, search_term)
