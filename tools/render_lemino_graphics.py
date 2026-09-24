#!/usr/bin/env python3
"""
LEMiNO Broadcast Motion Graphics Renderer (Version 3.0 - Ultra Clean Overlays)
Re-engineered from scratch to eradicate PowerPoint/PPT card aesthetics.
Features:
- Full Unicode Kanit Typography (Zero Tofu / Square Boxes)
- Sleek, Modern, Minimalist Infographics & Telemetry HUDs
- Cinematic Overlays with 100% WCAG AA contrast compliance
- Glowing Neon Curves, Clean Bar Charts, Silicon Die Diagrams, and Forensic Highlights
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Full Unicode Font Suite (Latin, Thai, Digits 0-9, Accents, Dashes, Punctuation)
FONT_UNIVERSAL = "/home/keng/.local/share/lemino_fonts/universal.ttf"
FONT_BOLD = "/home/keng/.local/share/lemino_fonts/thai-bold.ttf"
FONT_MEDIUM = "/home/keng/.local/share/lemino_fonts/thai-medium.ttf"

# Canonical LEMiNO Color Palette
BG_COLOR = (14, 18, 20)           # #0e1214 Deep Charcoal Black
TEAL = (138, 194, 187)            # #8ac2bb LEMiNO Turquoise Primary
GOLD = (213, 167, 100)            # #d5a764 Warm Amber Gold Accent
WHITE = (255, 255, 255)           # Pure White
OFF_WHITE = (238, 230, 211)       # #eee6d3 Stone Off-White
CRIMSON = (230, 69, 83)           # #e64553 Alert Red / Drop Indicator
MUTED_GRAY = (115, 130, 135)      # Technical Sub-labels
DARK_GLASS = (16, 21, 24, 215)    # Sleek Translucent HUD Backplate

def get_font(size, weight="regular"):
    font_path = FONT_BOLD if weight == "bold" else FONT_MEDIUM if weight == "medium" else FONT_UNIVERSAL
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

def draw_corner_brackets(draw, x1, y1, x2, y2, arm=25, color=TEAL, width=1):
    """Draw sleek technical HUD framing brackets at 4 corners."""
    draw.line([(x1, y1), (x1 + arm, y1)], fill=color, width=width)
    draw.line([(x1, y1), (x1, y1 + arm)], fill=color, width=width)
    draw.line([(x2, y1), (x2 - arm, y1)], fill=color, width=width)
    draw.line([(x2, y1), (x2, y1 + arm)], fill=color, width=width)
    draw.line([(x1, y2), (x1 + arm, y2)], fill=color, width=width)
    draw.line([(x1, y2), (x1, y2 - arm)], fill=color, width=width)
    draw.line([(x2, y2), (x2 - arm, y2)], fill=color, width=width)
    draw.line([(x2, y2), (x2, y2 - arm)], fill=color, width=width)

def draw_top_bar(draw, act_num="ACT I", edl_tc="00:00:00:00", shot_id="SHOT-001"):
    """LEMiNO standard minimalist top header bar."""
    f_bar = get_font(18, weight="medium")
    draw.text((118, 55), "LEMINO INVESTIGATION // CASE FILE #2014-ACU", font=f_bar, fill=TEAL)
    right_text = f"{shot_id}  |  TC {edl_tc}"
    bbox = f_bar.getbbox(right_text)
    w = bbox[2] - bbox[0]
    draw.text((1920 - 118 - w, 55), right_text, font=f_bar, fill=GOLD)
    draw.line([(118, 88), (1920 - 118, 88)], fill=(138, 194, 187, 50), width=1)

def draw_footer_bar(draw, subtitle="PARIS 1789 - 2019 // ANVILNEXT 2.0 ARCHITECTURAL ANALYSIS"):
    """LEMiNO standard minimalist footer bar."""
    f_foot = get_font(16, weight="regular")
    draw.line([(118, 1000), (1920 - 118, 1000)], fill=(138, 194, 187, 50), width=1)
    draw.text((118, 1015), subtitle, font=f_foot, fill=OFF_WHITE)
    draw.text((1920 - 118 - 180, 1015), "BROADCAST MASTER", font=f_foot, fill=TEAL)

def draw_subtle_grid(draw, width=1920, height=1080, cell_size=120, alpha=15):
    """Draw subtle technical blueprint grid without visual clutter."""
    grid_col = (138, 194, 187, alpha)
    for x in range(0, width, cell_size):
        draw.line([(x, 0), (x, height)], fill=grid_col, width=1)
    for y in range(0, height, cell_size):
        draw.line([(0, y), (width, y)], fill=grid_col, width=1)

# ==============================================================================
# 1. GRAND TITLE CARD (SHOT-001, 002, 003)
# ==============================================================================
def render_grand_title_frame(progress):
    """Render Grand Title sequence frame (0.0 <= progress <= 1.0)."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=100, alpha=18)
    
    draw_top_bar(draw, act_num="COLD OPEN", edl_tc="00:00:15:00", shot_id="GRAND TITLE CARD")
    draw_footer_bar(draw, "LEMINO DOCUMENTARY INVESTIGATION // SPECIAL PRESENTATION")
    
    cx = 1920 // 2
    cy = 1080 // 2 - 25
    
    # Translucent glass backplate
    bp_w, bp_h = 1300, 420
    draw.rectangle([(cx - bp_w//2, cy - bp_h//2), (cx + bp_w//2, cy + bp_h//2)], fill=(12, 16, 18, 220), outline=(138, 194, 187, 70), width=1)
    draw_corner_brackets(draw, cx - bp_w//2, cy - bp_h//2, cx + bp_w//2, cy + bp_h//2, arm=35, color=TEAL, width=2)
    
    # Glowing animated geometric line
    line_w = int(min(progress * 1.5, 1.0) * (bp_w - 100))
    lx1 = cx - (bp_w - 100) // 2
    draw.line([(lx1, cy - 85), (lx1 + line_w, cy - 85)], fill=GOLD, width=2)
    
    # Typography
    f_sub = get_font(20, weight="medium")
    f_title = get_font(56, weight="bold")
    f_tag = get_font(22, weight="regular")
    
    # Category tag
    draw.text((cx - 580, cy - 140), "SPECIAL INVESTIGATIVE DOCUMENTARY", font=f_sub, fill=TEAL)
    
    # Main Grand Title
    draw.text((cx - 580, cy - 65), "ASSASSIN'S CREED: UNITY", font=f_title, fill=WHITE)
    
    # Subtitle
    draw.text((cx - 580, cy + 25), "THE 1:1 REVOLUTION AND THE COLLAPSE OF THE ANNUAL MACHINE", font=f_tag, fill=GOLD)
    
    # Metadata pill badges
    p_y = cy + 100
    pills = ["PARIS 1789", "E3 2014 REVEAL", "15.2 FPS COLLAPSE", "NOTRE-DAME 2019"]
    px = cx - 580
    for p in pills:
        draw.rectangle([(px, p_y), (px + 175, p_y + 36)], fill=(20, 26, 30, 220), outline=(138, 194, 187, 90), width=1)
        draw.text((px + 14, p_y + 8), p, font=get_font(14, weight="medium"), fill=OFF_WHITE)
        px += 190
        
    return im.convert("RGB")

# ==============================================================================
# 2. ACT CHAPTER TITLE CARDS (ACT I - VI)
# ==============================================================================
def render_chapter_frame(act_num, title, subtitle, progress=1.0):
    """Render sleek, cinematic chapter title overlay."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=120, alpha=15)
    
    draw_top_bar(draw, act_num=act_num, edl_tc="--:--:--:--", shot_id=act_num)
    draw_footer_bar(draw, f"DOCUMENTARY CHAPTER // {act_num} — {title}")
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    # Glass backplate
    bw, bh = 1100, 320
    draw.rectangle([(cx - bw//2, cy - bh//2), (cx + bw//2, cy + bh//2)], fill=(12, 16, 18, 225), outline=(138, 194, 187, 80), width=1)
    draw_corner_brackets(draw, cx - bw//2, cy - bh//2, cx + bw//2, cy + bh//2, arm=30, color=GOLD, width=2)
    
    # Act Roman Numeral
    f_act = get_font(38, weight="bold")
    draw.text((cx - bw//2 + 60, cy - bh//2 + 50), act_num, font=f_act, fill=GOLD)
    
    # Glowing divider rule
    draw.line([(cx - bw//2 + 60, cy - bh//2 + 105), (cx + bw//2 - 60, cy - bh//2 + 105)], fill=TEAL, width=1)
    
    # Chapter Title
    f_title = get_font(42, weight="bold")
    draw.text((cx - bw//2 + 60, cy - bh//2 + 130), title, font=f_title, fill=WHITE)
    
    # Subtitle / Time Context
    f_sub = get_font(20, weight="regular")
    draw.text((cx - bw//2 + 60, cy - bh//2 + 205), subtitle, font=f_sub, fill=MUTED_GRAY)
    
    return im.convert("RGB")

# ==============================================================================
# 3. DIGITAL FOUNDRY 15.2 FPS TELEMETRY GRAPH (SHOT-043, 044, 045)
# ==============================================================================
def render_digital_foundry_frame(progress=1.0):
    """Render ultra-clean Digital Foundry framerate crash telemetry graph."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT II", edl_tc="03:45:00:00", shot_id="SHOT-043")
    draw_footer_bar(draw, "PERFORMANCE FORENSICS // DIGITAL FOUNDRY PS4 & XBOX ONE FRAME-RATE BENCHMARK")
    
    gx1, gy1, gx2, gy2 = 180, 150, 1920 - 180, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=(138, 194, 187, 80), width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    # Header
    draw.text((gx1 + 50, gy1 + 35), "DIGITAL FOUNDRY PERFORMANCE AUDIT // CONSOLE HARDWARE BOTTLENECK", font=get_font(26, weight="bold"), fill=WHITE)
    draw.text((gx1 + 50, gy1 + 75), "SCENARIO: PLACE DE LA CONCORDE (5,000 NPC CROWD DENSITY TEST)", font=get_font(18, weight="medium"), fill=TEAL)
    
    # Graph dimensions
    chart_x1, chart_y1 = gx1 + 70, gy1 + 140
    chart_x2, chart_y2 = gx2 - 400, gy2 - 60
    
    # Horizontal reference lines (30 FPS target, 20 FPS, 15 FPS critical)
    ref_lines = [
        (30, "30 FPS [LOCKED TARGET]", TEAL),
        (25, "25 FPS", (100, 120, 125)),
        (20, "20 FPS [UNPLAYABLE THRESHOLD]", GOLD),
        (15, "15 FPS [CRITICAL COLLAPSE]", CRIMSON)
    ]
    
    for fps_val, lbl, col in ref_lines:
        y_norm = 1.0 - (fps_val - 10) / 25.0
        y_pos = int(chart_y1 + y_norm * (chart_y2 - chart_y1))
        draw.line([(chart_x1, y_pos), (chart_x2, y_pos)], fill=(*col[:3], 60), width=1)
        draw.text((chart_x1 - 65, y_pos - 10), f"{fps_val}", font=get_font(16, weight="bold"), fill=col)
        draw.text((chart_x1 + 15, y_pos - 22), lbl, font=get_font(13, weight="regular"), fill=col)
        
    # Animated neon curve points (30 -> 24 -> 18 -> 15.2 -> 16.5)
    total_pts = 80
    curve_pts = []
    max_step = int(total_pts * min(progress * 1.3, 1.0))
    
    for i in range(max_step):
        t = i / total_pts
        # S-curve dropping to 15.2 FPS
        if t < 0.25:
            fps = 30.0 - (t / 0.25) * 3.0 + np.sin(i * 0.8) * 0.4
        elif t < 0.65:
            dt = (t - 0.25) / 0.40
            fps = 27.0 - dt * 11.8 + np.sin(i * 1.2) * 0.7
        else:
            fps = 15.2 + np.sin(i * 1.5) * 0.9
            
        y_norm = 1.0 - (fps - 10) / 25.0
        px = chart_x1 + int(t * (chart_x2 - chart_x1))
        py = int(chart_y1 + y_norm * (chart_y2 - chart_y1))
        curve_pts.append((px, py))
        
    if len(curve_pts) > 1:
        # Glow layer
        draw.line(curve_pts, fill=(230, 69, 83, 90), width=6)
        # Core line
        draw.line(curve_pts, fill=CRIMSON, width=3)
        
    # Right Side Data Cards
    rx = gx2 - 360
    # Card 1: 15.2 FPS Crash Stat
    draw.rectangle([(rx, gy1 + 140), (rx + 310, gy1 + 310)], fill=(20, 26, 30, 220), outline=CRIMSON, width=1)
    draw.text((rx + 20, gy1 + 160), "MINIMUM RECORDED FPS", font=get_font(15, weight="medium"), fill=MUTED_GRAY)
    draw.text((rx + 20, gy1 + 195), "15.2", font=get_font(64, weight="bold"), fill=CRIMSON)
    draw.text((rx + 165, gy1 + 230), "FPS", font=get_font(24, weight="bold"), fill=CRIMSON)
    draw.text((rx + 20, gy1 + 270), "DROP FROM TARGET: -49.3%", font=get_font(15, weight="bold"), fill=CRIMSON)
    
    # Card 2: Frame Time Jitter
    draw.rectangle([(rx, gy1 + 335), (rx + 310, gy1 + 480)], fill=(20, 26, 30, 220), outline=GOLD, width=1)
    draw.text((rx + 20, gy1 + 355), "PEAK FRAME TIME", font=get_font(15, weight="medium"), fill=MUTED_GRAY)
    draw.text((rx + 20, gy1 + 385), "65.8 ms", font=get_font(38, weight="bold"), fill=GOLD)
    draw.text((rx + 20, gy1 + 440), "TARGET: 33.3 ms (30 FPS)", font=get_font(15, weight="regular"), fill=MUTED_GRAY)
    
    return im.convert("RGB")

# ==============================================================================
# 4. AMD JAGUAR 8-CORE CPU DIE SATURATION (SHOT-064, 065)
# ==============================================================================
def render_cpu_architecture_frame(progress=1.0):
    """Render clean AMD Jaguar 8-Core CPU saturation telemetry diagram."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT III", edl_tc="05:15:00:00", shot_id="SHOT-064")
    draw_footer_bar(draw, "HARDWARE ARCHITECTURE // AMD CUSTOM 8-CORE JAGUAR 1.6 GHz (PS4 & XBOX ONE)")
    
    gx1, gy1, gx2, gy2 = 180, 150, 1920 - 180, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=(138, 194, 187, 80), width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    draw.text((gx1 + 50, gy1 + 35), "MICROPROCESSOR THREAD OVERHEAD // 8-CORE DIE LAYOUT", font=get_font(26, weight="bold"), fill=WHITE)
    draw.text((gx1 + 50, gy1 + 75), "DIAGNOSIS: CROWD AI & DRAW CALL DISPATCH SATURATING HARDWARE CAPACITY", font=get_font(18, weight="medium"), fill=TEAL)
    
    # 8-Core Grid
    start_x = gx1 + 50
    start_y = gy1 + 130
    box_w = 345
    box_h = 160
    spacing_x = 35
    spacing_y = 30
    
    cores = [
        ("CORE 0", "MAIN GAME ENGINE", 88, TEAL),
        ("CORE 1", "CROWD AI (5,000 NPCs)", 99, CRIMSON),
        ("CORE 2", "INVERSE KINEMATICS", 94, CRIMSON),
        ("CORE 3", "AUDIO & AMBIENCE", 72, TEAL),
        ("CORE 4", "DIRECTX 11 DISPATCH", 98, CRIMSON),
        ("CORE 5", "CLOTH & PHYSICS", 85, GOLD),
        ("CORE 6", "VRAM STREAM QUEUE", 78, TEAL),
        ("CORE 7", "DRAW CALL PIPELINE", 100, CRIMSON)
    ]
    
    for idx, (cid, desc, base_load, col) in enumerate(cores):
        r = idx // 4
        c = idx % 4
        bx = start_x + c * (box_w + spacing_x)
        by = start_y + r * (box_h + spacing_y)
        
        load = min(100, int(base_load - 5 + 6 * math.sin(idx * 1.5 + progress * 5)))
        border_col = CRIMSON if load >= 95 else GOLD if load >= 85 else TEAL
        
        draw.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=(20, 26, 30, 220), outline=border_col, width=1)
        draw.text((bx + 20, by + 18), cid, font=get_font(18, weight="bold"), fill=WHITE)
        draw.text((bx + 20, by + 46), desc, font=get_font(14, weight="medium"), fill=MUTED_GRAY)
        draw.text((bx + box_w - 75, by + 18), f"{load}%", font=get_font(20, weight="bold"), fill=border_col)
        
        # Load meter bar
        bar_w = int((box_w - 40) * (load / 100.0) * min(progress * 1.2, 1.0))
        draw.rectangle([(bx + 20, by + 115), (bx + box_w - 20, by + 130)], fill=(10, 14, 16), outline=(60, 75, 80), width=1)
        draw.rectangle([(bx + 20, by + 115), (bx + 20 + bar_w, by + 130)], fill=border_col)
        
    # Bottom Telemetry Summary Callout
    bot_y = gy1 + 540
    draw.rectangle([(start_x, bot_y), (gx2 - 50, bot_y + 170)], fill=(20, 25, 28, 220), outline=GOLD, width=1)
    draw.text((start_x + 30, bot_y + 25), "TECHNICAL ROOT CAUSE SUMMARY:", font=get_font(18, weight="bold"), fill=GOLD)
    draw.text((start_x + 30, bot_y + 65), "• The 1.6 GHz clock speed of the AMD Jaguar cores lacked single-threaded IPC throughput.", font=get_font(17, weight="regular"), fill=OFF_WHITE)
    draw.text((start_x + 30, bot_y + 100), "• DirectX 11 API driver overhead bottlenecked Cores 1, 4, and 7 under 50,000 draw calls per frame.", font=get_font(17, weight="regular"), fill=OFF_WHITE)
    draw.text((start_x + 30, bot_y + 135), "• Result: GPU remained idle waiting for CPU command buffers, locking frame rates at 15-22 FPS.", font=get_font(17, weight="regular"), fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 5. YANNIS MALLAT APOLOGY STATEMENT (SHOT-087, 088)
# ==============================================================================
def render_archival_apology_frame(progress=1.0):
    """Render clean, high-contrast forensic exhibit of Yannis Mallat apology."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT IV", edl_tc="07:45:00:00", shot_id="SHOT-087")
    draw_footer_bar(draw, "UBISOFT MONTREAL ARCHIVES // OFFICIAL COMMUNITY STATEMENT — NOVEMBER 26, 2014")
    
    gx1, gy1, gx2, gy2 = 220, 150, 1920 - 220, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=GOLD, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=35, color=GOLD, width=2)
    
    # Header
    draw.text((gx1 + 60, gy1 + 40), "UBISOFT MONTREAL & TORONTO // FORENSIC EXHIBIT #07.1", font=get_font(24, weight="bold"), fill=GOLD)
    draw.text((gx1 + 60, gy1 + 80), "AN UPDATE ON ASSASSIN'S CREED UNITY FROM CEO YANNIS MALLAT", font=get_font(18, weight="medium"), fill=TEAL)
    draw.line([(gx1 + 60, gy1 + 120), (gx2 - 60, gy1 + 120)], fill=(138, 194, 187, 60), width=1)
    
    # Key Quotation Card
    qx1, qy1, qx2, qy2 = gx1 + 60, gy1 + 160, gx2 - 60, gy1 + 420
    draw.rectangle([(qx1, qy1), (qx2, qy2)], fill=(20, 26, 30, 230), outline=CRIMSON, width=2)
    draw_corner_brackets(draw, qx1, qy1, qx2, qy2, arm=20, color=CRIMSON, width=2)
    
    quote_text = (
        '"Unfortunately, at launch, the overall quality of the game was diminished '
        'by bugs and unexpected technical issues. I want to sincerely apologize on behalf '
        'of Ubisoft and the entire Assassin\'s Creed team."'
    )
    lines = wrap_text(draw, quote_text, get_font(28, weight="bold"), qx2 - qx1 - 80)
    cur_qy = qy1 + 45
    for l in lines:
        draw.text((qx1 + 40, cur_qy), l, font=get_font(28, weight="bold"), fill=WHITE)
        cur_qy += 45
        
    draw.text((qx1 + 40, qy2 - 50), "— YANNIS MALLAT, CEO OF UBISOFT MONTREAL & TORONTO", font=get_font(17, weight="medium"), fill=GOLD)
    
    # Concessions Breakdown Below
    cy = gy1 + 455
    draw.text((gx1 + 60, cy), "OFFICIAL CORPORATE CONCESSIONS ANNOUNCED:", font=get_font(20, weight="bold"), fill=TEAL)
    
    concessions = [
        ("DEAD KINGS EXPANSION", "Valued at $29.99 — Distributed FREE to all players worldwide"),
        ("FREE AAA GAME FOR SEASON PASS", "Eligible picks: Far Cry 4, Watch Dogs, The Crew, Rayman Legends"),
        ("CLASS-ACTION DISCHARGE", "Accepting free game legally forfeited right to sue Ubisoft")
    ]
    
    cy += 45
    for title, desc in concessions:
        draw.rectangle([(gx1 + 60, cy), (gx2 - 60, cy + 60)], fill=(20, 24, 28, 200), outline=(138, 194, 187, 70), width=1)
        draw.text((gx1 + 80, cy + 10), title, font=get_font(16, weight="bold"), fill=GOLD)
        draw.text((gx1 + 80, cy + 32), desc, font=get_font(15, weight="regular"), fill=OFF_WHITE)
        cy += 75
        
    return im.convert("RGB")

# ==============================================================================
# 6. FREE GAME LEGAL WAIVER (SHOT-092, 093, 094)
# ==============================================================================
def render_archival_free_game_frame(progress=1.0):
    """Render clean legal forensics of the Class-Action Waiver clause."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT IV", edl_tc="08:15:00:00", shot_id="SHOT-092")
    draw_footer_bar(draw, "LEGAL FORENSICS // UBISOFT SEASON PASS COMPENSATION CLAUSE & WAIVER OF LIABILITY")
    
    gx1, gy1, gx2, gy2 = 220, 150, 1920 - 220, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=CRIMSON, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=35, color=CRIMSON, width=2)
    
    draw.text((gx1 + 60, gy1 + 40), "UBISOFT REDEMPTION AGREEMENT // TERMS OF USE CLAUSE", font=get_font(24, weight="bold"), fill=CRIMSON)
    draw.text((gx1 + 60, gy1 + 80), "SECTION 4.2: UNCONDITIONAL WAIVER OF CLASS-ACTION RIGHTS", font=get_font(18, weight="medium"), fill=TEAL)
    draw.line([(gx1 + 60, gy1 + 120), (gx2 - 60, gy1 + 120)], fill=(230, 69, 83, 70), width=1)
    
    clause_box_y = gy1 + 160
    draw.rectangle([(gx1 + 60, clause_box_y), (gx2 - 60, clause_box_y + 260)], fill=(24, 20, 22, 230), outline=CRIMSON, width=2)
    
    clause_text = (
        '"You hereby unconditionally release and discharge Ubisoft Entertainment S.A., '
        'its affiliates and licensors from any and all claims, causes of action, damages '
        'or liabilities arising from the purchase or operation of Assassin\'s Creed: Unity."'
    )
    lines = wrap_text(draw, clause_text, get_font(24, weight="bold"), gx2 - gx1 - 200)
    cy = clause_box_y + 45
    for l in lines:
        draw.text((gx1 + 100, cy), l, font=get_font(24, weight="bold"), fill=WHITE)
        cy += 40
        
    draw.text((gx1 + 100, clause_box_y + 205), "STATUS: BINDING LEGAL DISCHARGE // FREE AAA GAME CONDITION", font=get_font(16, weight="bold"), fill=CRIMSON)
    
    # Forensic stamp
    draw.rectangle([(gx2 - 320, gy1 + 460), (gx2 - 80, gy1 + 540)], fill=(230, 69, 83, 40), outline=CRIMSON, width=2)
    draw.text((gx2 - 300, gy1 + 485), "LEGAL WAIVER BINDING", font=get_font(17, weight="bold"), fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 7. UK SALES SLUMP (-40%) BAR CHART (SHOT-120, 121)
# ==============================================================================
def render_sales_comparison_frame(progress=1.0):
    """Render modern minimalist bar chart comparing launch sales."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT V", edl_tc="10:15:00:00", shot_id="SHOT-120")
    draw_footer_bar(draw, "COMMERCIAL MARKET ANALYSIS // UK WEEK 1 LAUNCH SALES (GfK CHART-TRACK)")
    
    gx1, gy1, gx2, gy2 = 220, 150, 1920 - 220, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=GOLD, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=35, color=GOLD, width=2)
    
    draw.text((gx1 + 60, gy1 + 40), "FRANCHISE BRAND CONTAMINATION // UK WEEK 1 LAUNCH SALES", font=get_font(26, weight="bold"), fill=WHITE)
    draw.text((gx1 + 60, gy1 + 80), "COMPARATIVE IMPACT: AC UNITY (2014) VS. AC SYNDICATE (2015)", font=get_font(18, weight="medium"), fill=TEAL)
    
    base_y = gy2 - 140
    max_h = 420
    
    # Bar 1: AC Unity (100% baseline)
    b1_x = gx1 + 220
    b1_w = 260
    b1_h = int(max_h * min(progress * 1.2, 1.0))
    draw.rectangle([(b1_x, base_y - b1_h), (b1_x + b1_w, base_y)], fill=(138, 194, 187, 210), outline=TEAL, width=2)
    draw.text((b1_x + 35, base_y + 25), "AC UNITY (2014)", font=get_font(22, weight="bold"), fill=WHITE)
    draw.text((b1_x + 65, base_y - b1_h - 55), "100%", font=get_font(42, weight="bold"), fill=TEAL)
    draw.text((b1_x + 35, base_y - b1_h - 90), "BASELINE LAUNCH SALES", font=get_font(16, weight="medium"), fill=MUTED_GRAY)
    
    # Bar 2: AC Syndicate (-40.2%)
    b2_x = gx1 + 680
    b2_w = 260
    b2_h = int((max_h * 0.598) * min(progress * 1.2, 1.0))
    draw.rectangle([(b2_x, base_y - b2_h), (b2_x + b2_w, base_y)], fill=(230, 69, 83, 210), outline=CRIMSON, width=2)
    draw.text((b2_x + 20, base_y + 25), "AC SYNDICATE (2015)", font=get_font(22, weight="bold"), fill=WHITE)
    draw.text((b2_x + 50, base_y - b2_h - 55), "-40.2%", font=get_font(42, weight="bold"), fill=CRIMSON)
    draw.text((b2_x + 35, base_y - b2_h - 90), "CATASTROPHIC SLUMP", font=get_font(16, weight="bold"), fill=CRIMSON)
    
    # Right Side Market Summary
    sx = gx1 + 1040
    sy = gy1 + 180
    draw.rectangle([(sx, sy), (gx2 - 60, sy + 380)], fill=(20, 26, 30, 220), outline=GOLD, width=1)
    draw.text((sx + 30, sy + 30), "COMMERCIAL AFTERMATH:", font=get_font(20, weight="bold"), fill=GOLD)
    draw.text((sx + 30, sy + 75), "• Unity's technical reputation fatally poisoned Syndicate's launch.", font=get_font(16, weight="regular"), fill=OFF_WHITE)
    draw.text((sx + 30, sy + 120), "• Despite positive critical reviews, players refused to buy Day 1.", font=get_font(16, weight="regular"), fill=OFF_WHITE)
    draw.text((sx + 30, sy + 165), "• Forced Ubisoft to kill the annual release cycle.", font=get_font(16, weight="bold"), fill=CRIMSON)
    draw.text((sx + 30, sy + 210), "• Led to the 2-year reboot resulting in Assassin's Creed: Origins.", font=get_font(16, weight="regular"), fill=TEAL)
    
    return im.convert("RGB")

