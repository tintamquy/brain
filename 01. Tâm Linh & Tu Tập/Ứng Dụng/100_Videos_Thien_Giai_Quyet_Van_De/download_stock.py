import urllib.request
import os
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_DIR = os.path.join(BASE_DIR, "stock_videos")
os.makedirs(STOCK_DIR, exist_ok=True)

VIDEOS = {
    "typing": "https://assets.mixkit.co/videos/1781/1781-1080.mp4",
    "stress": "https://assets.mixkit.co/videos/4701/4701-1080.mp4",
    "fire": "https://assets.mixkit.co/videos/52284/52284-1080.mp4",
    "meditate": "https://assets.mixkit.co/videos/4397/4397-1080.mp4",
    "waterfall": "https://assets.mixkit.co/active_storage/video_items/100174/1721166924/100174-video-1080.mp4",
    "study_boy": "https://assets.mixkit.co/videos/4761/4761-1080.mp4",
    "study_notes": "https://assets.mixkit.co/videos/50109/50109-1080.mp4"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for key, url in VIDEOS.items():
    dest = os.path.join(STOCK_DIR, f"{key}.mp4")
    if os.path.exists(dest) and os.path.getsize(dest) > 100000:
        print(f"[SKIP] Đã có {key}.mp4 ({os.path.getsize(dest)} bytes)")
        continue
    print(f"[*] Đang tải {key} từ {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        print(f"  [+] Xong {key}.mp4 ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"  [-] Lỗi tải {key}: {e}")
