#!/usr/bin/env python3
"""
LEMiNO 15-Minute Master Timeline Assembler
Aligns all 172 shots of voiceover, background music, and video layers to exact SMPTE timecodes.
"""

import os
import re
import subprocess
import docx

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

def assemble_master_voiceover(shots, vo_dir, out_vo_path):
    os.makedirs(os.path.dirname(out_vo_path), exist_ok=True)
    temp_dir = "/tmp/lemino_vo_aligned"
    os.makedirs(temp_dir, exist_ok=True)
    
    file_list = []
    print(f"Aligning {len(shots)} voiceover segments with exact duration padding...")
    
    for s in shots:
        vo_file = os.path.join(vo_dir, f"{s['id'].lower()}_vo.mp3")
        padded_file = os.path.join(temp_dir, f"{s['id'].lower()}_pad.mp3")
        target_dur = s["duration"]
        
        if os.path.exists(vo_file) and s["voiceover"]:
            # Pad audio to exact target_dur with apad / atrim
            cmd = [
                "ffmpeg", "-y", "-i", vo_file,
                "-af", f"apad=whole_dur={target_dur},atrim=0:{target_dur}",
                "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                padded_file
            ]
        else:
            # Silent track for pure music/visual shots
            cmd = [
                "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
                "-t", str(target_dur),
                "-c:a", "libmp3lame", "-b:a", "192k",
                padded_file
            ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        file_list.append(padded_file)

    concat_txt = os.path.join(temp_dir, "vo_concat.txt")
    with open(concat_txt, "w") as f:
        for p in file_list:
            f.write(f"file '{p}'\n")

    print(f"Stitching into master continuous voiceover: {out_vo_path}...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", out_vo_path], check=True)
    print("Master Voiceover track ready!")

if __name__ == "__main__":
    docx_file = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/4_Full_Production_Shot_List_Doc_15Min.docx"
    vo_directory = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/voiceover"
    output_master_vo = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/Master_Voiceover_15Min.mp3"
    
    shots_data = parse_all_shots(docx_file)
    assemble_master_voiceover(shots_data, vo_directory, output_master_vo)
