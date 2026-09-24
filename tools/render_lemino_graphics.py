#!/usr/bin/env python3
"""
LEMiNO Broadcast Motion Graphics Renderer (Version 2.0)
Generates authentic broadcast-grade animated motion graphics clips (1080p @ 30fps)
following the strict LEMiNO visual design system:
- Deep Charcoal (#121719) canvas
- LEMiNO Turquoise / Cyan (#8ac2bb) primary accents
- Warm Desert Gold (#d5a764) secondary accents
- Alert Crimson (#e64553)
- 100% WCAG AA contrast compliance with translucent backplates & drop shadows
- Corner brackets, fine grids, scanlines, animated rules, telemetry HUDs
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_SERIF = "/home/keng/.local/share/lemino_fonts/serif.ttf"
FONT_THAI = "/home/keng/.local/share/lemino_fonts/thai.ttf"
FONT_SERIF_THAI = "/home/keng/.local/share/lemino_fonts/serif-thai.ttf"

# Canonical LEMiNO Color Palette
BG_COLOR = (18, 23, 25)           # #121719 Deep Charcoal
TEAL = (138, 194, 187)            # #8ac2bb Primary Accent
GOLD = (213, 167, 100)            # #d5a764 Warm Gold
WHITE = (255, 255, 255)
OFF_WHITE = (238, 230, 211)       # #eee6d3 Stone Off-White
CRIMSON = (230, 69, 83)           # #e64553 Alert Red
MUTED_GRAY = (110, 125, 130)
PANEL_BG = (14, 18, 20, 235)

def get_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    """Cleanly wrap text into lines fitting within max_width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]
        if w > max_width:
            current_line.pop()
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_grid_background(draw, width=1920, height=1080, cell_size=120, alpha=20):
    """Draw subtle technical blueprint grid."""
    grid_col = (138, 194, 187, alpha)
    for x in range(0, width, cell_size):
        draw.line([(x, 0), (x, height)], fill=grid_col, width=1)
    for y in range(0, height, cell_size):
        draw.line([(0, y), (width, y)], fill=grid_col, width=1)

def draw_corner_brackets(draw, x1, y1, x2, y2, arm=30, color=TEAL, width=2):
    """Draw technical HUD framing brackets at 4 corners."""
    # Top-Left
    draw.line([(x1, y1), (x1 + arm, y1)], fill=color, width=width)
    draw.line([(x1, y1), (x1, y1 + arm)], fill=color, width=width)
    # Top-Right
    draw.line([(x2, y1), (x2 - arm, y1)], fill=color, width=width)
    draw.line([(x2, y1), (x2, y1 + arm)], fill=color, width=width)
    # Bottom-Left
    draw.line([(x1, y2), (x1 + arm, y2)], fill=color, width=width)
    draw.line([(x1, y2), (x1, y2 - arm)], fill=color, width=width)
    # Bottom-Right
    draw.line([(x2, y2), (x2 - arm, y2)], fill=color, width=width)
    draw.line([(x2, y2), (x2, y2 - arm)], fill=color, width=width)

def draw_top_bar(draw, act_num="ACT // I", edl_tc="00:00:00:00", shot_id="SHOT-001"):
    """LEMiNO standard top header bar."""
    f_bar = get_font(FONT_SERIF, 20)
    draw.text((118, 55), "LEMINO INVESTIGATION // CASE FILE #2014-ACU", font=f_bar, fill=TEAL)
    right_text = f"{shot_id}  |  TC {edl_tc}"
    bbox = f_bar.getbbox(right_text)
    w = bbox[2] - bbox[0]
    draw.text((1920 - 118 - w, 55), right_text, font=f_bar, fill=GOLD)
    draw.line([(118, 88), (1920 - 118, 88)], fill=(138, 194, 187, 70), width=1)

def draw_footer_bar(draw, subtitle="PARIS 1789 — 2019 // ANVILNEXT 2.0 ARCHITECTURAL ANALYSIS"):
    """LEMiNO standard footer bar."""
    f_foot = get_font(FONT_SERIF, 18)
    draw.line([(118, 1000), (1920 - 118, 1000)], fill=(138, 194, 187, 70), width=1)
    draw.text((118, 1015), subtitle, font=f_foot, fill=OFF_WHITE)
    draw.text((1920 - 118 - 180, 1015), "BROADCAST MASTER", font=f_foot, fill=TEAL)

