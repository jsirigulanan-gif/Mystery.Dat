# LEMiNO Investigative Documentary Production System

Broadcast-grade automated documentary production system inspired by LEMiNO, powered by HyperFrames and GitHub Actions.

## 📺 Completed Episodes:
- **Episode 01:** *Shadow of the Colossus: The 7-Year Quest for the 17th Colossus & The Secret Garden (2005–2018)*
  - **Runtime:** 13:15 (795s / 23,850 frames @ 1080p 30fps)
  - **Google Drive Master Video:** [Open in Google Drive](https://drive.google.com/open?id=1OLQFyeBoOacyf0-1BQ4SbdvVEDGHPzqj)

## 🚀 Cloud Automation:
This repository includes a GitHub Actions workflow (`.github/workflows/lemino_producer.yml`) configured to:
1. Run on a 6-hour recurring schedule (`cron: '0 */6 * * *'`)
2. Pull pending docx scripts from Google Drive queue
3. Check WCAG AA contrast (100% compliance) & render 1080p 30fps video
4. Upload master renders to Google Drive (`Vids Exports/`)
5. Email finished video link to `jakkarin.sirigulanan@gmail.com`

## 🎨 Modular Theme System
Configured in `templates/lemino-episode-template/themes.json`:
- `charcoal_teal` (Canonical LEMiNO)
- `alien_industrial` (Weyland-Yutani Acid Green)
- `sepia_noir` (Archival Vintage)
- `deep_navy` (Cold War Dossier)
- `crimson_cyber` (Cyber / Threat Alert)
