# Martin Penberthy
# This file contains code for requesting data from the YouTube API V3.
# The data needed is extracted and stored. Then the data is passed to the
# SentimentAnalysis.py file which returns a sentiment score. This file then
# passes the analyzed data to the ResultPlot.py file which generates a graph.

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


# This fuction getss invoked by tkinterUI.py which passes it the search  term to use
def getDataFromYouTube(search_term):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC-wXmcxtxwUnmJLJSrb4jZ6pDP0-bkYYM"
    client_secrets_file = "client_secret_241273044011-fjfcd77opncv1rd2q04fcurmv5ptmbkq.apps.googleusercontent.com.json"

    # YouTube API set up
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_search = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Set parameters for video search
    request_search = youtube_search.search().list(
        part="snippet",
        maxResults=20,
        q=search_term
    )
    # Execute request and save the response
    response_search = request_search.execute()

    # Convert the response to a string to write to file for debug purposes
    response_search_string = json.dumps(response_search)
    f = open("json_out2.json", "w")
    f.write(response_search_string)
    f.close()
    # Get the number of results returned
    count = response_search["pageInfo"]["resultsPerPage"]
    list_videos = []
    # For every video in the response, add the ID to the list
    for i in range(count):
        if response_search["items"][i]["id"]["kind"] == "youtube#video":
            string = response_search["items"][i]["id"]["videoId"]
            list_videos.append(string)

    print("VideoIds extracted")
    """
    for string in list_videos:
        print(string)
        print("---------------------------")
    """

    titles = []
    titles_clean = []
    # For every video in the response, add the video title to the list
    for i in range(count):
        print(response_search["items"][i]["snippet"]["title"])
        if response_search["items"][i]["id"]["kind"] == "youtube#video":
            print("if TRUE")
            string = json.dumps(response_search["items"][i]["snippet"]["title"])
            titles.append(string)

    # Strip emojis from the titles
    for string in titles:
        titles_clean.append(clean(string, no_emoji=True))

    # Set up YouTube APIv3
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    list_scores = []
    video_index = 0
    # For every video ID in the list
    for videoID in list_videos:
        try:
            # Gets the pinned comment and "maxResults" most recent comments in addition to their replies
            request = youtube.commentThreads().list(
                part="snippet,replies",
                # videoId="pRiGQWfiz2A",
                videoId=videoID,
                maxResults=25
            )
            # Store the response
            response = request.execute()
            # Convert the response to a string
            response_string = json.dumps(response)
            # Write to file for debugging purposes
            f = open("json_outComments.json", "w")
            f.write(response_string)
            f.close()

            # Get the number of comments actually returned
            comments_count = response["pageInfo"]["totalResults"]
            list = []
            # Get each comment, strip emojis and add it to the list
            for i in range(comments_count):
                string = response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                list.append(clean(string, no_emoji=True))

            # Invoke the analysis function and give it the list of comments
            analysis_result = SentimentAnalysis.doAnalysis(list)
            # print("Index: " + str(video_index))
            # print("VideoID: " + str(videoID))
            # print("Analysis Result: " + str(analysis_result))

            # Add the results for each video
            list_scores.append(analysis_result)
            video_index += 1
        # Catch any errors with the API request
        except googleapiclient.errors.HttpError as e:
            print("-----------------Error with request------------------")
            print("for video id: " + str(videoID))
            print("ERROR: " + str(e.error_details[0]["reason"]))
            print("ERROR: " + str(e.error_details[0]["message"]))
            # print("ERROR: " + str(e.error_details["errors"]["message"]))
            list_scores.append(0)
            video_index += 1
    # END FOR

    print("All Scores: " + str(list_scores))
    total_scores = 0
    # Calculate total score for all videos
    for score in list_scores:
        total_scores += score

    print("Scores Total: " + str(total_scores))
    # Create a text file to contain results
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

    # Display results in new window and save as png
    ResultPlot.plotResults(titles_clean, list_scores, search_term)
