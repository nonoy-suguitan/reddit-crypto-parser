from datetime import datetime
import json
import pandas
import pprint
import praw
import properties
import requests

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

def ingest_data():
    # initialize data frames
    reddit_posts = pandas.DataFrame()
    params = {'limit': 100}

    
    res = requests.get("https://oauth.reddit.com/r/CryptoCurrency/new",
                       headers=headers,
                       params=params)

    new_df = df_from_response(res)

    reddit_posts = reddit_posts.append(new_df, ignore_index=True)

    return reddit_posts

def process_data(reddit_praw_auth,reddit_posts):
    for index, rows in reddit_posts.iterrows():
        print(rows.id)
        submission = reddit_praw_auth.submission(id=rows.id)

        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print(comment.body)
            print("-----------")
            for coin in properties.coin_dictionary:
                if any(ext in comment.body.lower() for ext in coin):
                    properties.coin_dictionary[coin] += 1


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

def print_inventory(dct):
    #sorted_dictionary = dict(sorted(dct.items(), key=lambda item: item[1]))
    sorted_dictionary = dict(reversed(sorted(dct.items(), key=lambda item: item[1])))
    print("Items held:")
    for item, amount in sorted_dictionary.items():  # dct.iteritems() in Python 2
        if (amount != 0):
            print("{} ({})".format(item, amount))

def main():
    # authenticate and initialize praw
    reddit_praw_auth = authenticate()

    # ingest data
    reddit_posts = ingest_data()

    # process data
    process_data(reddit_praw_auth,reddit_posts)

    # print result
    print_inventory(properties.coin_dictionary)


#random prints
#print(json.dumps(response.json(), indent=4))
#print(reddit_posts)
#print(f"{headers} hello world")

if __name__ == "__main__":
    main()
