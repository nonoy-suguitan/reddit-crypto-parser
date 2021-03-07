from datetime import datetime
import json
import pandas
import praw
import properties
import requests

# Parses through reddit posts and counts the nunmber of times certain words are mentioned.

#add main
#create dictionary of mapping crypto terms
#argument for time range - default 1 week

key = properties.personal_use_script

auth = requests.auth.HTTPBasicAuth(properties.personal_use_script, properties.secret)

data = {'grant_type': 'password',
        'username': properties.username,
        'password': properties.password}

headers = {'User-Agent': properties.user_agent}

def authenticate():
    response = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth,
                            data=data,
                            headers=headers)

    token = response.json()['access_token']

    headers['Authorization'] = f'bearer {token}'

    reddit = praw.Reddit(
        client_id=properties.personal_use_script,
        client_secret=properties.secret,
        user_agent=properties.user_agent,
    )

    return reddit

def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pandas.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df

def main():
    # authenticate and initialize praw
    reddit = authenticate()

    # initialize data frames
    reddit_posts = pandas.DataFrame()
    params = {'limit': 5}

    res = requests.get("https://oauth.reddit.com/r/CryptoCurrency/new",
                       headers=headers,
                       params=params)

    new_df = df_from_response(res)

    reddit_posts = reddit_posts.append(new_df, ignore_index=True)

#    response = requests.get("https://oauth.reddit.com/r/CryptoCurrency/comments/lysxbc",
#                       headers=headers)

#    print(json.dumps(response.json(), indent=4))

    print(reddit_posts)
    print(f"{headers} hello world")

    for index, rows in reddit_posts.iterrows():
        print(rows.id)
        submission = reddit.submission(id=rows.id)

        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print(comment.body)
            print("-----------")

    print(f"{headers} hello world")

if __name__ == "__main__":
    main()
