import urllib.request
import re
import json
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

categories = ['typing', 'water', 'study', 'stress', 'fire', 'focus']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

results = {}

for cat in categories:
    url = f'https://mixkit.co/free-stock-video/{cat}/'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract VideoObjects
            scripts = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
            cat_videos = []
            for s in scripts:
                try:
                    data = json.loads(s)
                    graph = data.get('@graph', [data])
                    for item in graph:
                        if item.get('@type') == 'VideoObject' and 'contentUrl' in item:
                            cat_videos.append({
                                'name': item.get('name'),
                                'url': item.get('contentUrl'),
                                'desc': item.get('description', '')
                            })
                except:
                    pass
            results[cat] = cat_videos
            print(f"[{cat}] Tìm thấy {len(cat_videos)} videos.")
            for v in cat_videos[:3]:
                print(f"  - {v['name']}: {v['url']}")
    except Exception as e:
        print(f"Lỗi {cat}: {e}")

with open('stock_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
