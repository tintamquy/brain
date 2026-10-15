import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for query in ['wash-face', 'cold-water', 'ocean', 'breathe', 'running']:
    url = f'https://mixkit.co/free-stock-video/{query}/'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            urls = re.findall(r'\"contentUrl\":\"(https://assets\.mixkit\.co/videos/[^\"]+\.mp4)\"', html)
            print(f"[{query}]:")
            for u in urls[:3]:
                print(f"  {u}")
    except Exception as e:
        print(f"[{query}] Error:", e)
