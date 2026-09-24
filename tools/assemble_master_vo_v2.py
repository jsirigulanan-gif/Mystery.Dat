#!/usr/bin/env python3
"""
LEMiNO Master Voiceover Track Assembler V2
Aligns complete narrative sections without any speech truncation (Zero atrim).
Preserves natural Thai sentence flow, breathing room, and exact Act synchronization.
"""

import os
import json
import subprocess

def assemble_continuous_master_vo(sections_json, audio_dir, out_vo_path):
    os.makedirs(os.path.dirname(out_vo_path), exist_ok=True)
    with open(sections_json, "r", encoding="utf-8") as f:
        sections = json.load(f)

    segments = []
    temp_dir = "/home/keng/.tmp/master_vo_v2_work"
    os.makedirs(temp_dir, exist_ok=True)
    
    timeline_cursor = 0.0 # in seconds
    
    for i, s in enumerate(sections):
        sec_idx = i + 1
        sec_audio = os.path.join(audio_dir, f"sec_{sec_idx:02d}.mp3")
        target_start = float(s["start_sec"])
        
        # Get actual duration of this section audio
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", sec_audio],
            capture_output=True, text=True
        )
        actual_dur = float(res.stdout.strip())
        
        # If there is a gap between current timeline cursor and target start, insert clean silence
        silence_gap = target_start - timeline_cursor
        if silence_gap > 0.05:
            silence_file = os.path.join(temp_dir, f"gap_{sec_idx:02d}.mp3")
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-t", f"{silence_gap:.3f}",
                "-c:a", "libmp3lame", "-b:a", "256k", silence_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            segments.append(silence_file)
            timeline_cursor += silence_gap
            
        # Add the actual speech clip
        segments.append(sec_audio)
        timeline_cursor += actual_dur
        print(f"Sec {sec_idx:02d}: Target Start {target_start:6.2f}s | Cursor now at {timeline_cursor:6.2f}s ({s['title'][:30]})")
        
    # Pad up to 900.0s if needed
    if timeline_cursor < 900.0:
        final_gap = 900.0 - timeline_cursor
        silence_file = os.path.join(temp_dir, "gap_final.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", f"{final_gap:.3f}",
            "-c:a", "libmp3lame", "-b:a", "256k", silence_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segments.append(silence_file)
        timeline_cursor += final_gap
        
    # Concat all segments into master VO
    concat_list = os.path.join(temp_dir, "vo_concat_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")
            
    print(f"\nConcatenating master voiceover to {out_vo_path} (Total duration: {timeline_cursor:.2f}s)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
        "-c:a", "libmp3lame", "-b:a", "256k",
        "-t", "900.00",
        out_vo_path
    ]
    subprocess.run(cmd, check=True)
    print("Master Voiceover V2 successfully built!")

if __name__ == "__main__":
    sections_json = "/home/keng/.tmp/script_sections.json"
    audio_dir = "/home/keng/.tmp/test_sections_audio"
    out_vo = "/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/Master_Voiceover_15Min.mp3"
    assemble_continuous_master_vo(sections_json, audio_dir, out_vo)