# ==============================================================================
# 8. CROWD DENSITY AI MAP (SHOT-016)
# ==============================================================================
def render_crowd_density_frame(progress=1.0):
    """Render Place de la Concorde 5,000 AI NPC crowd density radar."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc="01:15:00:00", shot_id="SHOT-016")
    draw_footer_bar(draw, "SIMULATION TELEMETRY // 5,000 INDEPENDENT AI AGENTS (PLACE DE LA CONCORDE)")
    
    gx1, gy1, gx2, gy2 = 180, 150, 1920 - 180, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=TEAL, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    draw.text((gx1 + 50, gy1 + 35), "AI CROWD DENSITY HEATMAP // 5,000 AUTONOMOUS AGENTS", font=get_font(26, weight="bold"), fill=WHITE)
    draw.text((gx1 + 50, gy1 + 75), "ANVILNEXT 2.0 MULTI-THREADED MORALE & BEHAVIOR TREE SIMULATION", font=get_font(18, weight="medium"), fill=TEAL)
    
    # Radar Circles
    rcx, rcy = gx1 + 500, gy1 + 450
    for rad in [100, 200, 300]:
        draw.ellipse([(rcx - rad, rcy - rad), (rcx + rad, rcy + rad)], outline=(138, 194, 187, 60), width=1)
        
    # Animated Radar Sweep Line
    angle = progress * 2.0 * math.pi
    sweep_x = rcx + int(300 * math.cos(angle))
    sweep_y = rcy + int(300 * math.sin(angle))
    draw.line([(rcx, rcy), (sweep_x, sweep_y)], fill=TEAL, width=2)
    
    # Right Side Telemetry Card
    tx = gx2 - 450
    draw.rectangle([(tx, gy1 + 180), (gx2 - 50, gy2 - 80)], fill=(20, 26, 30, 220), outline=GOLD, width=1)
    draw.text((tx + 30, gy1 + 220), "SIMULATION METRICS:", font=get_font(20, weight="bold"), fill=GOLD)
    draw.text((tx + 30, gy1 + 270), "TOTAL ACTIVE AGENTS: 5,000", font=get_font(17, weight="bold"), fill=WHITE)
    draw.text((tx + 30, gy1 + 310), "AI STATE: MASS RIOT / MORALE DISPATCH", font=get_font(16, weight="medium"), fill=TEAL)
    draw.text((tx + 30, gy1 + 350), "ANIMATION BLEND: 32 BONES PER NPC", font=get_font(16, weight="regular"), fill=OFF_WHITE)
    draw.text((tx + 30, gy1 + 390), "CPU OVERHEAD: 100% MULTI-CORE LOAD", font=get_font(16, weight="bold"), fill=CRIMSON)
    draw.text((tx + 30, gy1 + 430), "DRAW CALLS: > 50,000 PER FRAME", font=get_font(16, weight="bold"), fill=CRIMSON)
    
    return im.convert("RGB")

# ==============================================================================
# 9. CAROLINE MIOUSSE DEVELOPER DOSSIER (SHOT-020)
# ==============================================================================
def render_caroline_miousse_frame(progress=1.0):
    """Render Caroline Miousse 2-year Notre-Dame modeling dossier."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc="01:40:00:00", shot_id="SHOT-020")
    draw_footer_bar(draw, "HISTORICAL RECONSTRUCTION // SENIOR LEVEL ARTIST CAROLINE MIOUSSE — 2 YEARS ON NOTRE-DAME")
    
    gx1, gy1, gx2, gy2 = 200, 150, 1920 - 200, 930
    draw.rectangle([(gx1, gy1), (gx2, gy2)], fill=DARK_GLASS, outline=GOLD, width=1)
    draw_corner_brackets(draw, gx1, gy1, gx2, gy2, arm=30, color=GOLD, width=2)
    
    draw.text((gx1 + 50, gy1 + 35), "UBISOFT MONTREAL // LEAD ARCHITECTURAL RESEARCH DOSSIER", font=get_font(26, weight="bold"), fill=GOLD)
    draw.text((gx1 + 50, gy1 + 75), "CAROLINE MIOUSSE — SENIOR LEVEL ARTIST (2012 - 2014)", font=get_font(18, weight="medium"), fill=TEAL)
    
    # Left Card
    ax1, ay1 = gx1 + 50, gy1 + 130
    draw.rectangle([(ax1, ay1), (ax1 + 400, ay1 + 560)], fill=(20, 26, 30, 230), outline=TEAL, width=1)
    draw.rectangle([(ax1 + 30, ay1 + 30), (ax1 + 370, ay1 + 320)], fill=(12, 16, 18), outline=GOLD, width=1)
    draw.text((ax1 + 80, ay1 + 150), "PHOTO ARCHIVE", font=get_font(18, weight="medium"), fill=MUTED_GRAY)
    draw.text((ax1 + 50, ay1 + 360), "ROLE: LEAD CATHEDRAL MODELER", font=get_font(17, weight="bold"), fill=WHITE)
    draw.text((ax1 + 50, ay1 + 400), "EFFORT: 24 MONTHS FULL-TIME", font=get_font(17, weight="bold"), fill=GOLD)
    draw.text((ax1 + 50, ay1 + 440), "ACCURACY: BRICK-BY-BRICK 1:1", font=get_font(17, weight="medium"), fill=TEAL)
    
    # Right Content
    rx = ax1 + 440
    draw.text((rx, ay1 + 30), "RESEARCH & MODELING SPECIFICATIONS:", font=get_font(20, weight="bold"), fill=GOLD)
    
    specs = [
        "• Spent over 2 years consulting architectural historians and analyzing blueprints.",
        "• Reconstructed every stone block, flying buttress, and gargoyle in 1:1 metric scale.",
        "• Added the iconic 19th-century spire by Eugène Viollet-le-Duc for historical recognition.",
        "• Created a digital twin that became invaluable after the April 2019 Notre-Dame fire."
    ]
    sy = ay1 + 90
    for s in specs:
        draw.text((rx, sy), s, font=get_font(18, weight="regular"), fill=OFF_WHITE)
        sy += 55
        
    return im.convert("RGB")

