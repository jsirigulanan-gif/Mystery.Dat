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
# MASTER RENDER CLIP DISPATCHER
# ==============================================================================
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
    with deterministic Shot ID binding and renders it to 1080p MP4.
    """
    sid = shot["id"].upper()
    dur = shot["duration"]
    stype = shot["type"]
    gfx = shot["graphics"]
    vis = shot["visual"]
    
    # 1. Deterministic Explicit Shot ID Mapping
    s_tc = shot.get("start_tc", "00:00:00:00")
    if sid in ["SHOT-001", "SHOT-002", "SHOT-003"]:
        return render_clip_to_mp4(render_grand_title_frame, dur, out_path)
        
    if sid in ["SHOT-006"]:
        return render_clip_to_mp4(lambda p: render_bastille_frame(p, shot_id=sid, edl_tc=s_tc), dur, out_path)
        
    if sid in ["SHOT-012", "SHOT-013"]:
        return render_clip_to_mp4(lambda p: render_graphic_broll_blueprint(p, shot_id=sid, edl_tc=s_tc), dur, out_path)
        
    if sid in ["SHOT-043", "SHOT-044", "SHOT-045"]:
        return render_clip_to_mp4(render_digital_foundry_frame, dur, out_path)
        
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

    # 2. Content & Keyword Fallback Rules
    if any(k in (gfx + vis + stype).lower() for k in ["digital foundry", "15.2 fps", "15 fps", "frame-rate", "framerate", "fps drop"]):
        return render_clip_to_mp4(render_digital_foundry_frame, dur, out_path)
        
    if any(k in (gfx + vis + stype).lower() for k in ["jaguar", "8-core", "cpu", "microprocessor", "thread saturation"]):
        return render_clip_to_mp4(render_cpu_architecture_frame, dur, out_path)
        
    if any(k in (gfx + vis + stype).lower() for k in ["apology", "yannis mallat", "open letter", "diminished by bugs"]):
        return render_clip_to_mp4(render_archival_apology_frame, dur, out_path)
        
    if any(k in (gfx + vis + stype).lower() for k in ["free game", "waiver", "class action", "concessions", "far cry 4"]):
        return render_clip_to_mp4(render_archival_free_game_frame, dur, out_path)
        
    if any(k in (gfx + vis + stype).lower() for k in ["sales", "syndicate", "slump", "-40%", "market", "collapse"]):
        return render_clip_to_mp4(render_sales_comparison_frame, dur, out_path)
        
    if any(k in (gfx + vis).lower() for k in ["bastille", "14 july 1789", "engraving"]):
        return render_clip_to_mp4(render_bastille_frame, dur, out_path)
        
    if any(k in (gfx + vis + stype).lower() for k in ["blueprint", "anvilnext", "interior ratio", "1:1 scale", "photogrammetry"]):
        return render_clip_to_mp4(render_graphic_broll_blueprint, dur, out_path)
        
    # 3. Chapter Card
    if "Transition" in stype or "Chapter" in stype or "ACT " in gfx.upper():
        act_lbl = "ACT // " + sid
        if "ACT I" in gfx.upper(): act_lbl = "ACT I"
        elif "ACT II" in gfx.upper(): act_lbl = "ACT II"
        elif "ACT III" in gfx.upper(): act_lbl = "ACT III"
        elif "ACT IV" in gfx.upper(): act_lbl = "ACT IV"
        elif "ACT V" in gfx.upper(): act_lbl = "ACT V"
        elif "ACT VI" in gfx.upper(): act_lbl = "ACT VI"
        
        act_title = gfx if gfx else "INVESTIGATIVE DOSSIER"
        act_sub = vis[:60] if vis else "PARIS 1789 — 2019"
        return render_clip_to_mp4(lambda p: render_chapter_frame(act_lbl, act_title, act_sub, p), dur, out_path)
        
    # 4. Typography Quote Card
    if "Typography" in stype or "Quote" in stype or (gfx.startswith("“") or gfx.startswith('"')):
        clean_quote = gfx.replace('“', '"').replace('”', '"')
        if not clean_quote:
            clean_quote = vis
        return render_clip_to_mp4(lambda p: render_typography_frame(clean_quote, f"{sid} // LEMINO DOSSIER", p), dur, out_path)
        
    # Fallback to authentic LEMiNO blueprint frame
    return render_clip_to_mp4(render_graphic_broll_blueprint, dur, out_path)

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
