import requests # type: ignore
import json

params = {
  "engine": "google_scholar_author",
  "author_id": "SehFB3sAAAAJ",
  "api_key": "044cd4179486a2ec60c518e279336ea584771cd5286a0d7e64452a184fb22345"
}

search = requests.get("https://serpapi.com/search",params=params)
results = search.json()
author = results["author"]
interests = author["interests"]
for interest in interests:
    print(f'Title:{interest['title']}')
    print(f'Link:{interest['link']}')