# ==============================================================================
# 10. BASTILLE COPPERPLATE (SHOT-006)
# ==============================================================================
def render_bastille_frame(progress=1.0, shot_id="SHOT-006", edl_tc="00:00:30:00"):
    """Render historic Bastille 1789 archival presentation."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=80, alpha=20)
    
    draw_top_bar(draw, act_num="COLD OPEN", edl_tc=edl_tc, shot_id=shot_id)
    draw_footer_bar(draw, "ARCHIVAL COPPERPLATE ENGRAVING // STORMING OF THE BASTILLE — 14 JULY 1789")
    
    cx = 1920 // 2
    cy = 1080 // 2
    
    # Outer frame
    draw.rectangle([(280, 160), (1640, 920)], fill=DARK_GLASS, outline=GOLD, width=1)
    draw_corner_brackets(draw, 280, 160, 1640, 920, arm=30, color=GOLD, width=2)
    
    draw.text((320, 200), "HISTORICAL ARCHIVE // BIBLIOTHÈQUE NATIONALE DE FRANCE", font=get_font(22, weight="bold"), fill=GOLD)
    draw.text((320, 240), "PRISE DE LA BASTILLE (14 JUILLET 1789)", font=get_font(34, weight="bold"), fill=WHITE)
    draw.text((320, 300), "SYMBOLIC GENESIS OF THE FRENCH REVOLUTION AND THE PROMISE OF LIBERTY", font=get_font(18, weight="medium"), fill=TEAL)
    
    return im.convert("RGB")

# ==============================================================================
# 11. ANVILNEXT 2.0 PARIS 1:1 METRIC BLUEPRINT (SHOT-012, 013)
# ==============================================================================
def render_graphic_broll_blueprint(progress=1.0, shot_id="SHOT-012", edl_tc="01:00:00:00"):
    """Render AnvilNext 2.0 Paris 1:1 Metric Blueprint."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=60, alpha=25)
    
    draw_top_bar(draw, act_num="ACT I", edl_tc=edl_tc, shot_id=shot_id)
    draw_footer_bar(draw, "ENGINE ARCHITECTURE // ANVILNEXT 2.0 SEAMLESS VOLUMETRIC TRANSITIONS")
    
    cx = 1920 // 2
    cy = 1080 // 2 - 20
    
    # Center blueprint card
    draw.rectangle([(cx - 500, cy - 250), (cx + 500, cy + 250)], fill=DARK_GLASS, outline=TEAL, width=1)
    draw_corner_brackets(draw, cx - 500, cy - 250, cx + 500, cy + 250, arm=35, color=TEAL, width=2)
    
    draw.text((cx - 450, cy - 200), "ANVILNEXT 2.0 // TRUE 1:1 PARIS METRIC RECONSTRUCTION", font=get_font(26, weight="bold"), fill=WHITE)
    draw.text((cx - 450, cy - 150), "METRIC ACCURACY: 1.0 METER IN-GAME = 1.0 METER REAL-WORLD", font=get_font(18, weight="medium"), fill=GOLD)
    
    # Technical specs
    specs = [
        ("SEAMLESS INTERIORS", "1/4 OF ALL PARIS BUILDINGS FULLY EXPLORABLE"),
        ("LOADING SCREENS", "0.00 SECONDS (VOLUMETRIC STREAMING)"),
        ("NPC SIMULATION", "UP TO 5,000 INDEPENDENT CROWD AGENTS ON SCREEN")
    ]
    sy = cy - 70
    for lbl, val in specs:
        draw.text((cx - 450, sy), lbl, font=get_font(17, weight="bold"), fill=TEAL)
        draw.text((cx - 150, sy), val, font=get_font(17, weight="regular"), fill=OFF_WHITE)
        sy += 50
        
    return im.convert("RGB")

