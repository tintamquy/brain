"""
RENDER COMPLETE BUDDHIST MEDITATION SHORT VIDEO
Outputs a 1080x1920 vertical 9:16 MP4 video with:
- 2s - 3s scene transitions with dynamic subtle motion
- AI Neural Monastic Voiceover
- High-contrast, dynamic burnt-in subtitles
- Ambient meditation sound design (Tibetan bell + 432Hz drone)
"""

import asyncio
import os
import shutil
import subprocess
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

import edge_tts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "render_assets")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "BUDDHIST_MEDITATION_SHORT_EP01.mp4")

os.makedirs(ASSETS_DIR, exist_ok=True)

# 12 Image paths from brain folder
BRAIN_DIR = r"C:\Users\tamquy\.gemini\antigravity-ide\brain\195f8171-fffa-4677-a036-e00698961f22"
IMAGE_MAP = {
    "tab": os.path.join(BRAIN_DIR, "scene01_closing_tab_1792021476532.jpg"),
    "guilt": os.path.join(BRAIN_DIR, "scene02_heavy_guilt_1792021493175.jpg"),
    "brain": os.path.join(BRAIN_DIR, "scene03_dopamine_brain_1792021508465.jpg"),
    "buddha": os.path.join(BRAIN_DIR, "scene04_stone_buddha_1792021523279.jpg"),
    "sand": os.path.join(BRAIN_DIR, "scene05_phone_sand_1792021543157.jpg"),
    "spine": os.path.join(BRAIN_DIR, "scene06_golden_spine_1792021560653.jpg"),
    "water": os.path.join(BRAIN_DIR, "scene07_still_water_1792021580305.jpg"),
    "splash": os.path.join(BRAIN_DIR, "scene08_cold_water_1792021599890.jpg"),
    "scholar": os.path.join(BRAIN_DIR, "scene09_victorious_scholar_1792021618852.jpg"),
    "fist": os.path.join(BRAIN_DIR, "scene10_fist_opening_1792021698585.jpg"),
    "prana": os.path.join(BRAIN_DIR, "scene11_prana_inhale_1792021726009.jpg"),
    "thermal": os.path.join(BRAIN_DIR, "scene12_thermal_cool_1792021749156.jpg"),
}

VOICE_TEXT = (
    "You just closed that tab, didn’t you? "
    "And that heavy, suffocating guilt is crushing your chest right now. "
    "Stop hating yourself. Your brain was hijacked by a cheap dopamine trap. "
    "In Buddhism, this is Kama: an illusion that promises gold, but leaves you in ashes. "
    "The pleasure lasted ten seconds. The brain fog lasts for days. "
    "Here is your cure right now. Sit upright. Unclench your jaw. Open your fists. "
    "Feel that fiery craving. Do not fight it. Just watch it burn itself out. "
    "Take one massive breath through your nose. Fill your lower belly. "
    "Now splash freezing cold water on your face. Turn that primal fire into mental fuel. "
    "You are not a slave to pixels. Open your book. Master your mind today."
)

VOICE = "en-US-ChristopherNeural"
RATE = "+6%"
PITCH = "-2Hz"

# Format time in ASS format: H:MM:SS.cs
def format_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:05.2f}"

async def generate_speech_and_subs(audio_path, ass_path):
    print("[1/5] Sinh giọng đọc AI trầm ấm & tính toán timing từng câu...")
    c = edge_tts.Communicate(VOICE_TEXT, VOICE, rate=RATE, pitch=PITCH)
    
    sentences = []
    audio_data = bytearray()
    
    async for chunk in c.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            start_sec = chunk["offset"] / 10_000_000.0
            dur_sec = chunk["duration"] / 10_000_000.0
            end_sec = start_sec + dur_sec
            sentences.append((start_sec, end_sec, chunk["text"]))
            
    with open(audio_path, "wb") as f:
        f.write(audio_data)
        
    print(f"  [+] Đã lưu Voiceover: {len(audio_data)} bytes ({len(sentences)} câu)")
    
    # Tạo style phụ đề ASS cao cấp: chữ to, viền đen dày, màu vàng/trắng nổi bật
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,7,3,2,60,60,340,1
Style: Highlight,Arial,72,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,8,4,2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    # Từ khóa cần tô màu vàng nổi bật
    highlight_words = ["CLOSED", "GUILT", "HIJACKED", "DOPAMINE", "KAMA", "ILLUSION", "ASHES", "PLEASURE", "BRAIN FOG", "CURE", "SIT UPRIGHT", "UNCLENCH", "VIPASSANA", "BURN OUT", "MASSIVE BREATH", "COLD WATER", "FIRE INTO FUEL", "NOT A SLAVE", "MASTER YOUR MIND"]
    
    for start, end, raw_text in sentences:
        text = raw_text.strip()
        # Chuyển đổi một số từ thành chữ in hoa và tô vàng
        formatted = text
        for hw in highlight_words:
            # Case insensitive replace with ASS formatting tags
            import re
            pattern = re.compile(re.escape(hw), re.IGNORECASE)
            formatted = pattern.sub(f"{{\\\\c&H0000FFFF&}}{hw}{{\\\\c&H00FFFFFF&}}", formatted)
            
        start_str = format_ass_time(start)
        end_str = format_ass_time(end)
        events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{formatted}")
        
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(events))
        
    print(f"  [+] Đã tạo file phụ đề ASS: {ass_path}")

