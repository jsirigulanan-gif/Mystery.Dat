#!/usr/bin/env python3
"""
LEMiNO Professional Broadcast Audio Mastering Engine
Performs Dynamic Sidechain Ducking, Vocal EQ Carving, and Multi-track SFX Balancing.
"""

import argparse
import os
import subprocess
import sys

def mix_broadcast_audio(video_in, vo_audio, bgm_audio, output_mp4, sfx_list=None, ducking_depth=0.10, vo_boost=1.5):
    """
    Mixes voiceover, background music with sidechain ducking, and SFX into target video.
    """
    if not os.path.exists(video_in):
        raise FileNotFoundError(f"Input video not found: {video_in}")
    if not os.path.exists(vo_audio):
        raise FileNotFoundError(f"Voiceover track not found: {vo_audio}")

    inputs = ["-i", video_in, "-i", vo_audio]
    input_count = 2

    # Build filter complex
    # 1. Voiceover processing
    filter_parts = [
        f"[1:a]volume={vo_boost},aformat=channel_layouts=stereo[vo]"
    ]

    mix_inputs = ["[vo]"]
    mix_weights = ["1.0"]

    # 2. BGM processing with EQ carving and Sidechain Ducking
    if bgm_audio and os.path.exists(bgm_audio):
        inputs.extend(["-i", bgm_audio])
        bgm_idx = input_count
        input_count += 1
        # EQ Carve 1200Hz -6dB + Volume base level + Sidechain compress against [vo]
        filter_parts.append(
            f"[{bgm_idx}:a]volume={ducking_depth},equalizer=f=1200:width_type=o:w=2:g=-6,aformat=channel_layouts=stereo[bgm_eq];"
            f"[bgm_eq][vo]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[ducked_bgm]"
        )
        mix_inputs.append("[ducked_bgm]")
        mix_weights.append("0.8")

    # 3. SFX processing
    if sfx_list:
        for item in sfx_list:
            sfx_file = item.get("file")
            delay_ms = item.get("delay_ms", 0)
            vol = item.get("volume", 0.4)
            if sfx_file and os.path.exists(sfx_file):
                inputs.extend(["-i", sfx_file])
                sfx_idx = input_count
                input_count += 1
                lbl = f"sfx_{sfx_idx}"
                if delay_ms > 0:
                    filter_parts.append(f"[{sfx_idx}:a]adelay={delay_ms}|{delay_ms},volume={vol},aformat=channel_layouts=stereo[{lbl}]")
                else:
                    filter_parts.append(f"[{sfx_idx}:a]volume={vol},aformat=channel_layouts=stereo[{lbl}]")
                mix_inputs.append(f"[{lbl}]")
                mix_weights.append("0.5")

    # Master amix combine
    total_mix = len(mix_inputs)
    inputs_str = "".join(mix_inputs)
    weights_str = " ".join(mix_weights)
    filter_parts.append(f"{inputs_str}amix=inputs={total_mix}:duration=first:weights={weights_str}[aout]")

    full_filter = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        output_mp4
    ]

    print("Executing Broadcast Audio Mastering Pipeline...")
    subprocess.run(cmd, check=True)
    print(f"Master audio output generated: {output_mp4}")

def main():
    parser = argparse.ArgumentParser(description="LEMiNO Broadcast Audio Mixer")
    parser.add_argument("--video", required=True, help="Input video MP4")
    parser.add_argument("--vo", required=True, help="Voiceover audio file")
    parser.add_argument("--bgm", help="Background music audio file")
    parser.add_argument("--output", required=True, help="Output mastered MP4")
    parser.add_argument("--ducking", type=float, default=0.10, help="Base music volume level (e.g. 0.10)")
    parser.add_argument("--vo-boost", type=float, default=1.5, help="Voiceover boost multiplier (e.g. 1.5)")
    args = parser.parse_args()

    mix_broadcast_audio(args.video, args.vo, args.bgm, args.output, ducking_depth=args.ducking, vo_boost=args.vo_boost)

if __name__ == "__main__":
    main()
