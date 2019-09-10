import requests
import json

headers={
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

access_token = '???'

params = {
  'v': 5.52,
  'access_token': access_token,
}


res = requests.get('https://api.vk.com/method/friends.getOnline', headers=headers, params=params)

with open("vk_friends.json", "w") as write_file:
  json.dump(json.loads(res.content), write_file)