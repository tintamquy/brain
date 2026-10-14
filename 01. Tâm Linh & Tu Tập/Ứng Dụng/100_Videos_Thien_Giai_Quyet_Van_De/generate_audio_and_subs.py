"""
HỆ THỐNG TỰ ĐỘNG HÓA SẢN XUẤT AUDIO & SUBTITLE CHO 100 VIDEO THIỀN PHẬT GIÁO
Sử dụng AI Neural Voice (Edge-TTS hoàn toàn miễn phí & chất lượng cao)
"""

import asyncio
import os
import sys

# Khắc phục lỗi hiển thị tiếng Việt trên terminal Windows (cp1252)
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

import edge_tts

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(OUTPUT_DIR, "output_audio")
SUB_DIR = os.path.join(OUTPUT_DIR, "output_subs")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(SUB_DIR, exist_ok=True)

# Giọng đọc chuẩn: en-US-ChristopherNeural (Trầm ấm, nội lực, uy nghiêm)
VOICE = "en-US-ChristopherNeural"
RATE = "-6%"    # Đọc chậm hơn một chút để tạo sự tĩnh lặng, trầm định
PITCH = "-3Hz"  # Tông trầm uy lực

SCRIPTS = [
    {
        "id": "video_01_lust_cure",
        "title": "You Just Relapsed Again",
        "pillar": "Pillar 1 - Overcoming Lust",
        "text": (
            "You just closed that tab, didn’t you? And right now, that heavy, dirty guilt is crushing your chest. "
            "Stop hating yourself. Your brain was just hijacked by a dopamine trap. "
            "In Buddhism, this is not a sin. It is Kama—an illusion that promises gold but leaves you with ashes. "
            "That pixel woman is not real. The pleasure lasted ten seconds. The brain fog lasts for days. "
            "Here is your cure right now. Do not run. Sit up straight. "
            "Put both feet flat on the floor. Unclench your jaw. Drop your shoulders. "
            "Close your eyes. Feel the physical sensation of craving. Where is it? In your gut? In your chest? "
            "In Vipassana, whatever you observe loses its power. Do not fight it. Just watch it burn itself out. "
            "Take one massive breath through your nose. Fill your lower belly for 4 seconds. "
            "Now exhale slowly through your mouth for 6 seconds. Release the shame. "
            "Wash your face with freezing cold water. That primal fire is now your fuel. "
            "You are not a slave to pixels. Open your book. Master your mind today."
        ),
        "srt_cues": [
            ("00:00:00,000", "00:00:02,500", "You just CLOSED that tab..."),
            ("00:00:02,500", "00:00:05,000", "That heavy GUILT is crushing you."),
            ("00:00:05,000", "00:00:07,500", "Your brain was HIJACKED by dopamine."),
            ("00:00:07,500", "00:00:10,000", "It's not a sin. It's an ILLUSION."),
            ("00:00:10,000", "00:00:12,500", "Pleasure: 10 seconds. BRAIN FOG: Days."),
            ("00:00:12,500", "00:00:15,000", "Here is your CURE. Sit up straight."),
            ("00:00:15,000", "00:00:18,000", "Feet flat. UNCLENCH your jaw."),
            ("00:00:18,000", "00:00:21,000", "Feel the urge: WHERE IS IT?"),
            ("00:00:21,000", "00:00:24,000", "Don't fight it. WATCH IT BURN OUT."),
            ("00:00:24,000", "00:00:27,000", "Inhale DEEP: 4 seconds."),
            ("00:00:27,000", "00:00:30,000", "Exhale slow... RELEASE THE SHAME."),
            ("00:00:30,000", "00:00:33,000", "Freeze your face. FIRE IS NOW FUEL."),
            ("00:00:33,000", "00:00:36,000", "You are NOT a slave. MASTER YOUR MIND.")
        ]
    },
    {
        "id": "video_35_anger_cure",
        "title": "You Just Slammed Your Door",
        "pillar": "Pillar 2 - Taming Anger",
        "text": (
            "You just slammed that door. Your hands are shaking. Your chest is on fire. "
            "You want to scream. You want them to suffer the way you are hurting right now. "
            "Listen to the Buddha: Holding onto anger is like grasping a hot coal to throw at someone else. "
            "They don't feel the burn. You are the one getting destroyed. "
            "Open your fist. Drop the coal right now. "
            "Apply the 3-Second Monastic Rule. Do not speak. Swallow your saliva. "
            "Unclench your back teeth. Separate your teeth by two millimeters. When the body softens, the rage has no fuel. "
            "Understand this: Hurt people hurt people. Their harsh words came from their own fear and stress. "
            "Inhale deeply. Send cooling ice water straight into your burning heart. Hold it for 3 seconds. "
            "Exhale: I will not let outside chaos destroy my inner kingdom. "
            "Anyone who can make you angry is your master. Today, you take back your crown. "
            "Step out of that room. Keep your silence. True strength is total silence under fire."
        ),
        "srt_cues": [
            ("00:00:00,000", "00:00:02,500", "You slammed the door. CHEST ON FIRE."),
            ("00:00:02,500", "00:00:05,000", "You want to SCREAM."),
            ("00:00:05,000", "00:00:07,500", "Anger is a HOT COAL..."),
            ("00:00:07,500", "00:00:10,000", "They don't feel it. YOU ARE BURNING."),
            ("00:00:10,000", "00:00:12,500", "DROP THE COAL. Right now."),
            ("00:00:12,500", "00:00:15,500", "The 3-SECOND RULE. Do not speak."),
            ("00:00:15,500", "00:00:18,500", "Separate your teeth. KILL THE FUEL."),
            ("00:00:18,500", "00:00:21,500", "Hurt people HURT PEOPLE."),
            ("00:00:21,500", "00:00:24,500", "Inhale ice water. COOL YOUR HEART."),
            ("00:00:24,500", "00:00:27,500", "I won't let chaos DESTROY MY KINGDOM."),
            ("00:00:27,500", "00:00:31,000", "Who makes you angry IS YOUR MASTER."),
            ("00:00:31,000", "00:00:35,000", "Take your crown back. STAY SILENT.")
        ]
    },
    {
        "id": "video_68_brainfog_cure",
        "title": "Read 5 Times Zero Retention",
        "pillar": "Pillar 3 - Focus & Study Retention",
        "text": (
            "You've read this exact paragraph five times, and remembered zero words. "
            "Your eyes are scanning, but your mind is thousands of miles away in a digital fog. "
            "Buddhism calls this Markata-citta, the wild Monkey Mind, swinging helplessly between dopamine hits. "
            "You cannot force a muddy glass of water to be clear by stirring it harder. "
            "You must let it sit completely still. Stop reading right now. Close the book. "
            "Put your phone in a drawer across the room. Remove the parasite. "
            "Sit upright. Imagine your spine is a stack of gold coins balanced to the sky. "
            "Now, count ten conscious breaths at the tip of your nose. Inhale one, exhale one. "
            "If your mind wanders to a text or game, gently pull it back to the breath. No judgment. "
            "Open the page. Use your index finger as a physical anchor. Wherever the finger points, your whole universe lives there. "
            "Read word by word. Not to finish the book, but to understand this single sentence. "
            "The fog is gone. The lake is still. Your memory is now a photographic lens. "
            "You are not dumb. You were just scattered. Focus now. Slay the exam."
        ),
        "srt_cues": [
            ("00:00:00,000", "00:00:02,500", "5 times... ZERO RETENTION."),
            ("00:00:02,500", "00:00:05,000", "Your mind is in a DIGITAL FOG."),
            ("00:00:05,000", "00:00:07,500", "MONKEY MIND. Addicted to hits."),
            ("00:00:07,500", "00:00:10,000", "Stop stirring the MUDDY WATER."),
            ("00:00:10,000", "00:00:12,500", "Stop reading. CLOSE THE BOOK."),
            ("00:00:12,500", "00:00:15,000", "Put phone away. KILL THE PARASITE."),
            ("00:00:15,000", "00:00:18,000", "Spine straight like a STACK OF GOLD COINS."),
            ("00:00:18,000", "00:00:21,000", "Count 1 to 10 at TIP OF YOUR NOSE."),
            ("00:00:21,000", "00:00:24,000", "Mind wandered? PULL IT BACK."),
            ("00:00:24,000", "00:00:27,000", "Your finger is an ANCHOR."),
            ("00:00:27,000", "00:00:30,000", "One sentence: FULL UNDERSTANDING."),
            ("00:00:30,000", "00:00:33,000", "The fog is gone. MIND IS A LENS."),
            ("00:00:33,000", "00:00:36,000", "You are NOT dumb. FOCUS AND SLAY.")
        ]
    }
]