# ==============================================================================
# 1. GRAND TITLE CARD
# ==============================================================================
def render_grand_title_frame(progress):
    """Render Grand Title sequence frame (0.0 <= progress <= 1.0)."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=100, alpha=25)
    
    # Top & Footer
    draw_top_bar(draw, act_num="COLD OPEN", edl_tc="00:00:15:00", shot_id="GRAND TITLE CARD")
    draw_footer_bar(draw, "LEMINO DOCUMENTARY INVESTIGATION // SPECIAL PRESENTATION")
    
    # Outer HUD frame
    draw_corner_brackets(draw, 118, 120, 1920 - 118, 970, arm=40, color=(138, 194, 187, 180), width=2)
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    # Dark translucent backplate for 100% WCAG AA contrast compliance
    draw.rectangle([(cx - 750, cy - 240), (cx + 750, cy + 220)], fill=(14, 18, 20, 220), outline=(138, 194, 187, 60), width=1)
    
    # Architectural photogrammetry geometry behind title (LEMiNO aesthetic)
    geom_alpha = min(220, int(180 * min(progress * 2.0, 1.0)))
    geom_col = (138, 194, 187, geom_alpha)
    gold_geom = (213, 167, 100, geom_alpha)
    
    # Triangle (Notre-Dame Spire / Freemason architecture)
    tri_top = (cx, cy - 210)
    tri_left = (cx - 240, cy + 160)
    tri_right = (cx + 240, cy + 160)
    draw.polygon([tri_top, tri_left, tri_right], outline=geom_col, width=2)
    
    # Circle (Rose Window)
    r = 85
    draw.ellipse([(cx - r, cy - 50 - r), (cx + r, cy - 50 + r)], outline=gold_geom, width=2)
    
    # Square (Cathedral Base)
    draw.rectangle([(cx - 140, cy - 10), (cx + 140, cy + 160)], outline=geom_col, width=1)
    
    # Animated Title Elements
    f_eyebrow = get_font(FONT_SERIF, 24)
    f_title = get_font(FONT_SERIF, 74)
    f_sub = get_font(FONT_SERIF, 30)
    f_badge = get_font(FONT_SERIF, 19)
    
    # 1. Eyebrow
    eyebrow = "D O C U M E N T A R Y   I N V E S T I G A T I O N"
    bb = f_eyebrow.getbbox(eyebrow)
    ew = bb[2] - bb[0]
    draw.text((cx - ew // 2, cy - 130), eyebrow, font=f_eyebrow, fill=TEAL)
    
    # 2. Main Title
    title = "ASSASSIN'S CREED: UNITY"
    bb = f_title.getbbox(title)
    tw = bb[2] - bb[0]
    draw.text((cx - tw // 2 + 2, cy - 70 + 2), title, font=f_title, fill=(0, 0, 0, 240))
    draw.text((cx - tw // 2, cy - 70), title, font=f_title, fill=WHITE)
    
    # 3. Expanding Gold Divider Rule
    rule_max_w = 420
    rule_w = int(rule_max_w * min(progress * 1.5, 1.0))
    draw.line([(cx - rule_w // 2, cy + 30), (cx + rule_w // 2, cy + 30)], fill=GOLD, width=3)
    
    # 4. Subtitle
    sub = "The Missing Faces, The 1:1 Paris Engine & The Fall of the Annual Franchise"
    bb = f_sub.getbbox(sub)
    sw = bb[2] - bb[0]
    draw.text((cx - sw // 2, cy + 55), sub, font=f_sub, fill=OFF_WHITE)
    
    # 5. Micro Badge
    badge = "ANVILNEXT 2.0 FORENSIC ANALYSIS  •  PARIS 1789 — 2019"
    bb = f_badge.getbbox(badge)
    bw = bb[2] - bb[0]
    bx = cx - bw // 2
    by = cy + 120
    draw.rectangle([(bx - 20, by - 6), (bx + bw + 20, by + 28)], fill=(14, 18, 20, 240), outline=TEAL, width=1)
    draw.text((bx, by), badge, font=f_badge, fill=TEAL)
    
    return im.convert("RGB")

# ==============================================================================
# 2. CHAPTER TITLE CARDS (Acts I - VI)
# ==============================================================================
def render_chapter_frame(act_num, act_title, act_sub, progress=1.0):
    """Render minimalist chapter title card."""
    im = Image.new("RGBA", (1920, 1080), (14, 18, 20))
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=140, alpha=20)
    
    draw_top_bar(draw, act_num=act_num, edl_tc="00:00:00:00", shot_id=act_num)
    draw_footer_bar(draw, "LEMINO INVESTIGATION // NARRATIVE ACT PROGRESSION")
    
    draw_corner_brackets(draw, 180, 180, 1920 - 180, 900, arm=35, color=(213, 167, 100, 160), width=1)
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    f_act = get_font(FONT_SERIF, 26)
    f_main = get_font(FONT_SERIF, 64)
    f_sub = get_font(FONT_SERIF, 28)
    
    # Act label
    bb = f_act.getbbox(act_num)
    aw = bb[2] - bb[0]
    draw.text((cx - aw // 2, cy - 90), act_num, font=f_act, fill=TEAL)
    
    # Main Act Title
    bb = f_main.getbbox(act_title)
    mw = bb[2] - bb[0]
    draw.text((cx - mw // 2, cy - 40), act_title, font=f_main, fill=GOLD)
    
    # Hairline divider
    rule_w = int(340 * min(progress * 1.6, 1.0))
    draw.line([(cx - rule_w // 2, cy + 50), (cx + rule_w // 2, cy + 50)], fill=(138, 194, 187, 180), width=2)
    
    # Act Subtitle
    bb = f_sub.getbbox(act_sub)
    sw = bb[2] - bb[0]
    draw.text((cx - sw // 2, cy + 75), act_sub, font=f_sub, fill=OFF_WHITE)
    
    return im.convert("RGB")

# ==============================================================================
# 3. DATA VISUALIZATION: DIGITAL FOUNDRY 15.2 FPS DROP
# ==============================================================================
def render_digital_foundry_frame(progress=1.0):
    """Render Digital Foundry 15.2 FPS drop telemetry benchmark graph."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=25)
    
    draw_top_bar(draw, act_num="ACT II", edl_tc="03:45:00:00", shot_id="SHOT-043")
    draw_footer_bar(draw, "DIGITAL FOUNDRY BENCHMARK  |  NOTRE-DAME REVOLUTIONARY CROWD RIOT (5,000 NPCs)")
    
    gx1, gy1, gx2, gy2 = 180, 160, 1920 - 180, 920
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=(138, 194, 187, 90), width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=CRIMSON, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_data = get_font(FONT_SERIF, 26)
    
    draw.text((gx1 + 50, gy1 + 40), "FRAME-RATE PERFORMANCE ANALYSIS // 1080p CAPTURE", font=f_head, fill=OFF_WHITE)
    draw.text((gx1 + 50, gy1 + 85), "BENCHMARK SUITE: DIGITAL FOUNDRY FORENSIC TELEMETRY", font=f_sub, fill=TEAL)
    
    cur_fps = 30.0 - (14.8 * min(progress * 1.4, 1.0))
    fps_color = CRIMSON if cur_fps < 22 else GOLD
    draw.text((gx1 + 50, gy1 + 140), f"CURRENT FRAME RATE: {cur_fps:.1f} FPS", font=f_data, fill=fps_color)
    
    cpu_load = min(100, int(60 + 40 * progress))
    draw.text((gx1 + 50, gy1 + 180), f"AMD JAGUAR 8-CORE CPU LOAD: [{'|' * (cpu_load // 4)}] {cpu_load}%", font=f_data, fill=CRIMSON)
    
    draw_calls = int(12000 + 40480 * min(progress * 1.2, 1.0))
    draw.text((gx1 + 50, gy1 + 220), f"DIRECTX 11 DRAW CALLS: {draw_calls:,} / FRAME (LIMIT: 10,000)", font=f_data, fill=GOLD)
    
    chart_x1 = gx1 + 50
    chart_y1 = gy1 + 300
    chart_x2 = gx2 - 50
    chart_y2 = gy2 - 60
    
    target_30_y = chart_y1 + 40
    draw.line([(chart_x1, target_30_y), (chart_x2, target_30_y)], fill=(138, 194, 187, 80), width=1)
    draw.text((chart_x2 - 130, target_30_y - 25), "30.0 FPS TARGET", font=f_sub, fill=TEAL)
    
    floor_15_y = chart_y1 + 220
    draw.line([(chart_x1, floor_15_y), (chart_x2, floor_15_y)], fill=(230, 69, 83, 100), width=1)
    draw.text((chart_x2 - 150, floor_15_y - 25), "15.2 FPS CRITICAL", font=f_sub, fill=CRIMSON)
    
    pts = []
    num_samples = 80
    chart_w = chart_x2 - chart_x1
    for i in range(num_samples):
        frac = i / (num_samples - 1)
        x = chart_x1 + int(frac * chart_w)
        if frac < 0.35:
            y = target_30_y + int(math.sin(i * 0.8) * 3)
        elif frac < 0.65:
            drop_f = (frac - 0.35) / 0.30
            y = target_30_y + int(drop_f * (floor_15_y - target_30_y)) + int(math.sin(i * 1.2) * 5)
        else:
            y = floor_15_y + int(math.sin(i * 1.5) * 8)
        
        if frac <= progress:
            pts.append((x, y))
            
    if len(pts) > 1:
        draw.line(pts, fill=CRIMSON, width=4)
        for p in pts:
            draw.ellipse([(p[0]-3, p[1]-3), (p[0]+3, p[1]+3)], fill=CRIMSON)
            
    if progress > 0.6:
        cx_box = chart_x1 + int(0.75 * chart_w)
        cy_box = floor_15_y + 40
        draw.rectangle([(cx_box - 160, cy_box - 25), (cx_box + 160, cy_box + 25)], fill=(230, 69, 83, 40), outline=CRIMSON, width=2)
        draw.text((cx_box - 145, cy_box - 14), "CRITICAL COLLAPSE: 15.2 FPS", font=f_sub, fill=WHITE)
        
    return im.convert("RGB")

