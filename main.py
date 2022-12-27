# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

import SentimentAnalysis

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    """
        i = 0
        while i < 130:
            index = response_string.find('textOriginal: ', index + 12)
            #print(index)
            i += 1
    """
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC-wXmcxtxwUnmJLJSrb4jZ6pDP0-bkYYM"

    client_secrets_file = "client_secret_241273044011-fjfcd77opncv1rd2q04fcurmv5ptmbkq.apps.googleusercontent.com.json"

    ##############EXTRACT 25 VIDEOIDS FROM SEARCH##############
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_search = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_search = youtube_search.search().list(
        part="snippet",
        maxResults=20,
        q="funny"
    )
    response_search = request_search.execute()

    # Convert the response to a string
    response_search_string = json.dumps(response_search)

    string_split_search = response_search_string.split('videoId')

    """for string in string_split_search:
        print("\n")
        print(string)
        print("---------------------------")"""

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
                maxResults=10
            )
            response = request.execute()
            # Convert the response to a string
            response_string = json.dumps(response)

            # Split the response string at the 'textOriginal' tags
            string_split = response_string.split('textOriginal')

            list = []
            for string in string_split:
                text_index = string.find("authorDisplayName")
                list.append(string[4:text_index - 4])
                # print(text_index)

            list.pop(0)
            for item in list:
                print(item)
                print("\n")

            analysis_result = SentimentAnalysis.doAnalysis(list)
            print("Index: " + str(video_index))
            print("VideoID: " + str(videoID))
            print("Analysis Result: " + str(analysis_result))
            list_scores.append(analysis_result)
            video_index += 1

        except googleapiclient.errors.HttpError:
            print("COMMENTS DISABLED")
            video_index += 1
    #END FOR

    print("All Scores: " + str(list_scores))
    total_scores = 0

    for score in list_scores:
        total_scores += score

    print("Scores Total: " + str(total_scores))

    #print(response_search_string)
if __name__ == "__main__":
    main()
