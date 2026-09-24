#!/usr/bin/env python3
import os
import subprocess

POOL_DIR = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/broll_pool"
os.makedirs(POOL_DIR, exist_ok=True)

VIDEOS = [
    {
        "name": "e3_trailer.mp4",
        "url": "https://www.youtube.com/watch?v=taNGuF_k5Ao",
        "max_dur": 225
    },
    {
        "name": "notre_dame_tour.mp4",
        "url": "https://www.youtube.com/watch?v=kRN41A4XON8",
        "max_dur": 300
    },
    {
        "name": "paris_freeroam.mp4",
        "url": "https://www.youtube.com/watch?v=aLuZBLBCXoA",
        "max_dur": 300
    },
    {
        "name": "face_glitch.mp4",
        "url": "https://www.youtube.com/watch?v=T2zgtwLi15w",
        "max_dur": 15
    }
]

for v in VIDEOS:
    out_file = os.path.join(POOL_DIR, v["name"])
    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000000:
        print(f"[EXISTS] {v['name']} already downloaded.")
        continue

    print(f"\n[DOWNLOADING] {v['name']} ({v['url']})...")
    temp_file = os.path.join(POOL_DIR, f"temp_{v['name']}")
    dl_cmd = [
        "/home/keng/.local/bin/yt-dlp",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "--download-sections", f"*00:00:00-00:0{int(v['max_dur']//60):01d}:{int(v['max_dur']%60):02d}",
        "-o", temp_file,
        v["url"]
    ]
    try:
        subprocess.run(dl_cmd, check=True)
        # Standardize to 1080p 30fps
        std_cmd = [
            "ffmpeg", "-y",
            "-i", temp_file,
            "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
            "-an",
            out_file
        ]
        subprocess.run(std_cmd, check=True)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"[READY] {out_file} ({os.path.getsize(out_file)//1024//1024} MB)")
    except Exception as e:
        print(f"[ERROR] Failed {v['name']}: {e}")
