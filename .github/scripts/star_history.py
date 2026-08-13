import urllib.request
import json
import os
from datetime import datetime

def main():
    token = os.environ.get("GITHUB_TOKEN")
    url = "https://api.github.com/repos/sidinsearch/superbrain/stargazers"
    headers = {"Accept": "application/vnd.github.star+json", "User-Agent": "Mozilla/5.0"}
    if token: headers["Authorization"] = f"Bearer {token}"
    
    dates = []
    page = 1
    while True:
        req = urllib.request.Request(f"{url}?per_page=100&page={page}", headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        if not data: break
        for item in data:
            if 'starred_at' in item:
                d = item['starred_at'].split('T')[0]
                dates.append(d)
        if len(data) < 100: break
        page += 1
    
    if not dates: return
    dates.sort()
    
    start_date = datetime.strptime(dates[0], "%Y-%m-%d")
    end_date = datetime.now()  # up to current time
    days = (end_date - start_date).days
    
    width = 800
    height = 400
    padding_x = 60
    padding_y = 60
    max_stars = len(dates)
    
    # Start at 0,0
    points = [f"{padding_x},{height - padding_y}"]
    cumulative = 0
    
    for date_str in dates:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        cumulative += 1
        x = padding_x + ((dt - start_date).days / max(days, 1)) * (width - 2*padding_x)
        y = height - padding_y - (cumulative / max(max_stars, 1)) * (height - 2*padding_y)
        points.append(f"{x},{y}")
        
    # Final point at current time
    x = padding_x + (width - 2*padding_x)
    y = height - padding_y - (cumulative / max(max_stars, 1)) * (height - 2*padding_y)
    points.append(f"{x},{y}")
        
    path_d = "M " + " L ".join(points)
    
    grid_lines = ""
    for i in range(5):
        y = height - padding_y - i * ((height - 2*padding_y) / 4)
        grid_lines += f'<line x1="{padding_x}" y1="{y}" x2="{width - padding_x}" y2="{y}" stroke="#30363d" stroke-width="1" />\n'
        stars_at_y = int(i * max_stars / 4)
        grid_lines += f'<text x="{padding_x - 10}" y="{y + 5}" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="end">{stars_at_y}</text>\n'

    # X axis labels
    labels_x = ""
    start_str = start_date.strftime("%b %Y")
    end_str = end_date.strftime("%b %Y")
    mid_date = start_date + (end_date - start_date)/2
    mid_str = mid_date.strftime("%b %Y")
    
    labels_x += f'<text x="{padding_x}" y="{height - padding_y + 20}" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="middle">{start_str}</text>\n'
    labels_x += f'<text x="{padding_x + (width-2*padding_x)/2}" y="{height - padding_y + 20}" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="middle">{mid_str}</text>\n'
    labels_x += f'<text x="{width - padding_x}" y="{height - padding_y + 20}" fill="#8b949e" font-family="sans-serif" font-size="12" text-anchor="middle">{end_str}</text>\n'

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{width}" height="{height}" fill="#0d1117" rx="10" />
    {grid_lines}
    {labels_x}
    <path d="{path_d}" fill="none" stroke="#2f81f7" stroke-width="3" />
    <!-- Gradient Fill -->
    <path d="{path_d} L {width - padding_x} {height - padding_y} L {padding_x} {height - padding_y} Z" fill="url(#grad)" opacity="0.3" />
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#2f81f7" stop-opacity="1"/>
            <stop offset="100%" stop-color="#2f81f7" stop-opacity="0"/>
        </linearGradient>
    </defs>
    <text x="{width/2}" y="30" fill="#e6edf3" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">sidinsearch/superbrain Star History</text>
    </svg>"""
    
    with open("star_history.svg", "w") as f:
        f.write(svg)
    print("Generated star_history.svg")

main()