# ==============================================================================
# 4. DATA VISUALIZATION: AMD JAGUAR 8-CORE CPU BOTTLENECK
# ==============================================================================
def render_cpu_architecture_frame(progress=1.0):
    """Render AMD Jaguar 8-Core CPU architecture saturation diagram."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=25)
    
    draw_top_bar(draw, act_num="ACT III", edl_tc="05:15:00:00", shot_id="SHOT-064")
    draw_footer_bar(draw, "HARDWARE ARCHITECTURE // AMD CUSTOM 8-CORE JAGUAR 1.6 GHz (PS4 / XBOX ONE)")
    
    gx1, gy1, gx2, gy2 = 160, 140, 1920 - 160, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=(138, 194, 187, 90), width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 30)
    f_sub = get_font(FONT_SERIF, 21)
    f_core = get_font(FONT_SERIF, 19)
    
    draw.text((gx1 + 50, gy1 + 30), "MICROPROCESSOR THREAD OVERHEAD // 8-CORE DIE LAYOUT", font=f_head, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 70), "DIAGNOSIS: CROWD AI & INVERSE KINEMATICS SATURATING HARDWARE CAPACITY", font=f_sub, fill=TEAL)
    
    start_x = gx1 + 50
    start_y = gy1 + 120
    box_w = 345
    box_h = 160
    spacing_x = 35
    spacing_y = 30
    
    core_tasks = [
        "CORE 0: MAIN GAME LOGIC",
        "CORE 1: CROWD AI (5,000 NPCs)",
        "CORE 2: INVERSE KINEMATICS",
        "CORE 3: SOUND & AMBIENCE",
        "CORE 4: DX11 DRIVER DISPATCH",
        "CORE 5: CLOTH & PARQUET PHYSICS",
        "CORE 6: VRAM STREAM QUEUE",
        "CORE 7: DRAW CALL PIPELINE"
    ]
    
    for idx in range(8):
        row = idx // 4
        col = idx % 4
        bx = start_x + col * (box_w + spacing_x)
        by = start_y + row * (box_h + spacing_y)
        
        load = min(100, int(85 + 15 * math.sin(idx * 1.5 + progress * 4)))
        load_col = CRIMSON if load > 92 else GOLD
        
        draw.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=(20, 26, 30, 240), outline=load_col, width=2)
        draw.text((bx + 16, by + 16), core_tasks[idx], font=f_core, fill=WHITE)
        draw.text((bx + 16, by + 50), f"FREQUENCY: 1.60 GHz", font=f_sub, fill=MUTED_GRAY)
        draw.text((bx + 16, by + 80), f"CORE USAGE: {load}%", font=f_core, fill=load_col)
        
        bar_w = int((box_w - 32) * (load / 100.0))
        draw.rectangle([(bx + 16, by + 120), (bx + 16 + bar_w, by + 138)], fill=load_col)
        draw.rectangle([(bx + 16, by + 120), (bx + box_w - 16, by + 138)], outline=MUTED_GRAY, width=1)
        
    # Wrapped bottom note box
    note_box_y = gy1 + 520
    draw.rectangle([(gx1 + 50, note_box_y), (gx2 - 50, gy2 - 35)], fill=(230, 69, 83, 30), outline=CRIMSON, width=2)
    draw.text((gx1 + 75, note_box_y + 20), "CRITICAL ARCHITECTURAL BOTTLENECK DETECTED:", font=f_head, fill=CRIMSON)
    
    desc = "Single-threaded DirectX 11 command driver overhead blocks core parallelism. Jaguar's 1.6 GHz low single-core IPC cannot process 52,000 draw calls per frame, starving the GPU and collapsing frame rates."
    wrapped_desc = wrap_text(draw, desc, f_sub, gx2 - gx1 - 150)
    for i, l in enumerate(wrapped_desc):
        draw.text((gx1 + 75, note_box_y + 65 + i * 30), l, font=f_sub, fill=WHITE)
        
    return im.convert("RGB")

# ==============================================================================
# 5. ARCHIVAL EVIDENCE: YANNIS MALLAT APOLOGY LETTER
# ==============================================================================
def render_archival_apology_frame(progress=1.0):
    """Render official Yannis Mallat CEO Apology Letter with red highlight box."""
    im = Image.new("RGBA", (1920, 1080), (14, 12, 11))
    draw = ImageDraw.Draw(im, "RGBA")
    
    draw_top_bar(draw, act_num="ACT IV", edl_tc="07:45:00:00", shot_id="SHOT-087")
    draw_footer_bar(draw, "UBISOFT MONTREAL ARCHIVES  |  COMMUNITY STATEMENT // NOVEMBER 26, 2014")
    
    # Document paper backplate
    doc_x1, doc_y1, doc_x2, doc_y2 = 280, 130, 1640, 940
    # Drop shadow
    draw.rectangle([(doc_x1 + 10, doc_y1 + 10), (doc_x2 + 10, doc_y2 + 10)], fill=(0, 0, 0, 180))
    draw.rectangle([(doc_x1, doc_y1), (doc_x2, doc_y2)], fill=(245, 240, 230), outline=(213, 167, 100, 180), width=2)
    
    f_ubisoft = get_font(FONT_SERIF, 26)
    f_doc_title = get_font(FONT_SERIF, 32)
    f_body = get_font(FONT_SERIF, 21)
    f_sign = get_font(FONT_SERIF, 22)
    
    draw.text((doc_x1 + 60, doc_y1 + 40), "UBISOFT MONTREAL  //  OFFICIAL STATEMENT", font=f_ubisoft, fill=(40, 40, 40))
    draw.line([(doc_x1 + 60, doc_y1 + 75), (doc_x2 - 60, doc_y1 + 75)], fill=(180, 180, 180), width=1)
    
    draw.text((doc_x1 + 60, doc_y1 + 100), "AN UPDATE ON ASSASSIN'S CREED UNITY FROM YANNIS MALLAT", font=f_doc_title, fill=(20, 20, 20))
    
    paragraphs = [
        "To our community:",
        "The launch of Assassin's Creed Unity was a highly anticipated moment for all of us at Ubisoft.",
        "Unfortunately, at launch, the overall quality of the game was diminished by bugs and unexpected technical issues. I want to sincerely apologize on behalf of Ubisoft and the entire Assassin's Creed team.",
        "These issues took away from your enjoyment of the game, and kept many of you from experiencing the game at its fullest potential.",
        "To thank you for your ongoing support, we would like to offer the following concessions:",
        "  • The upcoming Dead Kings DLC will be made free for all players.",
        "  • For Season Pass holders, we are offering one free game from a selection of Ubisoft titles."
    ]
    
    cur_y = doc_y1 + 165
    max_w = doc_x2 - doc_x1 - 120
    hl_rect = None
    
    for p_idx, p in enumerate(paragraphs):
        lines = wrap_text(draw, p, f_body, max_w)
        for line in lines:
            if "diminished by bugs and unexpected technical issues" in line:
                # Save coordinates for the red highlight box
                hl_rect = (doc_x1 + 55, cur_y - 4, doc_x1 + 55 + max_w, cur_y + 32)
            draw.text((doc_x1 + 60, cur_y), line, font=f_body, fill=(45, 45, 45))
            cur_y += 34
        cur_y += 14
        
    # Render animated red forensic highlight box
    if hl_rect:
        hx1, hy1, hx2, hy2 = hl_rect
        cur_hx2 = hx1 + int((hx2 - hx1) * min(progress * 1.5, 1.0))
        draw.rectangle([(hx1, hy1), (cur_hx2, hy2)], fill=(230, 69, 83, 40), outline=CRIMSON, width=2)
        
    # Signature
    draw.text((doc_x1 + 60, doc_y2 - 100), "Yannis Mallat\nCEO, Ubisoft Montreal & Toronto", font=f_sign, fill=(30, 30, 30), spacing=5)
    
    # Evidence Stamp
    stamp_x = doc_x2 - 250
    stamp_y = doc_y2 - 110
    draw.rectangle([(stamp_x, stamp_y), (stamp_x + 190, stamp_y + 55)], outline=CRIMSON, width=3)
    draw.text((stamp_x + 20, stamp_y + 14), "EXHIBIT #07.1", font=get_font(FONT_SERIF, 22), fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 6. ARCHIVAL EVIDENCE: FREE AAA GAME WAIVER
# ==============================================================================
def render_archival_free_game_frame(progress=1.0):
    """Render Free AAA Game Redemption page with highlighted legal waiver."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT IV", edl_tc="09:00:00:00", shot_id="SHOT-092")
    draw_footer_bar(draw, "LEGAL FORENSICS // SEASON PASS COMPENSATION CLAUSE & CLASS-ACTION WAIVER")
    
    gx1, gy1, gx2, gy2 = 200, 140, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=GOLD, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 30)
    f_sub = get_font(FONT_SERIF, 22)
    f_game = get_font(FONT_SERIF, 20)
    
    draw.text((gx1 + 50, gy1 + 35), "UBISOFT FREE GAME REDEMPTION PORTAL // SEASON PASS HOLDERS", font=f_head, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "ELIGIBLE AAA SELECTIONS: FAR CRY 4, WATCH DOGS, THE CREW, RAYMAN LEGENDS", font=f_sub, fill=TEAL)
    
    # 4 Game Cards
    games = ["FAR CRY 4", "WATCH DOGS", "THE CREW", "RAYMAN LEGENDS"]
    card_w = 340
    card_h = 160
    card_start_x = gx1 + 50
    card_y = gy1 + 130
    
    for i, g in enumerate(games):
        cx_card = card_start_x + i * (card_w + 25)
        draw.rectangle([(cx_card, card_y), (cx_card + card_w, card_y + card_h)], fill=(20, 26, 30, 220), outline=TEAL, width=1)
        draw.text((cx_card + 20, card_y + 30), g, font=f_head, fill=WHITE)
        draw.text((cx_card + 20, card_y + 80), "FREE REDEMPTION", font=f_sub, fill=GOLD)
        draw.rectangle([(cx_card + 20, card_y + 115), (cx_card + 160, card_y + 145)], fill=(138, 194, 187, 40), outline=TEAL, width=1)
        draw.text((cx_card + 35, card_y + 120), "CLAIM TITLE", font=f_game, fill=TEAL)
        
    # Legal Clause Section with glowing red highlight
    legal_y = gy1 + 330
    draw.rectangle([(gx1 + 50, legal_y), (gx2 - 50, gy2 - 40)], fill=(25, 20, 22, 240), outline=CRIMSON, width=2)
    draw.text((gx1 + 75, legal_y + 25), "TERMS AND CONDITIONS // MANDATORY LEGAL RELEASE:", font=f_head, fill=CRIMSON)
    
    clause_text = (
        "“BY REDEEMING THIS FREE GAME OFFER, YOU HEREBY FULLY UNCONDITIONALLY RELEASE AND FOREVER DISCHARGE "
        "UBISOFT ENTERTAINMENT S.A. AND ITS AFFILIATES FROM ANY AND ALL CLAIMS, LIABILITIES, CAUSES OF ACTION, "
        "OR DEMANDS ARISING FROM OR RELATING TO ASSASSIN'S CREED UNITY, INCLUDING BUT NOT LIMITED TO ANY WAIVER "
        "OF PARTICIPATION IN ANY CLASS-ACTION LAWSUIT.”"
    )
    
    lines = wrap_text(draw, clause_text, f_sub, gx2 - gx1 - 150)
    for i, line in enumerate(lines):
        # Red highlight over waiver text
        ly = legal_y + 80 + i * 36
        hl_w = int((gx2 - gx1 - 150) * min(progress * 1.4, 1.0))
        draw.rectangle([(gx1 + 70, ly - 4), (gx1 + 70 + hl_w, ly + 28)], fill=(230, 69, 83, 40))
        draw.text((gx1 + 75, ly), line, font=f_sub, fill=WHITE)
        
    return im.convert("RGB")

