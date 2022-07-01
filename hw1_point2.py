from pprint import pprint

import requests

access_token = 'vk1.убрал'

expires_in = 86400
user_id = 59958534

url = f'https://api.vk.com/method/friends.getOnline?v=5.131&access_token={access_token}'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

friendsOnline = requests.get(url)
friendsObj = friendsOnline.json()
friendsStr = ','.join(map(str, friendsObj['response']))

url = f'https://api.vk.com/method/users.get?user_id={friendsStr}&v=5.131&access_token={access_token}'
friends = requests.get(url)
pprint(friends.json())