# ==============================================================================
# 12. OUTRO EPILOGUE CREDITS (SHOT-172)
# ==============================================================================
def render_outro_frame(progress=1.0):
    """Render Grand Outro and Epilogue Credits."""
    im = Image.new("RGBA", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(im, "RGBA")
    draw_subtle_grid(draw, cell_size=100, alpha=20)
    
    cx = 1920 // 2
    cy = 1080 // 2 - 30
    
    draw_top_bar(draw, act_num="EPILOGUE", edl_tc="15:00:00:00", shot_id="EPILOGUE")
    draw_footer_bar(draw, "LEMINO INVESTIGATION // PRODUCED IN 1080p 30.00 FPS")
    
    draw.text((cx - 300, cy - 80), "WRITTEN, DIRECTED & EDITED", font=get_font(18, weight="medium"), fill=TEAL)
    draw.text((cx - 300, cy - 40), "IN THE STYLE OF LEMiNO", font=get_font(42, weight="bold"), fill=WHITE)
    draw.text((cx - 300, cy + 30), "ASSASSIN'S CREED: UNITY // A DECADE LATER", font=get_font(20, weight="medium"), fill=GOLD)
    
    return im.convert("RGB")

# ==============================================================================
# CLIP RENDERER DISPATCHER
# ==============================================================================
def render_clip_to_mp4(frame_func, duration_sec, out_mp4, fps=30):
    """Render dynamic animated motion graphic sequence to an MP4 video clip."""
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
    """Strictly maps dedicated narrative motion graphics to explicit shot IDs."""
    sid = shot["id"].upper()
    dur = shot["duration"]
    s_tc = shot.get("start_tc", "00:00:00:00")
    
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
    if sid in ["SHOT-043", "SHOT-044", "SHOT-045"]:
        return render_clip_to_mp4(render_digital_foundry_frame, dur, out_path)
    if sid in ["SHOT-064", "SHOT-065", "SHOT-074", "SHOT-075"]:
        return render_clip_to_mp4(render_cpu_architecture_frame, dur, out_path)
    if sid in ["SHOT-087", "SHOT-088"]:
        return render_clip_to_mp4(render_archival_apology_frame, dur, out_path)
    if sid in ["SHOT-092", "SHOT-093", "SHOT-094"]:
        return render_clip_to_mp4(render_archival_free_game_frame, dur, out_path)
    if sid in ["SHOT-120", "SHOT-121"]:
        return render_clip_to_mp4(render_sales_comparison_frame, dur, out_path)
    if sid in ["SHOT-172"]:
        return render_clip_to_mp4(render_outro_frame, dur, out_path)
        
    # Act Chapter Cards
    if sid in ["SHOT-009", "SHOT-028", "SHOT-055", "SHOT-086", "SHOT-119", "SHOT-144"]:
        act_map = {
            "SHOT-009": ("ACT I", "THE 1:1 REVOLUTION", "PARIS 1789 — E3 2014 REVEAL"),
            "SHOT-028": ("ACT II", "THE NO-FACE NIGHTMARE", "NOVEMBER 11, 2014 — THE GLITCHES BEGIN"),
            "SHOT-055": ("ACT III", "FORENSIC CODE BREAKDOWN", "DIRECTX 11 & AMD JAGUAR SILICON LIMITS"),
            "SHOT-086": ("ACT IV", "THE APOLOGY & CONCESSIONS", "YANNIS MALLAT LETTER & FREE DEAD KINGS"),
            "SHOT-119": ("ACT V", "DEATH OF THE ANNUAL MACHINE", "THE SYNDICATE COLLAPSE & THE HIATUS"),
            "SHOT-144": ("ACT VI", "THE ASHES OF NOTRE-DAME", "APRIL 15, 2019 — DIGITAL IMMORTALITY")
        }
        act_num, title, sub = act_map.get(sid, ("INVESTIGATION", "CASE DOSSIER", "PARIS ARCHIVE"))
        return render_clip_to_mp4(lambda p: render_chapter_frame(act_num, title, sub, p), dur, out_path)

    return None
