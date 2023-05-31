import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from utils.comments import process_comments, make_csv

load_dotenv()

API_KEY = os.getenv("API_KEY")

youtube = build("youtube","v3",developerKey=API_KEY)

def comment_threads(vidID, to_csv):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
    part='id,replies,snippet',
    videoId = vidID
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))
    
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=vidID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))
        
    print(f"Finished fetching comments for {vidID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, vidID)
    
    return comments_list

#videoID will be replaced by the youtube video's unique ID identified as the set of alphanumeric characters after the = symbol in the hyperlink
def main():
    comment_threads('videoID',to_csv = True)


if __name__ == "__main__":
    main()
