#!/usr/bin/env python3
"""
LEMiNO AI Voiceover Generator (Edge-TTS Thai Neural)
Parses shot list cue sheet and generates high-grade Thai documentary narration for each shot.
"""

import argparse
import asyncio
import os
import re
import edge_tts
import docx

VOICE_DEFAULT = "th-TH-NiwatNeural" # Male deep documentary voice

def parse_voiceover_shots(docx_path):
    doc = docx.Document(docx_path)
    shots = []
    current_shot = None
    header_re = re.compile(r'---\s*(SHOT-\d+)\s*\[([\d:\.]+)\s*-\s*([\d:\.]+)\s*/\s*([\d\.]+)s\]\s*---')

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        m = header_re.match(text)
        if m:
            if current_shot and current_shot["voiceover"]:
                shots.append(current_shot)
            shot_id, start_tc, end_tc, duration_str = m.groups()
            current_shot = {"id": shot_id, "duration": float(duration_str), "voiceover": ""}
            continue
        if current_shot and text.startswith("Voiceover:"):
            vo_text = text.replace("Voiceover:", "").strip()
            # Clean surrounding quotes
            vo_text = re.sub(r'^["\']|["\']$', '', vo_text).strip()
            current_shot["voiceover"] = vo_text

    if current_shot and current_shot["voiceover"]:
        shots.append(current_shot)
    return shots

async def generate_shot_voice(shot, output_dir, voice=VOICE_DEFAULT):
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"{shot['id'].lower()}_vo.mp3")
    
    text = shot["voiceover"]
    if not text:
        return None
        
    print(f"[{shot['id']}] Generating VO: \"{text[:45]}...\"")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_file)
    print(f"[{shot['id']}] Saved to: {out_file}")
    return out_file

async def main_async(args):
    shots = parse_voiceover_shots(args.shot_list)
    print(f"Found {len(shots)} shots with Thai voiceover text.")
    
    limit = args.limit if args.limit > 0 else len(shots)
    for s in shots[:limit]:
        await generate_shot_voice(s, args.output_dir, args.voice)

def main():
    parser = argparse.ArgumentParser(description="LEMiNO Voiceover Generator")
    parser.add_argument("--shot-list", default="/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/4_Full_Production_Shot_List_Doc_15Min.docx")
    parser.add_argument("--output-dir", default="/home/keng/พื้นโต๊ะ/อิพี 1/production_packages/ac_unity/assets/audio/voiceover")
    parser.add_argument("--voice", default=VOICE_DEFAULT, help="TTS Voice (e.g. th-TH-NiwatNeural)")
    parser.add_argument("--limit", type=int, default=5, help="Number of shots to generate (0 for all)")
    args = parser.parse_args()

    asyncio.run(main_async(args))

if __name__ == "__main__":
    main()
