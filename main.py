import coinmarketcap
import json
import nltk
import pandas
import pprint
import praw
import properties
import requests
from nltk.corpus import stopwords
from datetime import datetime

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
    params = {'limit': 50}

    # loop through 10 times (returning 1K posts)
    for i in range(1):
        res = requests.get("https://oauth.reddit.com/r/CryptoCurrency/new",
                        headers=headers,
                        params=params)

        # get dataframe from response
        new_df = df_from_response(res)

        # take the final row (oldest entry)
        row = new_df.iloc[len(new_df)-1]
        # create fullname
        fullname = row['kind'] + '_' + row['id']
        # add/update fullname in params
        params['after'] = fullname

        # append new_df to data
        reddit_posts = reddit_posts.append(new_df, ignore_index=True)

    return reddit_posts

def process_data(reddit_praw_auth,reddit_posts,coin_dictionary):
    for index, rows in reddit_posts.iterrows():
        print(rows.id)
        submission = reddit_praw_auth.submission(id=rows.id)
        submission.comment_sort = "top"
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            remove_special_chars = comment.body.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            lower_string_split = remove_special_chars.lower().split()
            comment_filter_out_stopwords = [word for word in lower_string_split if word not in stopwords.words('english')]

            print(comment_filter_out_stopwords)

            for coin in coin_dictionary:
                if any(ext in comment_filter_out_stopwords for ext in coin):
                    coin_dictionary[coin] += 1


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
    sorted_dictionary = dict(reversed(sorted(dct.items(), key=lambda item: item[1])))
    print("Items held:")
    for item, amount in sorted_dictionary.items():  # dct.iteritems() in Python 2
        if (amount > 9):
            print("{} ({})".format(item, amount))

def main():
    # authenticate and initialize
    reddit_praw_auth = authenticate()
    coin_listing = coinmarketcap.ingest_coin_listing()
    coin_dictionary = coinmarketcap.process_data(coin_listing)

    # ingest data
    reddit_posts = ingest_data()

    # process data
    process_data(reddit_praw_auth,reddit_posts,coin_dictionary)

    # print result
    print_inventory(coin_dictionary)

#random prints
#print(json.dumps(response.json(), indent=4))
#print(reddit_posts)
#print(f"{headers} hello world")

if __name__ == "__main__":
    main()
