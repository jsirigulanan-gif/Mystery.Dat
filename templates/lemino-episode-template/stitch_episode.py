#!/usr/bin/env python3
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
    parser = argparse.ArgumentParser(description="Stitch LEMiNO episode from acts")
    parser.add_argument("--base", default=".", help="Base project directory")
    parser.add_argument("--output", default="master_episode/Master_Episode.mp4", help="Output MP4 path")
    args = parser.parse_args()

    # Find acts in order
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
        print("No renders found!")
        sys.exit(1)

    concat_txt = "concat_list_temp.txt"
    with open(concat_txt, "w") as f:
        for p in file_list:
            f.write(f"file '{os.path.abspath(p)}'\n")

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", args.output]
    print(f"Concatenating into {args.output}...")
    subprocess.run(cmd, check=True)
    if os.path.exists(concat_txt):
        os.remove(concat_txt)
    print("Master episode stitched successfully!")

if __name__ == "__main__":
    main()