def generate_srt_content(cues):
    srt_lines = []
    for index, (start, end, text) in enumerate(cues, start=1):
        srt_lines.append(f"{index}\n{start} --> {end}\n{text}\n")
    return "\n".join(srt_lines)

async def generate_audio_for_item(item):
    audio_path = os.path.join(AUDIO_DIR, f"{item['id']}.mp3")
    sub_path = os.path.join(SUB_DIR, f"{item['id']}.srt")
    
    print(f"[*] Đang sinh giọng đọc: {item['title']}...")
    communicate = edge_tts.Communicate(text=item['text'], voice=VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(audio_path)
    print(f"  [+] Đã lưu file âm thanh: {audio_path}")
    
    # Ghi file phụ đề SRT
    srt_content = generate_srt_content(item['srt_cues'])
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"  [+] Đã lưu file phụ đề SRT: {sub_path}")

async def main():
    print("=" * 60)
    print("BẮT ĐẦU SINH TỰ ĐỘNG VOICE-OVER & PHỤ ĐỀ CHO CÁC TẬP MẪU")
    print(f"Giọng đọc AI: {VOICE} | Tốc độ: {RATE} | Âm vực: {PITCH}")
    print("=" * 60)
    
    for item in SCRIPTS:
        await generate_audio_for_item(item)
        
    print("\n[V] HOÀN TẤT! Bạn có thể mở CapCut / Premiere và kéo thả các file audio và srt vào ngay!")

if __name__ == "__main__":
    asyncio.run(main())
