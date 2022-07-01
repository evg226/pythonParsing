import requests
from pprint import pprint
import json

username = 'evg226'
url = f'https://api.github.com/users/{username}/repos'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

response = requests.get(url, headers=headers)
repositories = response.json()

with open('data.json', 'w') as f:
    json.dump(repositories, f)

# pprint(repositories)
for repository in repositories:
    print(repository['full_name'])
    print('Browser: ' + repository['html_url'])
