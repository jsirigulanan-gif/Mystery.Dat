#!/usr/bin/env python3
"""
LEMiNO Automated Asset Harvester & Video Cutter
Parses Production Shot List Cue Sheet (.docx) and downloads/cuts footage using yt-dlp and ffmpeg.
"""

import argparse
import os
import re
import subprocess
import sys
import docx

def parse_shot_list(docx_path):
    doc = docx.Document(docx_path)
    shots = []
    current_shot = None

    shot_header_pattern = re.compile(r'---\s*(SHOT-\d+)\s*\[([\d:\.]+)\s*-\s*([\d:\.]+)\s*/\s*([\d\.]+)s\]\s*---')

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue

        match = shot_header_pattern.match(text)
        if match:
            if current_shot:
                shots.append(current_shot)
            shot_id, start_tc, end_tc, duration_str = match.groups()
            current_shot = {
                "id": shot_id,
                "start_tc": start_tc,
                "end_tc": end_tc,
                "duration": float(duration_str),
                "type": "",
                "source": "",
                "reference": "",
                "visual": "",
                "camera": "",
                "graphics": "",
                "voiceover": "",
                "audio": ""
            }
            continue

        if current_shot:
            if text.startswith("Type:"):
                current_shot["type"] = text.replace("Type:", "").strip()
            elif text.startswith("Source:"):
                current_shot["source"] = text.replace("Source:", "").strip()
            elif text.startswith("Reference:"):
                current_shot["reference"] = text.replace("Reference:", "").strip()
            elif text.startswith("Visual:"):
                current_shot["visual"] = text.replace("Visual:", "").strip()
            elif text.startswith("Camera:"):
                current_shot["camera"] = text.replace("Camera:", "").strip()
            elif text.startswith("Graphics:"):
                current_shot["graphics"] = text.replace("Graphics:", "").strip()
            elif text.startswith("Voiceover:"):
                current_shot["voiceover"] = text.replace("Voiceover:", "").strip()
            elif text.startswith("Audio/SFX:"):
                current_shot["audio"] = text.replace("Audio/SFX:", "").strip()

    if current_shot:
        shots.append(current_shot)

    return shots

def extract_search_query(reference_text):
    m = re.search(r"YT:\s*['\"]([^'\"]+)['\"]", reference_text)
    if m:
        return m.group(1)
    cleaned = re.sub(r'^(YT:|Archive:|Reference:)\s*', '', reference_text)
    return cleaned.strip()

def download_and_cut_shot(shot, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    out_filename = f"{shot['id'].lower()}.mp4"
    out_path = os.path.join(output_dir, out_filename)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"[{shot['id']}] Already exists: {out_path}")
        return out_path

    query = extract_search_query(shot["reference"])
    duration = shot["duration"]
    print(f"\n==================================================")
    print(f"[{shot['id']}] Processing: {shot['type']}")
    print(f"Query: '{query}' | Duration: {duration}s")
    print(f"==================================================")

    yt_search_cmd = [
        "/home/keng/.local/bin/yt-dlp",
        "--get-id",
        f"ytsearch1:{query}"
    ]
    try:
        proc = subprocess.run(yt_search_cmd, capture_output=True, text=True, check=True)
        video_id = proc.stdout.strip().split("\n")[0]
        if not video_id:
            print(f"[{shot['id']}] No YouTube video found for query.")
            return None
    except Exception as e:
        print(f"[{shot['id']}] Search failed: {e}")
        return None

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Found YouTube Video: {video_url}")

    temp_raw = f"/tmp/{shot['id']}_raw.mp4"
    if os.path.exists(temp_raw):
        os.remove(temp_raw)

    dl_cmd = [
        "/home/keng/.local/bin/yt-dlp",
        "--download-sections", f"*00:00:10-00:00:{int(10 + duration + 5):02d}",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "-o", temp_raw,
        video_url
    ]
    try:
        subprocess.run(dl_cmd, check=True)
    except Exception as e:
        print(f"Download section failed, falling back to direct stream: {e}")
        return None

    standardize_cmd = [
        "ffmpeg", "-y",
        "-ss", "0",
        "-i", temp_raw,
        "-t", str(duration),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-an",
        out_path
    ]
    try:
        subprocess.run(standardize_cmd, check=True)
        print(f"Successfully created broadcast-grade asset: {out_path}")
        if os.path.exists(temp_raw):
            os.remove(temp_raw)
        return out_path
    except Exception as e:
        print(f"FFmpeg standardization failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="LEMiNO Asset Harvester")
    parser.add_argument("--shot-list", default="/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/4_Full_Production_Shot_List_Doc_15Min.docx", help="Path to Shot List Docx")
    parser.add_argument("--output-dir", default="/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/footage", help="Output directory for clips")
    parser.add_argument("--limit", type=int, default=5, help="Limit number of shots to process")
    parser.add_argument("--dry-run", action="store_true", help="Print shot plan without downloading")
    args = parser.parse_args()

    shots = parse_shot_list(args.shot_list)
    print(f"Parsed {len(shots)} shots from {os.path.basename(args.shot_list)}")

    yt_shots = [s for s in shots if "YouTube" in s["source"]]
    print(f"Total YouTube B-roll shots identified: {len(yt_shots)}")

    if args.dry_run:
        for s in yt_shots[:args.limit]:
            query = extract_search_query(s["reference"])
            print(f"- {s['id']}: [{s['type']}] ({s['duration']}s) -> Query: '{query}'")
        return

    processed = 0
    for s in yt_shots:
        if processed >= args.limit:
            break
        download_and_cut_shot(s, args.output_dir)
        processed += 1

if __name__ == "__main__":
    main()
