---
name: lemino-documentary
description: >-
  Standard operating procedure and scaffolding generator for creating broadcast-grade
  LEMiNO-style investigative documentary video episodes with HyperFrames.
---

# LEMiNO Documentary Skill

Use this skill whenever creating new episodes, acts, or compositions following the LEMiNO investigative documentary style.

## Scaffolding Tool
Run the template CLI generator located at `templates/lemino-episode-template/scaffold_episode.py`:
```bash
python3 "templates/lemino-episode-template/scaffold_episode.py" --help
```

## Available Color Themes
Defined in `templates/lemino-episode-template/themes.json`:
- `charcoal_teal` (Default LEMiNO: Deep Charcoal #121719, Turquoise #8ac2bb, Warm Gold #d5a764)
- `sepia_noir` (Vintage Archive: Rich Umber #16120e, Muted Cream #ece4d4, Sepia #c59b6d)
- `deep_navy` (Military / Gov Cold: Midnight #0b111a, Electric Cyan #56c2d6, Silver #d6e2e8)
- `crimson_cyber` (High Threat / Cyber: Obsidian #140b0e, Crimson #e64553, Alert Amber #f5a97f)
- `monochrome_hud` (Clean Minimalist: Pitch #0e0e10, Bright White #ffffff, Ice Gray #a6adc8)

## Pipeline Commands
1. **Check Compositions:** `npx hyperframes check`
2. **Render Master:** `TMPDIR=/home/keng/.tmp npm run render`
3. **Stitch Episode:** `python3 templates/lemino-episode-template/stitch_episode.py`
4. **Upload to Cloud:** `python3 templates/lemino-episode-template/upload_to_gdrive.py`
