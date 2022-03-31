import base64
import pandas as pd
import requests
import json

#1. Twitter API developer key
client_key = 'key'
client_secret = 'secret'

#2. Conver into b64 encoded format
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

#3. make a url for request  
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

#4. HEADER 
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

#5. Authentication Data section 
auth_data = {
    'grant_type': 'client_credentials'
}

#6. To check status, POST request!
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

#7. Define Bearer token
access_token = auth_resp.json()['access_token']

#8. Search HEADER 
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

#9. SEARCH TWEET
search_params = {
    'q':'keyword',
    'result_type': 'recent', # 'mixed' or 'popular'
    'count': 100, #default:15, max:100
    'retryonratelimit':True,
}

search_url = '{}1.1/search/tweets.json'.format(base_url)
search_resp = requests.get(
    search_url, headers=search_headers,
    params=search_params
)

items = json.loads(search_resp.content)["statuses"]
result = []

for item in items:
    if "RT" in item["text"]:    #Pass RT tweets
        pass
    else:
        content = item["text"]
        id = item["user"]["screen_name"]
        date = item["created_at"]
        like = item["favorite_count"]
        retweet = item["retweet_count"]
        url = "https://twitter.com/" + id + "/status/" + item["id_str"]
        try:
            image = item["entities"]["media"][0]["media_url"]
        except:
            image = ""
        followers = item["user"]["followers_count"]
        total_content = item["user"]["statuses_count"]
        user_favorites = item["user"]["favourites_count"]

        data = [content, id, date, like, retweet, url, image, followers, total_content, user_favorites]
        result.append(data)
data = pd.DataFrame(result, columns = ["content", "id", "date", "like", "retweet", "url", "image", "followers", "total_content", "user_favorites"])

data.to_csv("tweet.csv")


