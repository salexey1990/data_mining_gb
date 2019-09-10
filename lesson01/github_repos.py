import requests
import json

headers={
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

res = requests.get('https://api.github.com/users/salexey1990/repos', headers)

with open("github_repos.json", "w") as write_file:
  json.dump(json.loads(res.content), write_file)