# ==============================================================================
# 6.5 ARCHIVAL EVIDENCE: COMMUNITY REACTION FORUM DOSSIER (SHOT-103)
# ==============================================================================
def render_community_sentiment_frame(progress=1.0):
    """Render community forum reaction cards for free game compensation."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=25)
    
    draw_top_bar(draw, act_num="ACT IV", edl_tc="08:54:00:00", shot_id="SHOT-103")
    draw_footer_bar(draw, "COMMUNITY REACTION FORENSICS // GAMER SENTIMENT SHIFT & FORUM ARCHIVES")
    
    gx1, gy1, gx2, gy2 = 200, 140, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=TEAL, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_forum = get_font(FONT_SERIF, 20)
    
    draw.text((gx1 + 50, gy1 + 35), "PUBLIC RELATIONS RECEPTIVITY // GLOBAL FORUM REACTION", font=f_head, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "ANALYSIS OF REDDIT, NEOGAF & TWITTER THREADS POST-APOLOGY", font=f_sub, fill=TEAL)
    
    # 3 Forum Post Cards
    posts = [
        ("REDDIT // r/games (Nov 27, 2014)", 
         "“Ubisoft actually apologized and gave away Far Cry 4 for free... That is a $60 game. Honestly did not expect them to do this.”",
         "+4,821 UPVOTES  •  94% POSITIVE"),
        ("NEOGAF FORUMS // THREAD #8192", 
         "“The PR disaster was so severe they had to sacrifice AAA revenue to stop a class-action lawsuit. But hey, free Watch Dogs.”",
         "VERIFIED MEMBER  •  NOVEMBER 2014"),
        ("IGN COMMUNITY FEEDBACK", 
         "“Unity still drops frames in Notre-Dame, but giving free games to Season Pass holders quelled the immediate boycott.”",
         "TOP RATED COMMENT  •  382 LIKES")
    ]
    
    card_y = gy1 + 140
    card_h = 190
    card_w = gx2 - gx1 - 100
    
    for i, (source_tag, body_text, meta_tag) in enumerate(posts):
        cy = card_y + i * (card_h + 35)
        # Staggered slide in
        prog_i = max(0.0, min(1.0, (progress - i * 0.15) * 1.5))
        ox = int((1.0 - prog_i) * 60)
        
        draw.rectangle([(gx1 + 50 + ox, cy), (gx1 + 50 + ox + card_w, cy + card_h)], fill=(16, 22, 26, 230), outline=(138, 194, 187, 120), width=1)
        draw.rectangle([(gx1 + 50 + ox, cy), (gx1 + 50 + ox + 6, cy + card_h)], fill=GOLD)
        
        draw.text((gx1 + 80 + ox, cy + 20), source_tag, font=f_forum, fill=TEAL)
        draw.text((gx1 + 80 + ox, cy + 60), body_text, font=f_sub, fill=WHITE)
        draw.text((gx1 + 80 + ox, cy + 145), meta_tag, font=f_forum, fill=MUTED_GRAY)
        
    return im.convert("RGB")


# ==============================================================================
# 7. DATA VISUALIZATION: UK SALES SLUMP (-40%)
# ==============================================================================
def render_sales_comparison_frame(progress=1.0):
    """Render UK Sales crash bar chart (-40% drop for Syndicate)."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=25)
    
    draw_top_bar(draw, act_num="ACT V", edl_tc="10:15:00:00", shot_id="SHOT-120")
    draw_footer_bar(draw, "COMMERCIAL MARKET ANALYSIS // UK WEEK 1 LAUNCH SALES (GfK CHART-TRACK)")
    
    gx1, gy1, gx2, gy2 = 200, 160, 1920 - 200, 920
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=(138, 194, 187, 90), width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_bar_lbl = get_font(FONT_SERIF, 26)
    f_val = get_font(FONT_SERIF, 44)
    
    draw.text((gx1 + 60, gy1 + 45), "FRANCHISE BRAND CONTAMINATION // LAUNCH WEEK SALES IMPACT", font=f_head, fill=OFF_WHITE)
    draw.text((gx1 + 60, gy1 + 90), "COMPARISON: AC UNITY (2014) VS. AC SYNDICATE (2015)", font=f_sub, fill=TEAL)
    
    base_y = gy2 - 120
    max_h = 420
    
    # Bar 1: AC UNITY
    b1_x = gx1 + 220
    b1_w = 260
    b1_h = int(max_h * min(progress * 1.2, 1.0))
    draw.rectangle([(b1_x, base_y - b1_h), (b1_x + b1_w, base_y)], fill=(138, 194, 187, 200), outline=TEAL, width=2)
    draw.text((b1_x + 35, base_y + 20), "AC UNITY (2014)", font=f_bar_lbl, fill=WHITE)
    draw.text((b1_x + 55, base_y - b1_h - 60), "100%", font=f_val, fill=TEAL)
    draw.text((b1_x + 25, base_y - b1_h - 100), "BASELINE SALES", font=f_sub, fill=MUTED_GRAY)
    
    # Bar 2: AC SYNDICATE (-40%)
    b2_x = gx1 + 680
    b2_w = 260
    b2_h = int((max_h * 0.60) * min(progress * 1.2, 1.0))
    draw.rectangle([(b2_x, base_y - b2_h), (b2_x + b2_w, base_y)], fill=(230, 69, 83, 200), outline=CRIMSON, width=2)
    draw.text((b2_x + 15, base_y + 20), "AC SYNDICATE (2015)", font=f_bar_lbl, fill=WHITE)
    draw.text((b2_x + 55, base_y - b2_h - 60), "-40.2%", font=f_val, fill=CRIMSON)
    draw.text((b2_x + 10, base_y - b2_h - 100), "CATASTROPHIC SLUMP", font=f_sub, fill=CRIMSON)
    
    draw.rectangle([(gx1 + 1040, gy1 + 180), (gx2 - 60, gy2 - 120)], fill=(14, 18, 20, 200), outline=GOLD, width=1)
    draw.text((gx1 + 1070, gy1 + 210), "EXECUTIVE FINDINGS:", font=f_head, fill=GOLD)
    summary_text = (
        "Despite Assassin's Creed Syndicate releasing virtually bug-free with positive critic reviews, players refused to buy it at launch. The brand damage from Unity's 2014 launch destroyed consumer trust, forcing Ubisoft to cancel the 2016 annual release cycle."
    )
    lines = wrap_text(draw, summary_text, f_sub, gx2 - (gx1 + 1040) - 60)
    for i, l in enumerate(lines):
        draw.text((gx1 + 1070, gy1 + 270 + i * 32), l, font=f_sub, fill=OFF_WHITE)
        
    return im.convert("RGB")

