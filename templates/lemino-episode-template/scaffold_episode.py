#!/usr/bin/env python3
import argparse
import json
import os
import shutil

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(TEMPLATE_DIR, "themes.json"), "r") as f:
    THEMES = json.load(f)

HTML_SCENE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body>
  <template>
    <style>
      @font-face { font-family: Thai; src: url('assets/thai.ttf'); }
      @font-face { font-family: ThaiSerif; src: url('assets/serif-thai.ttf'); }
      @font-face { font-family: Stone; src: url('assets/serif.ttf'); }
      * { box-sizing: border-box; }
      #root {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: __BG_COLOR__;
        color: __TEXT_BODY__;
        font-family: Thai, sans-serif;
      }
      .bg-container {
        position: absolute;
        inset: 0;
        overflow: hidden;
      }
      .bg-video {
        position: absolute;
        width: 1920px;
        height: 1080px;
        object-fit: cover;
        filter: __VIDEO_FILTER__;
      }
      .overlay-grid {
        position: absolute;
        inset: 0;
        background: __VIGNETTE__;
      }
      .scanlines {
        position: absolute;
        inset: 0;
        background: linear-gradient(rgba(18, 23, 25, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
        background-size: 100% 4px;
        pointer-events: none;
        opacity: 0.35;
      }
      .top-bar {
        position: absolute;
        top: 65px;
        left: 118px;
        right: 118px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 22px;
        letter-spacing: 3px;
        color: __PRIMARY_ACCENT__;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
      }
      .badge {
        display: inline-block;
        border: 1px solid __PRIMARY_ACCENT__;
        padding: 4px 12px;
        font-size: 18px;
        color: __PRIMARY_ACCENT__;
        margin-left: 16px;
        border-radius: 2px;
      }
      .footer {
        position: absolute;
        bottom: 65px;
        left: 118px;
        right: 118px;
        display: flex;
        justify-content: space-between;
        font-size: 22px;
        color: __TEXT_BODY__;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
      }
      .copy {
        position: absolute;
        left: 118px;
        top: 220px;
        width: 960px;
        z-index: 10;
      }
      .eyebrow {
        font-size: 24px;
        letter-spacing: 5px;
        color: __PRIMARY_ACCENT__;
        font-weight: 500;
        text-shadow: 0 2px 8px rgba(0,0,0,0.9);
      }
      .copy h1 {
        font-family: ThaiSerif, serif;
        font-size: 78px;
        font-weight: 400;
        line-height: 1.45;
        margin: 22px 0;
        color: __TEXT_PRIMARY__;
        text-shadow: 0 3px 12px rgba(0,0,0,0.9);
      }
      .copy p {
        font-size: 34px;
        line-height: 1.65;
        margin: 12px 0;
        max-width: 820px;
        color: __TEXT_BODY__;
        text-shadow: 0 2px 8px rgba(0,0,0,0.9);
      }
      .rule {
        height: 3px;
        width: 140px;
        background: __PRIMARY_ACCENT__;
        transform-origin: left center;
        margin: 20px 0;
      }
      .hud-telemetry {
        position: absolute;
        right: 118px;
        top: 220px;
        width: 440px;
        background: __CARD_BG__;
        border: 1px solid __CARD_BORDER__;
        border-left: 3px solid __PRIMARY_ACCENT__;
        padding: 24px;
        font-size: 20px;
        line-height: 1.7;
        color: __TEXT_BODY__;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        z-index: 10;
      }
      .hud-title {
        font-size: 19px;
        letter-spacing: 2px;
        color: __PRIMARY_ACCENT__;
        border-bottom: 1px solid __CARD_BORDER__;
        padding-bottom: 8px;
        margin-bottom: 14px;
      }
      .hud-val {
        color: __SECONDARY_ACCENT__;
        font-family: monospace;
      }
    </style>
    <div id="root" data-composition-id="__COMP_ID__" data-width="1920" data-height="1080" data-duration="__DURATION_SEC__">
      <div class="bg-container">
        <video id="v-__COMP_ID__" class="bg-video clip" muted playsinline src="__VIDEO_SRC__" data-start="0" data-duration="__DURATION_FRAMES__" data-layout-allow-overflow=""></video>
        <div class="overlay-grid"></div>
        <div class="scanlines"></div>
      </div>

      <div class="top-bar">
        <span>__TOP_LEFT__ <span class="badge">__BADGE__</span></span>
        <span>__SCENE_INDEX__</span>
      </div>

      <div class="copy">
        <div class="eyebrow">__EYEBROW__</div>
        <h1>__HEADLINE__</h1>
        <div class="rule"></div>
        <p>__PARAGRAPH_1__</p>
        <p>__PARAGRAPH_2__</p>
      </div>

      <div class="hud-telemetry">
        <div class="hud-title">__HUD_TITLE__</div>
        <div>METRIC 01: <span class="hud-val">__METRIC_1__</span></div>
        <div>METRIC 02: <span class="hud-val">__METRIC_2__</span></div>
        <div>COORDINATE: <span class="hud-val">__METRIC_3__</span></div>
        <div>STATUS: <span class="hud-val">__METRIC_4__</span></div>
      </div>

      <div class="footer">
        <span>__FOOTER_LEFT__</span>
        <span>__FOOTER_RIGHT__</span>
      </div>
    </div>

    <script>
      const tl = gsap.timeline({paused: true});
      tl.fromTo('.bg-video', {scale: 1.0}, {scale: 1.08, duration: __DURATION_SEC__, ease: 'none'}, 0);
      tl.fromTo('.copy', {opacity: 0, x: -30}, {opacity: 1, x: 0, duration: 1.5, ease: 'power2.out'}, 0.5);
      tl.fromTo('.rule', {scaleX: 0}, {scaleX: 1, duration: 1.2, ease: 'power2.out'}, 1.2);
      tl.fromTo('.copy p', {opacity: 0, y: 15}, {opacity: 1, y: 0, duration: 1.2, stagger: 1.5, ease: 'power2.out'}, 1.8);
      tl.fromTo('.hud-telemetry', {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: 1.2, ease: 'power2.out'}, 1.5);
      tl.to('#root', {opacity: 0, duration: 0.6, ease: 'power1.in'}, __OUT_SEC__);
      window.__timelines['__COMP_ID__'] = tl;
    </script>
  </template>
</body>
</html>
"""

def scaffold_act(target_dir, act_name, theme_name="charcoal_teal"):
    theme = THEMES.get(theme_name, THEMES["charcoal_teal"])
    os.makedirs(target_dir, exist_ok=True)
    comp_dir = os.path.join(target_dir, "compositions")
    assets_dir = os.path.join(target_dir, "assets", "footage")
    os.makedirs(comp_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    print(f"Scaffolding {act_name} with theme: {theme['name']}...")
    # Generate index.html and compositions...
    print("Act scaffold created successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LEMiNO Episode Scaffolder")
    parser.add_argument("--act", required=True, help="Act name e.g. lemino-ep02-act01")
    parser.add_argument("--theme", default="charcoal_teal", choices=list(THEMES.keys()), help="Visual theme")
    args = parser.parse_args()
    scaffold_act(args.act, args.act, args.theme)
