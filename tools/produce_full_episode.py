#!/usr/bin/env python3
"""
LEMiNO 15-Minute Full Documentary Master Producer
Renders and sequences all 172 shots, mixes broadcast audio with sidechain ducking,
and exports the complete 15-minute Master Documentary MP4.
"""

import os
import re
import subprocess
import sys
import docx

FONT_SERIF = "/home/keng/.local/share/lemino_fonts/serif.ttf"
FONT_THAI = "/home/keng/.local/share/lemino_fonts/thai.ttf"

def parse_all_shots(docx_path):
    doc = docx.Document(docx_path)
    shots = []
    current_shot = None
    header_re = re.compile(r'---\s*(SHOT-\d+)\s*\[([\d:\.]+)\s*-\s*([\d:\.]+)\s*/\s*([\d\.]+)s\]\s*---')

    for p in doc.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        m = header_re.match(t)
        if m:
            if current_shot:
                shots.append(current_shot)
            sid, s_tc, e_tc, dur = m.groups()
            current_shot = {
                "id": sid,
                "start_tc": s_tc,
                "end_tc": e_tc,
                "duration": float(dur),
                "type": "",
                "source": "",
                "reference": "",
                "visual": "",
                "camera": "",
                "graphics": "",
                "voiceover": ""
            }
            continue
        if current_shot:
            if t.startswith("Type:"): current_shot["type"] = t.replace("Type:", "").strip()
            elif t.startswith("Source:"): current_shot["source"] = t.replace("Source:", "").strip()
            elif t.startswith("Reference:"): current_shot["reference"] = t.replace("Reference:", "").strip()
            elif t.startswith("Visual:"): current_shot["visual"] = t.replace("Visual:", "").strip()
            elif t.startswith("Camera:"): current_shot["camera"] = t.replace("Camera:", "").strip()
            elif t.startswith("Graphics:"): current_shot["graphics"] = t.replace("Graphics:", "").strip()
            elif t.startswith("Voiceover:"): current_shot["voiceover"] = t.replace("Voiceover:", "").strip()

    if current_shot:
        shots.append(current_shot)
    return shots

