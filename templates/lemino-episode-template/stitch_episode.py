#!/usr/bin/env python3
"""
LEMiNO Universal Episode Assembler & Audio Masterer
Stitches video acts, aligns master voiceover, background music with sidechain ducking, and SFX.
"""

import argparse
import glob
import os
import subprocess
import sys

def get_latest_render(act_path):
    r_dir = os.path.join(act_path, "renders")
    if not os.path.exists(r_dir):
        return None
    mp4s = sorted(glob.glob(os.path.join(r_dir, "*.mp4")), key=os.path.getmtime)
    return mp4s[-1] if mp4s else None

def main():
    parser = argparse.ArgumentParser(description="Stitch and Master LEMiNO Episode")
    parser.add_argument("--base", default=".", help="Base project directory")
    parser.add_argument("--output", default="master_episode/Master_Episode.mp4", help="Output MP4 path")
    parser.add_argument("--vo", help="Master Voiceover audio file")
    parser.add_argument("--bgm", help="Master Background Music track")
    args = parser.parse_args()

    # 1. Find acts in numerical order
    acts = sorted([d for d in os.listdir(args.base) if d.startswith("lemino-") and os.path.isdir(os.path.join(args.base, d))])
    file_list = []
    print(f"Found {len(acts)} acts to stitch:")
    for a in acts:
        p = os.path.join(args.base, a)
        render = get_latest_render(p)
        if render:
            print(f"  [OK] {a} -> {os.path.basename(render)}")
            file_list.append(render)
        else:
            print(f"  [SKIP/MISSING] {a}")

    if not file_list:
        print("No rendered acts found to stitch!")
        sys.exit(1)

    temp_video = "temp_video_stitched.mp4"
    concat_txt = "concat_list_temp.txt"
    with open(concat_txt, "w") as f:
        for p in file_list:
            f.write(f"file '{os.path.abspath(p)}'\n")

    print("Concatenating video acts...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", temp_video], check=True)
    if os.path.exists(concat_txt):
        os.remove(concat_txt)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    # 2. Master Audio Pipeline (Ducking & EQ Carving)
    if args.vo and os.path.exists(args.vo):
        print("Mastering final audio with Voiceover and Sidechain Ducked BGM...")
        inputs = ["-i", temp_video, "-i", args.vo]
        filter_parts = ["[1:a]volume=1.5,aformat=channel_layouts=stereo[vo]"]
        mix_inputs = ["[vo]"]
        mix_weights = ["1.0"]

        if args.bgm and os.path.exists(args.bgm):
            inputs.extend(["-i", args.bgm])
            filter_parts.append(
                "[2:a]volume=0.10,equalizer=f=1200:width_type=o:w=2:g=-6,aformat=channel_layouts=stereo[bgm_eq];"
                "[bgm_eq][vo]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[ducked_bgm]"
            )
            mix_inputs.append("[ducked_bgm]")
            mix_weights.append("0.8")

        total_mix = len(mix_inputs)
        inputs_str = "".join(mix_inputs)
        weights_str = " ".join(mix_weights)
        filter_parts.append(f"{inputs_str}amix=inputs={total_mix}:duration=first:weights={weights_str}[aout]")

        full_filter = ";".join(filter_parts)
        master_cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", full_filter,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "256k",
            "-shortest",
            args.output
        ]
        subprocess.run(master_cmd, check=True)
        if os.path.exists(temp_video):
            os.remove(temp_video)
    else:
        # Simple copy if no external VO specified
        os.replace(temp_video, args.output)

    print(f"Master broadcast episode produced: {args.output}")

if __name__ == "__main__":
    main()
