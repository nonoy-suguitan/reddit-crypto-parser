import json
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

headers = {'User-Agent': 'stakemyeth/0.0.1'}

def authenticate():
    response = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth,
                            data=data,
                            headers=headers)

    token = response.json()['access_token']

    headers['Authorization'] = f'bearer {token}'
    return response

def main():
    authenticate()

    reponse = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    print(json.dumps(reponse.json(), indent=4))

    print(f"{headers} hello world")


if __name__ == "__main__":
    main()
