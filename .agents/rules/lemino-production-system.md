# LEMiNO Documentary Production System Rule

This project follows the broadcast-grade investigative documentary production standard inspired by LEMiNO.

## 1. Episode Architecture
- **Standard Resolution:** 1920x1080 (1080p Full HD) @ 30.00 fps.
- **Engine:** HyperFrames (`npx hyperframes@0.8.62`).
- **Standard Episode Breakdown:**
  - `Opening Sequence` (75s | 5 scenes @ 14-16s each): Cold open hook with footage, high-level map/dossier, vertical anomaly, central question, and grand title card.
  - `ACT I` to `ACT VI` (120s each | 5 scenes @ 20-25s each): Chronological investigative narrative progression.
  - Total Episode Runtime: ~13:15 (795 seconds / 23,850 frames).

## 2. Visual Aesthetic & Theme System
All scenes use a modular color theme system defined in `templates/lemino-episode-template/themes.json`:
- **Default Charcoal Teal (Canonical LEMiNO):**
  - Background Canvas: `#121719` (Deep Charcoal)
  - Primary Accent: `#8ac2bb` (LEMiNO Turquoise / Cyan)
  - Secondary Accent: `#d5a764` (Warm Desert Gold / Amber)
  - Primary Typography: `#ffffff` / `#eee6d3` (Stone Off-White)
  - HUD Panel Background: `rgba(18, 23, 25, 0.85)` with `1px solid rgba(138, 194, 187, 0.35)`
- **Visual Layers (Strict Order from back to front):**
  1. `<video class="bg-video">` (Cinematic footage, filtered with contrast, slight desaturation, sepia tint)
  2. `.overlay-grid` (Radial vignette `radial-gradient(circle, rgba(18,23,25,0.4) 0%, rgba(18,23,25,0.92) 85%)`)
  3. `.scanlines` (Subtle 4px video scanlines at 0.35 opacity)
  4. `.top-bar` & `.footer` (Archival classification tags, episode beats, timecodes)
  5. `.copy` (Headline, accent rule line, body paragraphs with ThaiSerif/Thai fonts)
  6. `.hud-telemetry` (Floating forensic HUD telemetry box, coordinates, status indicators)

## 3. Strict Quality Standards
- **100% WCAG AA Contrast Compliance:** Every text element must exceed 4.5:1 (normal text) and 3.0:1 (large text/headers). Always use drop-shadows or dark translucent backplates.
- **Zero Content Overlap:** Never place floating text over another text container without `data-layout-allow-overlap=""` and `aria-hidden="true"`.
- **Pre-flight Validation:** Always execute `npx hyperframes check` before launching any render.

## 4. Production Pipeline
1. **Footage Preparation:** Cut raw video into 1080p 30fps clips using `ffmpeg -preset ultrafast -threads 4`.
2. **Composition Authoring:** Generate HTML compositions via script using the template.
3. **Quality Check:** Run `npx hyperframes check` (GPU hardware probe).
4. **Master Render:** Execute `TMPDIR=/home/keng/.tmp npm run render` inside the act directory.
5. **Episode Assembly:** Concat all acts via `ffmpeg -f concat -c copy`.
6. **Cloud Delivery:** Upload master and individual acts to Google Drive `Vids Exports/` via `rclone`.
