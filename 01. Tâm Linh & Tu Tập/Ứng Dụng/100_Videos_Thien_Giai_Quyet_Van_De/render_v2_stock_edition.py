"""
RENDER V2: REAL STOCK VIDEO EDITION + SILKY SMOOTH PAN
- Uses real high-definition cinematic stock footage (typing, stress, fire, meditation, waterfall, ocean, studying)
- Images use pure linear horizontal/vertical pan (no zoom wobble/jitter)
- 2s - 3s dynamic cut pacing
- High-contrast, dynamic burnt-in subtitles
- Tibetan bell & 432Hz ambient meditation sound
"""

import asyncio
import os
import subprocess
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_DIR = os.path.join(BASE_DIR, "stock_videos")
BRAIN_DIR = r"C:\Users\tamquy\.gemini\antigravity-ide\brain\195f8171-fffa-4677-a036-e00698961f22"
ASSETS_DIR = os.path.join(BASE_DIR, "render_assets_v2")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "BUDDHIST_MEDITATION_SHORT_EP01_CINEMATIC.mp4")

os.makedirs(ASSETS_DIR, exist_ok=True)

# File sources
MEDIA_SOURCES = {
    # Stock Videos
    "v_typing": os.path.join(STOCK_DIR, "typing.mp4"),
    "v_stress": os.path.join(STOCK_DIR, "stress.mp4"),
    "v_fire": os.path.join(STOCK_DIR, "fire.mp4"),
    "v_meditate": os.path.join(STOCK_DIR, "meditate.mp4"),
    "v_waterfall": os.path.join(STOCK_DIR, "waterfall.mp4"),
    "v_breathe": os.path.join(STOCK_DIR, "breathe.mp4"),
    "v_ocean": os.path.join(STOCK_DIR, "ocean.mp4"),
    "v_study_notes": os.path.join(STOCK_DIR, "study_notes.mp4"),
    "v_study_boy": os.path.join(STOCK_DIR, "study_boy.mp4"),
    
    # High-Definition 8K Images for iconic spiritual/medical moments
    "img_brain": os.path.join(BRAIN_DIR, "scene03_dopamine_brain_1792021508465.jpg"),
    "img_buddha": os.path.join(BRAIN_DIR, "scene04_stone_buddha_1792021523279.jpg"),
    "img_spine": os.path.join(BRAIN_DIR, "scene06_golden_spine_1792021560653.jpg"),
    "img_thermal": os.path.join(BRAIN_DIR, "scene12_thermal_cool_1792021749156.jpg"),
    "img_splash": os.path.join(BRAIN_DIR, "scene08_cold_water_1792021599890.jpg"),
    "img_scholar": os.path.join(BRAIN_DIR, "scene09_victorious_scholar_1792021618852.jpg")
}

# 18 Cuts sequence (2.8s - 3.2s per cut, matching exactly 54.4s audio)
TIMELINE = [
    ("v_typing", 0.0, 2.8, "video", 2.0),       # start at 2s in stock video
    ("v_stress", 2.8, 5.8, "video", 1.0),
    ("img_brain", 5.8, 8.6, "image_pan_x", 0.0),
    ("img_buddha", 8.6, 11.6, "image_pan_y", 0.0),
    ("v_fire", 11.6, 14.5, "video", 0.5),
    ("v_stress", 14.5, 17.5, "video", 5.0),
    ("v_meditate", 17.5, 20.5, "video", 1.0),
    ("img_spine", 20.5, 23.5, "image_pan_y", 0.0),
    ("img_thermal", 23.5, 26.5, "image_pan_x", 0.0),
    ("v_waterfall", 26.5, 29.5, "video", 3.0),
    ("v_breathe", 29.5, 32.5, "video", 2.0),
    ("v_ocean", 32.5, 35.5, "video", 1.5),
    ("img_splash", 35.5, 39.0, "image_pan_x", 0.0),
    ("v_fire", 39.0, 42.0, "video", 3.5),
    ("img_buddha", 42.0, 45.0, "image_pan_x", 0.0),
    ("v_study_notes", 45.0, 48.0, "video", 2.0),
    ("v_study_boy", 48.0, 51.5, "video", 1.0),
    ("img_scholar", 51.5, 54.4, "image_pan_y", 0.0)
]

def render_clip(clip_id, media_key, duration, media_type, start_offset, out_path):
    src = MEDIA_SOURCES[media_key]
    
    if media_type == "video":
        # Scale to fill 1080x1920 with center crop, 30fps
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,fps=30"
        cmd = [
            "ffmpeg", "-y", "-ss", str(start_offset),
            "-i", src,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast",
            "-an", out_path
        ]
    elif media_type == "image_pan_x":
        # Pure silky horizontal pan without any zoom wobble
        vf = f"scale=1200:2133,crop=1080:1920:x='(1200-1080)*t/{duration}':y='(2133-1920)/2',fps=30"
        cmd = [
            "ffmpeg", "-y", "-loop", "1",
            "-i", src,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast",
            out_path
        ]
    elif media_type == "image_pan_y":
        # Pure silky vertical pan from top to bottom
        vf = f"scale=1200:2133,crop=1080:1920:x='(1200-1080)/2':y='(2133-1920)*t/{duration}',fps=30"
        cmd = [
            "ffmpeg", "-y", "-loop", "1",
            "-i", src,
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast",
            out_path
        ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def main():
    print("=" * 60)
    print("BẮT ĐẦU DỰNG VIDEO THÀNH PHẨM V2 (STOCK FOOTAGE + SILKY PAN)")
    print("=" * 60)
    
    clip_files = []
    for idx, (media_key, start_t, end_t, m_type, offset) in enumerate(TIMELINE):
        dur = round(end_t - start_t, 2)
        out_clip = os.path.join(ASSETS_DIR, f"clip_{idx:02d}.mp4")
        clip_files.append(out_clip)
        print(f"[*] Rendering Cut {idx+1:02d}/{len(TIMELINE)}: [{m_type.upper()}] {media_key} ({dur}s)...")
        render_clip(idx, media_key, dur, m_type, offset, out_clip)
        
    concat_txt = os.path.join(ASSETS_DIR, "concat_v2.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clip_files:
            f.write(f"file '{c.replace(os.sep, '/')}'\n")
            
    mixed_audio = os.path.join(BASE_DIR, "render_assets", "mixed_audio.mp3")
    subs_ass = os.path.join(BASE_DIR, "render_assets", "subs.ass")
    ass_escaped = subs_ass.replace("\\", "/").replace(":", "\\:")
    
    print("[*] Đang ghép tất cả phân cảnh, hòa âm và đốt phụ đề điện ảnh...")
    final_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", mixed_audio,
        "-vf", f"ass='{ass_escaped}'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(final_cmd, check=True)
    print(f"\n🎉 [HOÀN TẤT V2] Video chất lượng điện ảnh đã xuất tại:\n{OUTPUT_VIDEO}")

if __name__ == "__main__":
    main()
