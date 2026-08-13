import urllib.request
import json
import re

REPO = "sidinsearch/superbrain"
URL = f"https://api.github.com/repos/{REPO}/contributors"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as response:
    contributors = json.loads(response.read().decode())

contributors.append({
    "login": "cursoragent",
    "html_url": "https://github.com/cursoragent",
    "avatar_url": "https://github.com/cursoragent.png"
})
contributors.append({
    "login": "copilot-swe-agent",
    "html_url": "https://github.com/apps/copilot-swe-agent",
    "avatar_url": "https://avatars.githubusercontent.com/in/1143301?v=4"
})

html_parts = []
for c in contributors:
    login = c.get('login')
    html_url = c.get('html_url')
    # Request high-dps size
    avatar_url = c.get('avatar_url', '')
    if '?' in avatar_url:
        avatar_url += "&s=400"
    else:
        avatar_url += "?size=400"

    # Rounded square styling (High-res source mapped to 48x48 element)
    tag = f'<a href="{html_url}"><img src="{avatar_url}" width="48" height="48" alt="{login}" style="border-radius: 8px;"></a>'
    html_parts.append(tag)

new_content = " ".join(html_parts)

with open("README.md", "r", encoding="utf-8") as f:
    text = f.read()

pattern = r"(<!-- contributors:start -->\n).*?(<!-- contributors:end -->)"
replacement = r"\1" + new_content + r"\n\2"

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Updated contributors in README.md")
