from googleapiclient.discovery import build
import pandas as pd

DEVELOPER_KEY = "key"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#1. Load video lists related with keywords 
video_list = []
url = []
keyword = input("검색할 키워드를 입력하시오 > ")
day = input("ex 2020-01-01 > ")

search_response = youtube.search().list(
    publishedAfter = day +'T00:00:00+09:00',
    q = keyword,
    order = "date",
    part = "snippet",
    pageToken = None,
    maxResults = 50
    ).execute()

while "nextPageToken" in search_response:
    next_token = search_response["nextPageToken"]
    for item in search_response["items"]:
        try:
            videoId = item["id"]["videoId"]
        except:
            pass
        video_url = "https://www.youtube.com/watch?v="
        video_list.append(videoId)
        url.append(video_url+videoId)
    search_response = youtube.search().list(
        publishedAfter = day +'T00:00:00+09:00',
        q = keyword,
        order = "date",
        part = "snippet",
        pageToken = next_token,
        maxResults = 50
        ).execute()
    
#2 Extract information of videoes
dict_keys = ["content", "id", "date", "view", "like", "tags", "url", "image", "followers", "total_content", "total_view"]
content = [] ; date = [] ; view = [] ;  like = [] ; tags = [] ; image = []
followers = [] ; total_content = [] ; total_view = []

type = ["snippet", "statistics"]

##2-1 Video information
for video_id in video_list:
    request = youtube.videos().list(part = "snippet,statistics",id = video_id)
    item = request.execute()["items"][0]
    content.append(item["snippet"]["description"].replace("\n", " "))
    date.append(item[type[0]]["publishedAt"])
    view.append(item[type[1]]["viewCount"])
    try:
        like.append(item[type[1]]["likeCount"])
    except:
        like.append(0)
    try:
        tags.append(item["snippet"]["tags"])
    except:
        tags.append([])
    image.append(item["snippet"]["thumbnails"]["default"]["url"])

##2-2 Video Uploader information

    channel_id = item[type[0]]["channelId"]
    video_response = youtube.channels().list(
        id=channel_id,
        part="snippet,statistics"
    ).execute()
    try:
        followers.append(video_response["items"][0]["statistics"]["subscriberCount"])
    except:
        followers.append(0)
    try:
        total_content.append(video_response["items"][0]["statistics"]["videoCount"])
    except:
        total_content.append(0)
    try:
        total_view.append(video_response["items"][0]["statistics"]["viewCount"])
    except:
        total_view.append(0)

total = [content, video_list, date, view, like, tags, url, image, followers, total_content, total_view]
video_dict = dict(zip(dict_keys, total))
df = pd.DataFrame(video_dict)
df.to_csv("youtube.csv")