import urllib.request
import json
import os
from collections import Counter
from datetime import datetime

url = "https://api.github.com/repos/sidinsearch/superbrain/stargazers"
token = os.environ.get("GITHUB_TOKEN")
headers = {
    "Accept": "application/vnd.github.star+json",
    "User-Agent": "Mozilla/5.0",
    "Authorization": f"Bearer {token}"
}

dates = []
page = 1
while True:
    req = urllib.request.Request(f"{url}?per_page=100&page={page}", headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    if not data: break
    for item in data:
        dt = item['starred_at']
        d = dt.split('T')[0]
        dates.append(d)
    if len(data) < 100: break
    page += 1

print(f"Total stars: {len(dates)}")
