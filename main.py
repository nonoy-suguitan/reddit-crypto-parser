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

def main():
    reddit = authenticate()

    #reponse = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    data = pandas.DataFrame()
    params = {'limit': 5}

#    response = requests.get("https://oauth.reddit.com/r/CryptoCurrency/new",
#                       headers=headers,
#                       params=params)

#    response = requests.get("https://oauth.reddit.com/r/CryptoCurrency/comments/lysxbc",
#                       headers=headers)

#    print(json.dumps(response.json(), indent=4))

    print(f"{headers} hello world")
    print(reddit.read_only)


if __name__ == "__main__":
    main()