def render_shot_clip(shot, footage_dir, out_dir, txt_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{shot['id'].lower()}_ready.mp4")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        return out_path

    footage_path = os.path.join(footage_dir, f"{shot['id'].lower()}.mp4")
    dur = shot["duration"]
    gfx = shot["graphics"].strip()

    # Base subtitle file
    sub_title_file = os.path.join(txt_dir, "doc_subtitle.txt")
    if not os.path.exists(sub_title_file):
        with open(sub_title_file, "w", encoding="utf-8") as f:
            f.write("ASSASSIN'S CREED: UNITY")

    # Write graphics text to file
    gfx_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_gfx.txt")
    with open(gfx_txt_file, "w", encoding="utf-8") as f:
        f.write(gfx)

    # Case A: Real Footage exists
    if os.path.exists(footage_path) and os.path.getsize(footage_path) > 5000:
        if gfx:
            vf = f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,drawtext=fontfile={FONT_THAI}:textfile={gfx_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=118:y=h-75:box=1:boxcolor=0x121719@0.85:boxborderw=8"
        else:
            vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"

        cmd = [
            "ffmpeg", "-y",
            "-i", footage_path,
            "-t", str(dur),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-an",
            out_path
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return out_path
        except Exception:
            pass # Fall through to procedural graphics if file is busy or unreadable

    # Case B: Typography / Quote or Chapter
    if "Typography" in shot["type"] or "Quote" in shot["type"]:
        title_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_quote.txt")
        with open(title_txt_file, "w", encoding="utf-8") as f:
            f.write(gfx if gfx else "LEMINO INVESTIGATIVE DOCUMENTARY")

        vf = (
            f"drawtext=fontfile={FONT_SERIF}:textfile={title_txt_file}:expansion=none:fontcolor=white:fontsize=44:x=(w-text_w)/2:y=(h-text_h)/2-20,"
            f"drawtext=fontfile={FONT_THAI}:textfile={sub_title_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=20:x=(w-text_w)/2:y=(h-text_h)/2+45"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0f1416:s=1920x1080:d={dur}:r=30",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-an",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return out_path

    # Case C: Chapter Transition / Card
    if "Transition" in shot["type"] or "Chapter" in shot["type"]:
        ch_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_ch.txt")
        with open(ch_txt_file, "w", encoding="utf-8") as f:
            f.write(gfx if gfx else "CHAPTER BREAK")

        date_sub_file = os.path.join(txt_dir, "date_subtitle.txt")
        if not os.path.exists(date_sub_file):
            with open(date_sub_file, "w", encoding="utf-8") as f:
                f.write("PARIS 1789 - 2019")

        vf = (
            f"drawtext=fontfile={FONT_SERIF}:textfile={ch_txt_file}:expansion=none:fontcolor=0xd5a764:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2,"
            f"drawtext=fontfile={FONT_THAI}:textfile={date_sub_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=(w-text_w)/2:y=(h-text_h)/2+65"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x121719:s=1920x1080:d={dur}:r=30",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-an",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return out_path

    # Case D: Default Cinematic Canvas (Establishing / Archival / Diagram / Data Viz)
    bg_color = "0x14181a"
    label_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_label.txt")
    with open(label_txt_file, "w", encoding="utf-8") as f:
        f.write(f"{shot['id']} // {shot['type'].upper()}")

    vf = (
        f"drawtext=fontfile={FONT_SERIF}:textfile={label_txt_file}:expansion=none:fontcolor=white:fontsize=36:x=118:y=240,"
        f"drawtext=fontfile={FONT_THAI}:textfile={gfx_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=118:y=h-75:box=1:boxcolor=0x121719@0.85:boxborderw=8"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c={bg_color}:s=1920x1080:d={dur}:r=30",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-an",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return out_path

def main():
    docx_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/4_Full_Production_Shot_List_Doc_15Min.docx"
    footage_dir = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/footage"
    temp_shots_dir = "/tmp/lemino_shots_15min"
    txt_dir = "/tmp/lemino_txt_15min"
    vo_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/Master_Voiceover_15Min.mp3"
    bgm_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/bgm/Master_BGM_15Min.mp3"
    sfx_impact = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/sfx/sub_bass_impact.mp3"
    final_output = "/home/keng/พื้นโต๊ะ/Assassin_Creed_Unity_LEMiNO_15Min_Master.mp4"

    shots = parse_all_shots(docx_file)
    print(f"Total Shots in Episode: {len(shots)}")

    # 1. Render / standardize all 172 shot clips
    shot_clips = []
    print("Preparing 172 video shot clips...")
    for idx, s in enumerate(shots):
        clip = render_shot_clip(s, footage_dir, temp_shots_dir, txt_dir)
        shot_clips.append(clip)
        if (idx + 1) % 25 == 0 or (idx + 1) == len(shots):
            print(f"  Processed {idx + 1}/{len(shots)} shots...")

    # 2. Concat all 172 shots into video track
    concat_txt = os.path.join(temp_shots_dir, "master_video_concat.txt")
    with open(concat_txt, "w") as f:
        for c in shot_clips:
            f.write(f"file '{c}'\n")

    temp_video = os.path.join(temp_shots_dir, "temp_video_15min.mp4")
    print("Stitching 172 shots into continuous 15-minute 1080p video...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", temp_video], check=True)

    # 3. Master Audio Mixing with Ducking & EQ Carving
    print("Executing Broadcast Audio Mastering & Auto-Ducking Pipeline...")
    filter_complex = (
        "[1:a]volume=1.5,aformat=channel_layouts=stereo,asplit=2[vo1][vo2];"
        "[2:a]volume=0.10,equalizer=f=1200:width_type=o:w=2:g=-6,aformat=channel_layouts=stereo[bgm_eq];"
        "[bgm_eq][vo2]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[ducked_bgm];"
        "[3:a]volume=0.5,aformat=channel_layouts=stereo[sfx_imp];"
        "[vo1][ducked_bgm][sfx_imp]amix=inputs=3:duration=first:weights=1.0 0.8 0.4[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", vo_file,
        "-i", bgm_file,
        "-i", sfx_impact,
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        final_output
    ]
    subprocess.run(cmd, check=True)
    print(f"\n=======================================================")
    print(f"15-MINUTE MASTER DOCUMENTARY PRODUCED SUCCESSFULLY!")
    print(f"Location: {final_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