# ==============================================================================
# 8. HIGH-CONTRAST TYPOGRAPHY QUOTE CARDS
# ==============================================================================
def render_typography_frame(quote_text, attribution="ASSASSIN'S CREED: UNITY // HISTORICAL DOSSIER", progress=1.0):
    """Render stark high-contrast typography quote card."""
    im = Image.new("RGBA", (1920, 1080), (12, 15, 17))
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=160, alpha=15)
    
    draw_top_bar(draw, act_num="HISTORICAL ARCHIVE", edl_tc="00:00:00:00", shot_id="STATEMENT")
    draw_footer_bar(draw, attribution)
    
    draw_corner_brackets(draw, 220, 220, 1920 - 220, 860, arm=35, color=(138, 194, 187, 120), width=1)
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    f_quote = get_font(FONT_SERIF, 44)
    lines = wrap_text(draw, quote_text, f_quote, 1300)
        
    line_h = 65
    total_h = len(lines) * line_h
    start_y = cy - total_h // 2 - 20
    
    for i, line in enumerate(lines):
        bb = f_quote.getbbox(line)
        lw = bb[2] - bb[0]
        draw.text((cx - lw // 2 + 2, start_y + i * line_h + 2), line, font=f_quote, fill=(0, 0, 0, 220))
        draw.text((cx - lw // 2, start_y + i * line_h), line, font=f_quote, fill=OFF_WHITE)
        
    rule_w = int(240 * min(progress * 1.5, 1.0))
    rule_y = start_y + total_h + 30
    draw.line([(cx - rule_w // 2, rule_y), (cx + rule_w // 2, rule_y)], fill=GOLD, width=2)
    
    return im.convert("RGB")

# ==============================================================================
# 9. GRAPHIC B-ROLL: ANVILNEXT 2.0 3D PARIS BLUEPRINT
# ==============================================================================
def render_graphic_broll_blueprint(progress=1.0, shot_id="SHOT-013", act_lbl="ACT I", edl_tc="01:01:00:00"):
    """Render 3D Paris Wireframe & AnvilNext 2.0 Architectural Blueprint."""
    im = Image.new("RGBA", (1920, 1080), (10, 14, 17))
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=60, alpha=35)
    
    draw_top_bar(draw, act_num=act_lbl, edl_tc=edl_tc, shot_id=shot_id)
    draw_footer_bar(draw, "ANVILNEXT 2.0 BLUEPRINT // PARIS 1:1 METRIC RECONSTRUCTION & 25% SEAMLESS INTERIORS")
    
    cx = 1920 // 2
    cy = 1080 // 2
    
    buildings = [
        (-380, 80, 190, 260, True),
        (-140, -60, 230, 340, False),
        (160, 40, 210, 280, True),
        (400, -100, 170, 240, False),
        (-240, -280, 280, 200, False),
        (90, -300, 250, 220, True),
    ]
    
    f_sub = get_font(FONT_SERIF, 20)
    
    for ox, oy, bw, bh, has_interior in buildings:
        bx = cx + ox
        by = cy + oy
        col = GOLD if has_interior else TEAL
        fill_col = (213, 167, 100, 35) if has_interior else (138, 194, 187, 20)
        
        top_pts = [(bx, by - bh), (bx + bw // 2, by - bh - 30), (bx + bw, by - bh), (bx + bw // 2, by - bh + 30)]
        front_pts = [(bx, by - bh + 30), (bx + bw // 2, by - bh + 30), (bx + bw // 2, by + 30), (bx, by)]
        right_pts = [(bx + bw // 2, by - bh + 30), (bx + bw, by - bh), (bx + bw, by), (bx + bw // 2, by + 30)]
        
        draw.polygon(top_pts, fill=fill_col, outline=col, width=2)
        draw.polygon(front_pts, fill=fill_col, outline=col, width=1)
        draw.polygon(right_pts, fill=fill_col, outline=col, width=1)
        
        if has_interior:
            draw.text((bx + 15, by - bh + 45), "SEAMLESS INTERIOR", font=f_sub, fill=GOLD)
            
    # Telemetry HUD box on right
    tx1, ty1 = 1920 - 460, 150
    draw.rectangle([(tx1, ty1), (tx1 + 340, ty1 + 270)], fill=PANEL_BG, outline=TEAL, width=1)
    draw_corner_brackets(draw, tx1, ty1, tx1 + 340, ty1 + 270, arm=20, color=GOLD, width=1)
    
    f_hud = get_font(FONT_SERIF, 20)
    draw.text((tx1 + 20, ty1 + 20), "SYSTEM ARCHITECTURE:", font=f_hud, fill=GOLD)
    draw.text((tx1 + 20, ty1 + 65), "SCALE: TRUE 1:1 METRIC", font=f_sub, fill=WHITE)
    draw.text((tx1 + 20, ty1 + 105), "SEAMLESS INTERIORS: 25%", font=f_sub, fill=GOLD)
    draw.text((tx1 + 20, ty1 + 145), "LOADING SCREENS: ZERO", font=f_sub, fill=TEAL)
    draw.text((tx1 + 20, ty1 + 185), "BUILDINGS: > 3,000", font=f_sub, fill=WHITE)
    draw.text((tx1 + 20, ty1 + 225), "GLOBAL ILLUM: 128 LIGHTS", font=f_sub, fill=WHITE)
    
    return im.convert("RGB")

# ==============================================================================
# 10. ARCHIVAL EVIDENCE: 1789 BASTILLE COPPERPLATE ENGRAVING
# ==============================================================================
def render_bastille_frame(progress=1.0, shot_id="SHOT-006", act_lbl="ACT I", edl_tc="00:24:50:00"):
    """Render 1789 Bastille Engraving with 2.5D push-in and red forensic highlight."""
    im = Image.new("RGBA", (1920, 1080), (14, 12, 10))
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=100, alpha=15)
    
    draw_top_bar(draw, act_num=act_lbl, edl_tc=edl_tc, shot_id=shot_id)
    draw_footer_bar(draw, "HISTORICAL ARCHIVES // STORMING OF THE BASTILLE — 14 JULY 1789 (COPPERPLATE ENGRAVING)")
    
    # Outer frame
    gx1, gy1, gx2, gy2 = 220, 140, 1920 - 220, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=(20, 17, 15, 230), outline=(213, 167, 100, 150), width=2)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=35, color=GOLD, width=2)
    
    f_title = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    
    draw.text((gx1 + 50, gy1 + 35), "ARCHIVAL RECORD #1789-BASTILLE // COPPERPLATE PRINT", font=f_title, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "MUSEE CARNAVALET ARCHIVES  •  PARIS REVOLUTIONARY COLLECTION", font=f_sub, fill=TEAL)
    
    # Engraving architectural illustration sketch in center
    cx = 1920 // 2
    cy = 1080 // 2 + 30
    
    # Fortress Towers
    draw.rectangle([(cx - 320, cy - 140), (cx - 160, cy + 160)], fill=(30, 26, 23), outline=(138, 194, 187, 160), width=2)
    draw.rectangle([(cx + 160, cy - 140), (cx + 320, cy + 160)], fill=(30, 26, 23), outline=(138, 194, 187, 160), width=2)
    draw.rectangle([(cx - 160, cy - 80), (cx + 160, cy + 160)], fill=(25, 22, 19), outline=(138, 194, 187, 140), width=2)
    
    # Fortress Drawbridge Gate
    draw.polygon([(cx - 70, cy + 160), (cx + 70, cy + 160), (cx + 50, cy + 50), (cx - 50, cy + 50)], outline=GOLD, width=2)
    
    # Red forensic highlight box framing the drawbridge gate
    gate_hl_w = int(220 * min(progress * 1.4, 1.0))
    draw.rectangle([(cx - 110, cy + 30), (cx - 110 + gate_hl_w, cy + 175)], fill=(230, 69, 83, 40), outline=CRIMSON, width=2)
    draw.text((cx - 100, cy + 5), "TARGET: MAIN GATE DRAWBRIDGE", font=f_sub, fill=CRIMSON)
    
    # Stamp
    stamp_x = gx2 - 250
    stamp_y = gy2 - 90
    draw.rectangle([(stamp_x, stamp_y), (stamp_x + 190, stamp_y + 50)], outline=CRIMSON, width=2)
    draw.text((stamp_x + 18, stamp_y + 12), "EVIDENCE #01.5", font=f_sub, fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 11. DATA VISUALIZATION: PLACE DE LA CONCORDE 5,000 NPC CROWD DENSITY (SHOT-016)
# ==============================================================================
def render_crowd_density_frame(progress=1.0):
    """Render Place de la Concorde 5,000 AI NPC crowd density heat map."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=60, alpha=20)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc="01:17:50:00", shot_id="SHOT-016")
    draw_footer_bar(draw, "TECHNICAL BENCHMARK // PLACE DE LA CONCORDE — 5,000 SIMULTANEOUS INDEPENDENT AI AGENTS")
    
    gx1, gy1, gx2, gy2 = 200, 140, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=TEAL, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_hud = get_font(FONT_SERIF, 20)
    
    draw.text((gx1 + 50, gy1 + 35), "AI CROWD SIMULATION DENSITY // PLACE DE LA CONCORDE", font=f_head, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "ANVILNEXT 2.0 MULTI-AGENT INFERENCE ENGINE  •  PARIS 1789", font=f_sub, fill=TEAL)
    
    # Large circular plaza with heat particles
    cx = 1920 // 2 - 160
    cy = 1080 // 2 + 30
    
    # Outer plaza ring
    draw.ellipse([(cx - 320, cy - 320), (cx + 320, cy + 320)], outline=(138, 194, 187, 80), width=2)
    draw.ellipse([(cx - 200, cy - 200), (cx + 200, cy + 200)], outline=(213, 167, 100, 100), width=1)
    draw.line([(cx - 360, cy), (cx + 360, cy)], fill=(138, 194, 187, 40), width=1)
    draw.line([(cx, cy - 360), (cx, cy + 360)], fill=(138, 194, 187, 40), width=1)
    
    # Guillotine Scaffold center point
    draw.rectangle([(cx - 25, cy - 25), (cx + 25, cy + 25)], fill=(230, 69, 83, 180), outline=CRIMSON, width=2)
    draw.text((cx - 50, cy - 50), "SCAFFOLD", font=f_hud, fill=CRIMSON)
    
    # Dense particle crowd swarm (deterministic based on seed)
    import random
    rng = random.Random(42)
    num_dots = int(1200 * min(progress * 1.3, 1.0))
    for _ in range(num_dots):
        rad = rng.uniform(30, 310)
        ang = rng.uniform(0, 6.283)
        px = int(cx + rad * math.cos(ang))
        py = int(cy + rad * math.sin(ang))
        # Color based on radius (hot core crimson/gold, outer teal)
        dot_col = CRIMSON if rad < 120 else GOLD if rad < 220 else TEAL
        draw.rectangle([(px, py), (px + 2, py + 2)], fill=dot_col)
        
    # Right-side Telemetry Panel
    rx1, ry1 = 1920 - 580, 200
    draw.rectangle([(rx1, ry1), (rx1 + 340, ry1 + 340)], fill=(14, 18, 22, 240), outline=GOLD, width=1)
    draw.text((rx1 + 25, ry1 + 25), "AGENT TELEMETRY:", font=f_head, fill=GOLD)
    draw.text((rx1 + 25, ry1 + 80), f"SIMULATED NPCS: {int(5000 * min(progress * 1.2, 1.0)):,}", font=f_sub, fill=WHITE)
    draw.text((rx1 + 25, ry1 + 125), "AI LOGIC: INDEPENDENT MORALE", font=f_sub, fill=TEAL)
    draw.text((rx1 + 25, ry1 + 170), "ANIMATION BLEND: 32 BONES", font=f_sub, fill=WHITE)
    draw.text((rx1 + 25, ry1 + 215), "CPU THREAD COST: 100% SAT", font=f_sub, fill=CRIMSON)
    draw.text((rx1 + 25, ry1 + 260), "DRAW CALL FLOOD: > 50,000", font=f_sub, fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 12. ARCHIVAL EVIDENCE: CAROLINE MIOUSSE DEVELOPER DOSSIER (SHOT-020)
# ==============================================================================
def render_caroline_miousse_frame(progress=1.0):
    """Render Senior Level Artist Caroline Miousse 2-year Notre Dame dossier."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc="01:40:00:00", shot_id="SHOT-020")
    draw_footer_bar(draw, "HISTORICAL RECONSTRUCTION // SENIOR LEVEL ARTIST CAROLINE MIOUSSE — 2 YEARS ON NOTRE-DAME")
    
    gx1, gy1, gx2, gy2 = 200, 140, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=GOLD, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_body = get_font(FONT_SERIF, 24)
    
    draw.text((gx1 + 50, gy1 + 35), "UBISOFT MONTREAL // LEAD ARCHITECTURAL RESEARCH DOSSIER", font=f_head, fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "CAROLINE MIOUSSE  •  SENIOR LEVEL ARTIST (2012 — 2014)", font=f_sub, fill=TEAL)
    
    # Left Card: Artist Profile
    ax1, ay1 = gx1 + 50, gy1 + 130
    draw.rectangle([(ax1, ay1), (ax1 + 420, ay1 + 560)], fill=(18, 22, 26, 230), outline=TEAL, width=1)
    draw.rectangle([(ax1 + 30, ay1 + 30), (ax1 + 390, ay1 + 350)], fill=(25, 30, 35), outline=GOLD, width=1)
    
    # Stylized profile silhouette
    pcx, pcy = ax1 + 210, ay1 + 190
    draw.ellipse([(pcx - 50, pcy - 70), (pcx + 50, pcy + 30)], outline=TEAL, width=2)
    draw.arc([(pcx - 90, pcy + 20), (pcx + 90, pcy + 140)], start=180, end=360, fill=TEAL, width=2)
    draw.text((ax1 + 85, ay1 + 310), "CAROLINE MIOUSSE", font=f_sub, fill=GOLD)
    
    draw.text((ax1 + 30, ay1 + 380), "ROLE: LEAD CATHEDRAL MODELER", font=f_sub, fill=WHITE)
    draw.text((ax1 + 30, ay1 + 420), "DURATION: 24 MONTHS (FULL-TIME)", font=f_sub, fill=GOLD)
    draw.text((ax1 + 30, ay1 + 460), "BRICK-BY-BRICK RECONSTRUCTION", font=f_sub, fill=TEAL)
    draw.text((ax1 + 30, ay1 + 500), "ACCURACY: 1:1 TRUE METRIC", font=f_sub, fill=WHITE)
    
    # Right: Cathedral Blueprint Specs
    bx1 = ax1 + 460
    draw.rectangle([(bx1, ay1), (gx2 - 50, ay1 + 560)], fill=(14, 18, 22, 230), outline=(138, 194, 187, 80), width=1)
    draw.text((bx1 + 40, ay1 + 35), "NOTRE-DAME ARCHITECTURAL RECONSTRUCTION METRICS:", font=f_head, fill=GOLD)
    
    specs = [
        ("TOTAL POLYGON BUDGET", "Over 3,000,000 triangles dedicated exclusively to the cathedral"),
        ("HISTORICAL TEXTURE MAPS", "Scanned historical stone textures & authentic Parisian limestone"),
        ("THE ANACRONISTIC SPIRE", "Spire included Eugène Viollet-le-Duc design (1844) for player recognition"),
        ("SEAMLESS INTERIOR ACCESS", "Fully playable interior without a single loading screen transition"),
        ("2019 CATHEDRAL FIRE PRESERVATION", "Digital scans served as global architectural reference after the tragic fire")
    ]
    
    for i, (title, desc) in enumerate(specs):
        sy = ay1 + 100 + i * 88
        draw.text((bx1 + 40, sy), f"• {title}", font=f_sub, fill=TEAL)
        draw.text((bx1 + 60, sy + 30), desc, font=get_font(FONT_SERIF, 19), fill=WHITE)
        
    return im.convert("RGB")

# ==============================================================================
# 13. TIMELINE: CRITICAL DEVELOPMENT MILESTONES (SHOT-025)
# ==============================================================================
def render_timeline_frame(progress=1.0):
    """Render glowing animated horizontal timeline cursor sliding from E3 to launch."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc="02:08:00:00", shot_id="SHOT-025")
    draw_footer_bar(draw, "CHRONOLOGY // CRITICAL PRODUCTION MILESTONES & SHIPPING DEADLINE")
    
    gx1, gy1, gx2, gy2 = 200, 160, 1920 - 200, 920
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=TEAL, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_date = get_font(FONT_SERIF, 26)
    
    draw.text((gx1 + 60, gy1 + 45), "ROADMAP TO CATASTROPHE // 2014 SHIPPING TIMELINE", font=f_head, fill=GOLD)
    draw.text((gx1 + 60, gy1 + 90), "THE NARROWING WINDOW BETWEEN MARKETING PROMISE AND CODE READINESS", font=f_sub, fill=TEAL)
    
    # Horizontal Timeline Axis
    line_y = 1080 // 2 + 40
    lx1 = gx1 + 80
    lx2 = gx2 - 80
    draw.line([(lx1, line_y), (lx2, line_y)], fill=(138, 194, 187, 100), width=4)
    
    # 4 Key Nodes
    nodes = [
        ("JUNE 9, 2014", "E3 WORLD PREMIERE", "Gameplay trailer stuns industry; promises 1:1 Paris & no loading screens", TEAL),
        ("AUG 28, 2014", "2-WEEK DELAY", "Ubisoft delays launch from Oct 28 to Nov 11 to 'polish day-one experience'", GOLD),
        ("NOV 11, 2014", "NORTH AMERICAN LAUNCH", "Embargo lifts 12 hours AFTER game is on store shelves; game is critically broken", CRIMSON),
        ("NOV 27, 2014", "CEO FORMAL APOLOGY", "CEO Yannis Mallat issues public apology and offers free AAA games to players", GOLD)
    ]
    
    step_w = (lx2 - lx1) / 3
    curr_x = lx1 + (lx2 - lx1) * min(progress * 1.25, 1.0)
    
    for i, (date_str, title_str, desc_str, col) in enumerate(nodes):
        nx = int(lx1 + i * step_w)
        reached = curr_x >= nx
        node_col = col if reached else MUTED_GRAY
        
        # Circle on line
        draw.ellipse([(nx - 14, line_y - 14), (nx + 14, line_y + 14)], fill=(18, 23, 25), outline=node_col, width=3)
        if reached:
            draw.ellipse([(nx - 6, line_y - 6), (nx + 6, line_y + 6)], fill=node_col)
            
        # Top label (Date)
        draw.text((nx - 80, line_y - 65), date_str, font=f_date, fill=node_col)
        
        # Bottom card
        by = line_y + 35
        card_w = 280
        draw.rectangle([(nx - card_w // 2, by), (nx + card_w // 2, by + 160)], fill=(16, 20, 24, 220), outline=node_col, width=1)
        draw.text((nx - card_w // 2 + 15, by + 15), title_str, font=get_font(FONT_SERIF, 20), fill=GOLD if reached else MUTED_GRAY)
        
        lines = wrap_text(draw, desc_str, get_font(FONT_SERIF, 17), card_w - 30)
        for li, l in enumerate(lines[:3]):
            draw.text((nx - card_w // 2 + 15, by + 55 + li * 24), l, font=get_font(FONT_SERIF, 17), fill=WHITE if reached else MUTED_GRAY)
            
    # Cursor head
    draw.line([(int(curr_x), line_y - 30), (int(curr_x), line_y + 30)], fill=WHITE, width=2)
    
    return im.convert("RGB")

# ==============================================================================
# 14. FINANCIAL IMPACT: UBISOFT MARKET CAP EVAPORATION (SHOT-054)
# ==============================================================================
def render_market_cap_frame(progress=1.0):
    """Render financial market capitalization crash (-9.1% drop post-launch)."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_grid_background(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT III", edl_tc="04:39:00:00", shot_id="SHOT-054")
    draw_footer_bar(draw, "FINANCIAL VALUATION COLLAPSE // EURONEXT PARIS — UBISOFT ENTERTAINMENT S.A. (UBI.PA)")
    
    gx1, gy1, gx2, gy2 = 200, 150, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=PANEL_BG, outline=CRIMSON, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    f_head = get_font(FONT_SERIF, 32)
    f_sub = get_font(FONT_SERIF, 22)
    f_huge = get_font(FONT_SERIF, 72)
    
    draw.text((gx1 + 60, gy1 + 45), "SHAREHOLDER WEALTH CONTRACTION // LAUNCH WEEK STOCK REACTION", font=f_head, fill=CRIMSON)
    draw.text((gx1 + 60, gy1 + 90), "EURONEXT PARIS TRADING DESK  •  NOVEMBER 12 — 14, 2014", font=f_sub, fill=TEAL)
    
    # Left: Big bold numbers
    num_y = gy1 + 170
    draw.text((gx1 + 60, num_y), "-9.12%", font=f_huge, fill=CRIMSON)
    draw.text((gx1 + 60, num_y + 90), "SINGLE-DAY INTRADAY SHARE PRICE PLUNGE", font=f_sub, fill=WHITE)
    
    draw.text((gx1 + 60, num_y + 160), "OVER €150,000,000", font=get_font(FONT_SERIF, 46), fill=GOLD)
    draw.text((gx1 + 60, num_y + 225), "MARKET CAPITALIZATION EVAPORATED IN 48 HOURS", font=f_sub, fill=WHITE)
    
    # Right: Stock Chart Graphic
    cx1 = gx1 + 750
    cx2 = gx2 - 60
    cy1 = gy1 + 160
    cy2 = gy2 - 60
    draw.rectangle([(cx1, cy1), (cx2, cy2)], fill=(14, 18, 22, 240), outline=(138, 194, 187, 80), width=1)
    draw.text((cx1 + 30, cy1 + 25), "UBI.PA STOCK TICKER // 5-DAY TRAJECTORY", font=f_sub, fill=TEAL)
    
    # Graph points
    pts = [
        (cx1 + 40, cy1 + 90),
        (cx1 + 150, cy1 + 80),
        (cx1 + 260, cy1 + 95),
        (cx1 + 370, cy1 + 220), # Plunge on Nov 12
        (cx1 + 480, cy1 + 380), # Nov 13 bottom
        (cx1 + 600, cy1 + 360)  # Nov 14 slight rebound
    ]
    
    # Animate line drawing
    curr_pts = []
    max_idx = int(len(pts) * min(progress * 1.3, 1.0))
    for p_idx in range(max(1, max_idx)):
        curr_pts.append(pts[p_idx])
        
    if len(curr_pts) >= 2:
        for p_idx in range(len(curr_pts) - 1):
            p1 = curr_pts[p_idx]
            p2 = curr_pts[p_idx + 1]
            draw.line([p1, p2], fill=CRIMSON, width=4)
            draw.ellipse([(p1[0] - 5, p1[1] - 5), (p1[0] + 5, p1[1] + 5)], fill=GOLD)
        draw.ellipse([(curr_pts[-1][0] - 6, curr_pts[-1][1] - 6), (curr_pts[-1][0] + 6, curr_pts[-1][1] + 6)], fill=CRIMSON)
        
    return im.convert("RGB")

# ==============================================================================
# 15. GRAND OUTRO EPILOGUE CREDITS (SHOT-172)
# ==============================================================================
def render_outro_frame(progress=1.0):
    """Render stark broadcast documentary credits & closing epilogue."""
    im = Image.new("RGBA", (1920, 1080), (10, 12, 14))
    draw = ImageDraw.Draw(im, "RGBA")
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    f_title = get_font(FONT_SERIF, 44)
    f_sub = get_font(FONT_SERIF, 24)
    f_credit = get_font(FONT_SERIF, 20)
    
    alpha_prog = min(progress * 1.5, 1.0)
    col_white = (255, 255, 255, int(255 * alpha_prog))
    col_gold = (213, 167, 100, int(255 * alpha_prog))
    col_teal = (138, 194, 187, int(255 * alpha_prog))
    
    draw.text((cx - 360, cy - 100), "AN INVESTIGATION INTO ASSASSIN'S CREED: UNITY", font=f_title, fill=col_white)
    draw.line([(cx - 200, cy - 30), (cx + 200, cy - 30)], fill=col_gold, width=2)
    draw.text((cx - 280, cy), "PRODUCED IN ACCORDANCE WITH LEMiNO DOCUMENTARY STANDARDS", font=f_sub, fill=col_teal)
    draw.text((cx - 150, cy + 60), "15:00.00 MASTER EPISODE // 2026", font=f_credit, fill=col_gold)
    
    return im.convert("RGB")


def render_clip_to_mp4(frame_func, duration_sec, out_mp4, fps=30):
    """Render a dynamic animated motion graphic sequence to an MP4 video clip."""
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    total_frames = int(duration_sec * fps)
    
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-an",
        out_mp4
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f in range(total_frames):
        prog = f / max(total_frames - 1, 1)
        im = frame_func(prog)
        proc.stdin.write(im.tobytes())
        
    proc.stdin.close()
    proc.wait()
    return out_mp4

def generate_shot_graphic_clip(shot, out_path):
    """
    Selects the exact appropriate broadcast motion graphic composition
    with strict deterministic Shot ID binding.
    Returns out_path if a dedicated graphic exists, or None if the shot
    should be cut from authentic documentary B-roll footage.
    """
    sid = shot["id"].upper()
    dur = shot["duration"]
    stype = shot["type"]
    gfx = shot["graphics"]
    vis = shot["visual"]
    s_tc = shot.get("start_tc", "00:00:00:00")
    
    # 1. Deterministic Explicit Shot ID Mapping
    if sid in ["SHOT-001", "SHOT-002", "SHOT-003"]:
        return render_clip_to_mp4(render_grand_title_frame, dur, out_path)
        
    if sid in ["SHOT-006"]:
        return render_clip_to_mp4(lambda p: render_bastille_frame(p, shot_id=sid, edl_tc=s_tc), dur, out_path)
        
    if sid in ["SHOT-012", "SHOT-013"]:
        return render_clip_to_mp4(lambda p: render_graphic_broll_blueprint(p, shot_id=sid, edl_tc=s_tc), dur, out_path)

    if sid in ["SHOT-016"]:
        return render_clip_to_mp4(render_crowd_density_frame, dur, out_path)

    if sid in ["SHOT-020"]:
        return render_clip_to_mp4(render_caroline_miousse_frame, dur, out_path)

    if sid in ["SHOT-025"]:
        return render_clip_to_mp4(render_timeline_frame, dur, out_path)
        
    if sid in ["SHOT-043", "SHOT-044", "SHOT-045"]:
        return render_clip_to_mp4(render_digital_foundry_frame, dur, out_path)

    if sid in ["SHOT-054"]:
        return render_clip_to_mp4(render_market_cap_frame, dur, out_path)
        
    if sid in ["SHOT-064", "SHOT-065"]:
        return render_clip_to_mp4(render_cpu_architecture_frame, dur, out_path)
        
    if sid in ["SHOT-074", "SHOT-075"]:
        return render_clip_to_mp4(render_cpu_architecture_frame, dur, out_path)
        
    if sid in ["SHOT-087", "SHOT-088"]:
        return render_clip_to_mp4(render_archival_apology_frame, dur, out_path)
        
    if sid in ["SHOT-092", "SHOT-093", "SHOT-094"]:
        return render_clip_to_mp4(render_archival_free_game_frame, dur, out_path)
        
    if sid in ["SHOT-103"]:
        return render_clip_to_mp4(render_community_sentiment_frame, dur, out_path)
        
    if sid in ["SHOT-120", "SHOT-121"]:
        return render_clip_to_mp4(render_sales_comparison_frame, dur, out_path)
        
    if sid in ["SHOT-145", "SHOT-146"]:
        return render_clip_to_mp4(render_grand_title_frame, dur, out_path)

    if sid in ["SHOT-172"]:
        return render_clip_to_mp4(render_outro_frame, dur, out_path)

    # 2. Act Chapter Cards (Strictly on Chapter/Transition shots only)
    if sid in ["SHOT-009", "SHOT-028", "SHOT-055", "SHOT-086", "SHOT-119", "SHOT-144"]:
        act_lbl = "ACT // " + sid
        if sid == "SHOT-009": act_lbl = "ACT I"
        elif sid == "SHOT-028": act_lbl = "ACT II"
        elif sid == "SHOT-055": act_lbl = "ACT III"
        elif sid == "SHOT-086": act_lbl = "ACT IV"
        elif sid == "SHOT-119": act_lbl = "ACT V"
        elif sid == "SHOT-144": act_lbl = "ACT VI"
        
        act_title = gfx if gfx else "INVESTIGATIVE DOSSIER"
        act_sub = vis[:60] if vis else "PARIS 1789 — 2019"
        return render_clip_to_mp4(lambda p: render_chapter_frame(act_lbl, act_title, act_sub, p), dur, out_path)
        
    # 3. Typography Quote Cards (Only when quote marks explicitly appear in graphics or visual)
    if ("Typography" in stype or "Quote" in stype) and (gfx.startswith("“") or gfx.startswith('"') or vis.startswith("“") or vis.startswith('"')):
        clean_quote = gfx.replace('“', '"').replace('”', '"')
        if not clean_quote or len(clean_quote) < 5:
            clean_quote = vis
        return render_clip_to_mp4(lambda p: render_typography_frame(clean_quote, f"{sid} // LEMINO DOSSIER", p), dur, out_path)
        
    # STRICT RULE: No fallback to blueprint!
    # Returns None so caller cuts from authentic high-res documentary B-roll footage!
    return None

if __name__ == "__main__":
    print("Testing generate_shot_graphic_clip...")
    test_shot = {
        "id": "SHOT-009",
        "duration": 5.0,
        "type": "Transition / Chapter",
        "graphics": "ACT I // THE 1:1 REVOLUTION",
        "visual": "Paris 1789 and the promise of next-gen architecture"
    }
    out_mp4 = "/tmp/lemino_test_graphics/shot-009_test.mp4"
    generate_shot_graphic_clip(test_shot, out_mp4)
    print(f"Generated {out_mp4} ({os.path.getsize(out_mp4)} bytes)")