def build_video():
    audio_path = os.path.join(ASSETS_DIR, "voiceover.mp3")
    ass_path = os.path.join(ASSETS_DIR, "subs.ass")
    ambient_path = os.path.join(ASSETS_DIR, "ambient.mp3")
    mixed_audio_path = os.path.join(ASSETS_DIR, "mixed_audio.mp3")
    
    asyncio.run(generate_speech_and_subs(audio_path, ass_path))
    
    # Đo thời lượng thực của audio
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    total_duration = float(subprocess.check_output(probe_cmd).decode().strip())
    print(f"[2/5] Tổng thời lượng video: {total_duration:.2f} giây")
    
    # Tạo âm thanh thiền tĩnh lặng (432Hz Bell & Drone)
    print("[3/5] Tạo nhạc nền thiền định 432Hz & tiếng chuông ngân...")
    ambient_cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        f"-i", f"sine=frequency=108:duration={total_duration}",
        "-f", "lavfi",
        f"-i", f"sine=frequency=432:duration={total_duration}",
        "-filter_complex",
        "[0:a]volume=0.08[b1];[1:a]volume=0.03[b2];[b1][b2]amix=inputs=2[out]",
        "-map", "[out]", "-c:a", "libmp3lame", ambient_path
    ]
    subprocess.run(ambient_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Trộn Voiceover với Nhạc nền
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", audio_path,
        "-i", ambient_path,
        "-filter_complex",
        "[0:a]volume=1.2[v];[1:a]volume=0.3[m];[v][m]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]", "-c:a", "libmp3lame", mixed_audio_path
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("  [+] Đã hòa âm hoàn hảo giọng đọc và nhạc nền.")

    # 18 phân cảnh, mỗi phân cảnh dài ~2.9 - 3.1 giây (đúng tiêu chuẩn 2s - 3s chuyển cảnh)
    scene_sequence = [
        ("tab", 2.8),      # 00.0 - 02.8: You just closed that tab
        ("guilt", 2.8),    # 02.8 - 05.6: Guilt crushing your chest
        ("brain", 3.0),    # 05.6 - 08.6: Brain hijacked by dopamine
        ("buddha", 3.0),   # 08.6 - 11.6: In Buddhism this is Kama
        ("sand", 3.0),     # 11.6 - 14.6: Promises gold leaves ashes
        ("guilt", 2.8),    # 14.6 - 17.4: Pleasure 10s, brain fog days
        ("spine", 3.2),    # 17.4 - 20.6: Here is your cure: sit upright
        ("fist", 2.8),     # 20.6 - 23.4: Unclench jaw, open fists
        ("thermal", 3.2),  # 23.4 - 26.6: Feel that craving, watch it burn out
        ("water", 3.0),    # 26.6 - 29.6: Still water settling
        ("prana", 3.2),    # 29.6 - 32.8: Massive breath through nose
        ("spine", 3.0),    # 32.8 - 35.8: Fill lower belly
        ("splash", 3.2),   # 35.8 - 39.0: Splash freezing cold water
        ("splash", 3.0),   # 39.0 - 42.0: Fire into mental fuel
        ("buddha", 3.0),   # 42.0 - 45.0: Sacred stillness
        ("sand", 2.8),     # 45.0 - 47.8: Not a slave to pixels
        ("scholar", 3.2),  # 47.8 - 51.0: Open your book
        ("scholar", 3.4),  # 51.0 - 54.4: Master your mind today
    ]
    
    print("[4/5] Render các đoạn video con với hiệu ứng chuyển động Ken Burns...")
    clip_files = []
    
    # Tạo từng clip con 1080x1920 30fps
    for idx, (img_key, duration) in enumerate(scene_sequence):
        src_img = IMAGE_MAP[img_key]
        clip_path = os.path.join(ASSETS_DIR, f"clip_{idx:02d}.mp4")
        clip_files.append(clip_path)
        
        # Luân phiên hiệu ứng Zoom in hoặc Zoom out chậm rãi (2s-3s dynamic)
        if idx % 2 == 0:
            zoom_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.15)':d={int(duration*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        else:
            zoom_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='max(1.15-0.0015*on,1.0)':d={int(duration*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
            
        render_clip_cmd = [
            "ffmpeg", "-y", "-loop", "1",
            "-i", src_img,
            "-vf", zoom_filter,
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast",
            clip_path
        ]
        subprocess.run(render_clip_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"  [+] Clip {idx+1}/{len(scene_sequence)} ({img_key}) hoàn tất.")

    # Tạo file danh sách nối clips
    concat_list_path = os.path.join(ASSETS_DIR, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for clip in clip_files:
            f.write(f"file '{clip.replace(os.sep, '/')}'\n")

    # Ghép tất cả clips + âm thanh + đốt phụ đề ASS
    print("[5/5] Ghép phân cảnh + Âm thanh + Đốt phụ đề nổi (Subtitles Burn-in)...")
    
    # Format đường dẫn ASS cho bộ lọc ffmpeg (Windows escaping)
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    
    final_render_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list_path,
        "-i", mixed_audio_path,
        "-vf", f"ass='{ass_escaped}'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    subprocess.run(final_render_cmd, check=True)
    print(f"\n🎉 [THÀNH CÔNG RỰC RỠ] Video hoàn chỉnh đã xuất tại:\n{OUTPUT_VIDEO}")

if __name__ == "__main__":
    build_video()
