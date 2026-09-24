#!/usr/bin/env python3
"""
LEMiNO 15-Minute Full Documentary Master Producer (Version 2.0)
Guarantees 100% VISUAL COVERAGE across all 172 shots with ZERO black frames:
- Real downloaded footage where available
- Dynamic B-roll pool slicing (Paris dawn, Notre Dame, Revolution, Glitches)
- Broadcast-grade LEMiNO technical blueprint HUD animations
- 2.5D archival motion & high-contrast typography cards
- Master broadcast audio with dynamic sidechain ducking & notch EQ carving
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

def get_broll_clip(shot, idx, broll_pool):
    """Select the best matching high-res B-roll source and timestamp offset."""
    vis = shot["visual"].lower()
    ref = shot["reference"].lower()

    # 1. Face Glitch or Bug
    if any(w in vis or w in ref for w in ["glitch", "bug", "face", "broken", "missing"]):
        src = os.path.join(broll_pool, "face_glitch.mp4")
        if os.path.exists(src) and os.path.getsize(src) > 100000:
            offset = (idx * 2) % 10
            return src, offset

    # 2. Notre Dame Cathedral
    if any(w in vis or w in ref for w in ["notre-dame", "notre dame", "cathedral", "gothic", "spire", "stone"]):
        src = os.path.join(broll_pool, "notre_dame_tour.mp4")
        if os.path.exists(src) and os.path.getsize(src) > 100000:
            offset = 20 + (idx * 11) % 240
            return src, offset

    # 3. Paris Streets / Rooftops / Dawn / Parkour
    src = os.path.join(broll_pool, "paris_freeroam.mp4")
    if os.path.exists(src) and os.path.getsize(src) > 100000:
        offset = 10 + (idx * 13) % 200
        return src, offset

    # 4. Revolution / Crowds / E3 / Action
    src = os.path.join(broll_pool, "e3_trailer.mp4")
    if os.path.exists(src) and os.path.getsize(src) > 100000:
        offset = 15 + (idx * 9) % 180
        return src, offset

    return None, 0

def render_shot_clip(shot, idx, footage_dir, broll_pool, out_dir, txt_dir, force=False):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{shot['id'].lower()}_ready.mp4")

    if not force and os.path.exists(out_path) and os.path.getsize(out_path) > 500000:
        return out_path

    dur = shot["duration"]
    gfx = shot["graphics"].strip()
    stype = shot["type"]

    # Text helper
    gfx_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_gfx.txt")
    with open(gfx_txt_file, "w", encoding="utf-8") as f:
        f.write(gfx if gfx else f"{shot['id']} // 1789 PARIS ARCHIVE")

    # Priority 1: Check if specific downloaded footage exists
    footage_path = os.path.join(footage_dir, f"{shot['id'].lower()}.mp4")
    if os.path.exists(footage_path) and os.path.getsize(footage_path) > 10000:
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
            pass

    # Priority 2: Typography / Quote
    if "Typography" in stype or "Quote" in stype:
        title_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_quote.txt")
        clean_quote = gfx.replace('“', '"').replace('”', '"')
        if not clean_quote:
            clean_quote = "AMBITION AND COLLAPSE SHARE THE SAME SEED."
        with open(title_txt_file, "w", encoding="utf-8") as f:
            f.write(clean_quote)

        sub_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_qsub.txt")
        with open(sub_txt_file, "w", encoding="utf-8") as f:
            f.write("ASSASSIN'S CREED: UNITY // INVESTIGATION")

        vf = (
            f"drawbox=x=200:y=200:w=1520:h=680:color=0x8ac2bb@0.2:t=1,"
            f"drawbox=x=220:y=220:w=1480:h=640:color=0xd5a764@0.15:t=1,"
            f"drawtext=fontfile={FONT_SERIF}:textfile={title_txt_file}:expansion=none:fontcolor=0xeee6d3:fontsize=42:x=(w-text_w)/2:y=(h-text_h)/2-30:shadowcolor=0x000000@0.8:shadowx=2:shadowy=2,"
            f"drawtext=fontfile={FONT_THAI}:textfile={sub_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=(w-text_w)/2:y=(h-text_h)/2+60"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x111618:s=1920x1080:d={dur}:r=30",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-an",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return out_path

    # Priority 3: Chapter Transition
    if "Transition" in stype or "Chapter" in stype:
        ch_txt_file = os.path.join(txt_dir, f"{shot['id'].lower()}_ch.txt")
        with open(ch_txt_file, "w", encoding="utf-8") as f:
            f.write(gfx if gfx else f"ACT // {shot['id']}")

        date_file = os.path.join(txt_dir, "date_trans.txt")
        if not os.path.exists(date_file):
            with open(date_file, "w", encoding="utf-8") as f:
                f.write("PARIS 1789 — 2019 // INVESTIGATIVE DOSSIER")

        vf = (
            f"drawbox=x=0:y=530:w=1920:h=2:color=0xd5a764@0.6:t=2,"
            f"drawtext=fontfile={FONT_SERIF}:textfile={ch_txt_file}:expansion=none:fontcolor=0xd5a764:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2-50:shadowcolor=0x000000@0.9:shadowx=3:shadowy=3,"
            f"drawtext=fontfile={FONT_THAI}:textfile={date_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=(w-text_w)/2:y=(h-text_h)/2+40"
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

    # Priority 4: Diagram / Explainer / Data Viz / Timeline -> LEMiNO Technical Blueprint HUD
    if any(k in stype for k in ["Diagram", "Data Visualization", "Timeline", "Explainer"]):
        top_left_file = os.path.join(txt_dir, "blueprint_top_left.txt")
        if not os.path.exists(top_left_file):
            with open(top_left_file, "w", encoding="utf-8") as f:
                f.write("LEMINO FORENSIC TELEMETRY // ANVILNEXT ENGINE")

        timecode_file = os.path.join(txt_dir, f"{shot['id'].lower()}_timecode.txt")
        with open(timecode_file, "w", encoding="utf-8") as f:
            f.write(f"EDL TIMECODE {shot['start_tc']} - {shot['end_tc']}")

        diag_title_file = os.path.join(txt_dir, f"{shot['id'].lower()}_diag.txt")
        with open(diag_title_file, "w", encoding="utf-8") as f:
            f.write(f"SYSTEM ARCHITECTURE // {stype.upper()}")

        vf = (
            f"drawgrid=width=120:height=120:thickness=1:color=0x8ac2bb@0.14,"
            f"drawbox=x=80:y=60:w=1760:h=960:color=0x8ac2bb@0.35:t=1,"
            f"drawbox=x=80:y=60:w=1760:h=45:color=0x121719@0.9:t=fill,"
            f"drawtext=fontfile={FONT_SERIF}:textfile={top_left_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=18:x=100:y=75,"
            f"drawtext=fontfile={FONT_SERIF}:textfile={timecode_file}:expansion=none:fontcolor=white:fontsize=18:x=w-text_w-100:y=75,"
            f"drawtext=fontfile={FONT_SERIF}:textfile={diag_title_file}:expansion=none:fontcolor=0xd5a764:fontsize=36:x=118:y=180,"
            f"drawbox=x=118:y=240:w=1684:h=2:color=0x8ac2bb@0.4:t=2,"
            f"drawtext=fontfile={FONT_THAI}:textfile={gfx_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=24:x=118:y=h-85:box=1:boxcolor=0x121719@0.9:boxborderw=10"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=0x0a1014:s=1920x1080:d={dur}:r=30",
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-an",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return out_path

    # Priority 5: Cinematic / B-roll / Archival -> Slice from High-Res B-Roll Pool!
    broll_src, offset = get_broll_clip(shot, idx, broll_pool)
    if broll_src and os.path.exists(broll_src):
        if gfx:
            vf = (
                f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,"
                f"drawtext=fontfile={FONT_THAI}:textfile={gfx_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=22:x=118:y=h-75:box=1:boxcolor=0x121719@0.85:boxborderw=8"
            )
        else:
            vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30"

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(offset),
            "-i", broll_src,
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
            pass

    # Absolute fallback (rich graphic frame, never black)
    archive_header_file = os.path.join(txt_dir, "archive_header.txt")
    if not os.path.exists(archive_header_file):
        with open(archive_header_file, "w", encoding="utf-8") as f:
            f.write("LEMINO INVESTIGATION // ARCHIVE RECORD")

    vf = (
        f"drawgrid=width=100:height=100:thickness=1:color=0x8ac2bb@0.15,"
        f"drawtext=fontfile={FONT_SERIF}:textfile={archive_header_file}:expansion=none:fontcolor=0xd5a764:fontsize=32:x=118:y=180,"
        f"drawtext=fontfile={FONT_THAI}:textfile={gfx_txt_file}:expansion=none:fontcolor=0x8ac2bb:fontsize=24:x=118:y=h-80:box=1:boxcolor=0x121719@0.9:boxborderw=8"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=0x101518:s=1920x1080:d={dur}:r=30",
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
    broll_pool = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/broll_pool"
    temp_shots_dir = "/tmp/lemino_shots_15min_v2"
    txt_dir = "/tmp/lemino_txt_15min_v2"
    vo_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/Master_Voiceover_15Min.mp3"
    bgm_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/bgm/Master_BGM_15Min.mp3"
    sfx_impact = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/sfx/sub_bass_impact.mp3"
    final_output = "/home/keng/พื้นโต๊ะ/Assassin_Creed_Unity_LEMiNO_15Min_Master.mp4"

    shots = parse_all_shots(docx_file)
    print(f"Total Shots in Episode: {len(shots)}")

    # Clean old tiny clips
    os.makedirs(temp_shots_dir, exist_ok=True)
    for f in os.listdir(temp_shots_dir):
        fp = os.path.join(temp_shots_dir, f)
        if os.path.isfile(fp) and os.path.getsize(fp) < 500000:
            os.remove(fp)

    # 1. Render all 172 shot clips with guaranteed visuals
    shot_clips = []
    print("Producing 172 video shot clips (Guaranteed 100% Visual Coverage)...")
    for idx, s in enumerate(shots):
        clip = render_shot_clip(s, idx, footage_dir, broll_pool, temp_shots_dir, txt_dir, force=False)
        shot_clips.append(clip)
        if (idx + 1) % 25 == 0 or (idx + 1) == len(shots):
            print(f"  Processed {idx + 1}/{len(shots)} shots...")

    # 2. Concat all 172 shots into video track
    concat_txt = os.path.join(temp_shots_dir, "master_video_concat.txt")
    with open(concat_txt, "w") as f:
        for c in shot_clips:
            f.write(f"file '{c}'\n")

    temp_video = os.path.join(temp_shots_dir, "temp_video_15min.mp4")
    print("\nStitching 172 shots into continuous 15-minute 1080p video...")
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
    print(f"15-MINUTE MASTER DOCUMENTARY RE-MASTERED WITH FULL VISUALS!")
    print(f"Saved to: {final_output}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()
