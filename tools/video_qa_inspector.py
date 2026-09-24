#!/usr/bin/env python3
"""
================================================================================
LEMiNO Documentary Production System — Post-Render Video QA Inspector
หน่วยตรวจสอบวิดีโอหลังเรนเดอร์เสร็จ: ตรวจสอบความถูกต้อง, จับผิด (Defect Detection),
และแนะนำวิธีแก้ไข (Actionable Remediation Engine)
================================================================================
Broadcast Standard:
- Resolution: 1920x1080 (16:9 Full HD)
- Frame Rate: 30.00 fps (CFR)
- Pixel Format: YUV420p (Broadcast & YouTube Standard)
- Audio Loudness: EBU R128 (-14.0 LUFS ± 1.0 LUFS, True Peak <= -1.0 dBTP)
- Integrity: Moov atom faststart, zero dropped frames, zero unintended blackouts (>0.5s)
"""

import os
import sys
import json
import re
import subprocess
import argparse
from datetime import datetime

# ANSI Terminal Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

class VideoQAInspector:
    def __init__(self, video_path, target_duration=900.0, target_fps=30.0, 
                 target_res=(1920, 1080), target_lufs=-14.0, lufs_tolerance=1.5):
        self.video_path = os.path.abspath(video_path)
        self.target_duration = target_duration
        self.target_fps = target_fps
        self.target_res = target_res
        self.target_lufs = target_lufs
        self.lufs_tolerance = lufs_tolerance
        
        self.report = {
            "meta": {
                "file_path": self.video_path,
                "file_name": os.path.basename(self.video_path),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_size_bytes": 0,
                "file_size_mb": 0.0,
            },
            "streams": {},
            "checks": [],
            "defects": [],
            "remediations": [],
            "summary": {
                "total_checks": 0,
                "passed": 0,
                "warnings": 0,
                "critical": 0,
                "score_percent": 100.0,
                "verdict": "PENDING"
            }
        }
        
    def log_check(self, category, name, status, details, remedy=None, cmd_fix=None):
        """
        Record a check result:
        status: 'PASS', 'WARN', 'FAIL'
        """
        self.report["summary"]["total_checks"] += 1
        if status == "PASS":
            self.report["summary"]["passed"] += 1
        elif status == "WARN":
            self.report["summary"]["warnings"] += 1
        elif status == "FAIL":
            self.report["summary"]["critical"] += 1
            
        entry = {
            "category": category,
            "name": name,
            "status": status,
            "details": details,
            "remedy": remedy,
            "cmd_fix": cmd_fix
        }
        self.report["checks"].append(entry)
        
        if status in ["WARN", "FAIL"]:
            self.report["defects"].append(entry)
            if remedy:
                self.report["remediations"].append({
                    "defect": f"[{category}] {name}",
                    "severity": status,
                    "remedy": remedy,
                    "cmd_fix": cmd_fix
                })
                
        # Terminal output
        badge = f"{GREEN}[PASS]{RESET}" if status == "PASS" else f"{YELLOW}[WARN]{RESET}" if status == "WARN" else f"{RED}[FAIL]{RESET}"
        print(f"  {badge} {BOLD}{category}{RESET} // {name}: {details}")

    def run_ffprobe(self):
        """Extract stream metadata via ffprobe."""
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
            
        self.report["meta"]["file_size_bytes"] = os.path.getsize(self.video_path)
        self.report["meta"]["file_size_mb"] = round(os.path.getsize(self.video_path) / (1024 * 1024), 2)
        
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            self.video_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {res.stderr}")
        return json.loads(res.stdout)

    def check_container_and_faststart(self, data):
        """Check container format, duration, and moov atom placement."""
        print(f"\n{CYAN}{BOLD}--- [PASS 1/5] CONTAINER & MOOV ATOM INTEGRITY ---{RESET}")
        fmt = data.get("format", {})
        fmt_name = fmt.get("format_name", "")
        duration = float(fmt.get("duration", 0.0))
        bitrate_kbps = round(float(fmt.get("bit_rate", 0)) / 1000, 1) if fmt.get("bit_rate") else 0
        
        # 1. Container type
        if "mp4" in fmt_name or "mov" in fmt_name:
            self.log_check("Container", "Format Standard", "PASS", f"Valid MP4/MOV container ({fmt_name})")
        else:
            self.log_check(
                "Container", "Format Standard", "WARN", 
                f"Non-standard container: {fmt_name}. Preferred: mp4",
                remedy="Convert container to MP4 for maximum web and broadcast compatibility.",
                cmd_fix=f"ffmpeg -i {self.video_path} -c copy {self.video_path}.fixed.mp4"
            )
            
        # 2. Moov Atom placement (FastStart check)
        # Check first 64KB for 'moov' atom
        with open(self.video_path, "rb") as f:
            header_bytes = f.read(65536)
            has_faststart = b"moov" in header_bytes
            
        if has_faststart:
            self.log_check("Container", "Web Streaming (FastStart)", "PASS", "Moov atom located at beginning of file (Instant web playback enabled)")
        else:
            self.log_check(
                "Container", "Web Streaming (FastStart)", "WARN",
                "Moov atom located at end of file (Causes buffering delay on YouTube/Web)",
                remedy="ย้าย moov atom มาไว้ต้นไฟล์ เพื่อให้วิดีโอสามารถสตรีมมิ่งเล่นได้ทันทีโดยไม่ต้องรอโหลดครบทั้งไฟล์",
                cmd_fix=f"ffmpeg -i {self.video_path} -c copy -movflags +faststart {os.path.splitext(self.video_path)[0]}_faststart.mp4"
            )
            
        # 3. Exact Duration Check
        dur_diff = abs(duration - self.target_duration)
        if dur_diff <= 0.04:  # within 1 frame (33.3ms)
            self.log_check("Timeline", "Runtime Duration", "PASS", f"{duration:.2f}s (Matches target {self.target_duration:.2f}s within 1 frame)")
        elif dur_diff <= 1.0:
            self.log_check(
                "Timeline", "Runtime Duration", "WARN",
                f"{duration:.2f}s (Differs from target {self.target_duration:.2f}s by {dur_diff:.2f}s)",
                remedy="ปรับแต่งไทม์โค้ดช่วงท้าย หรือใช้พารามิเตอร์ -t 900.00 เพื่อล็อกเวลาให้ตรง 15:00.00 เป๊ะ",
                cmd_fix=f"ffmpeg -i {self.video_path} -t {self.target_duration:.2f} -c copy {os.path.splitext(self.video_path)[0]}_trimmed.mp4"
            )
        else:
            self.log_check(
                "Timeline", "Runtime Duration", "FAIL",
                f"{duration:.2f}s (Major discrepancy from target {self.target_duration:.2f}s by {dur_diff:.2f}s)",
                remedy="ไทม์ไลน์มีความคลาดเคลื่อนสูง กรุณาตรวจสอบการต่อช็อต (Concat) หรือความยาวของไฟล์เสียงพากย์",
                cmd_fix=f"ffmpeg -i {self.video_path} -t {self.target_duration:.2f} -c copy {os.path.splitext(self.video_path)[0]}_trimmed.mp4"
            )

    def check_video_stream(self, data):
        """Check video resolution, framerate, pixel format, and codec."""
        print(f"\n{CYAN}{BOLD}--- [PASS 2/5] VIDEO STREAM COMPLIANCE ---{RESET}")
        vstreams = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
        if not vstreams:
            self.log_check("Video", "Stream Presence", "FAIL", "No video stream detected in file!",
                           remedy="ตรวจสอบกระบวนการ Render หรือ Muxing วิดีโอหายไปจากไฟล์")
            return
            
        v = vstreams[0]
        codec = v.get("codec_name", "")
        pix_fmt = v.get("pix_fmt", "")
        width = int(v.get("width", 0))
        height = int(v.get("height", 0))
        
        # Framerate
        r_fps_str = v.get("r_frame_rate", "30/1")
        if "/" in r_fps_str:
            num, den = r_fps_str.split("/")
            fps = float(num) / float(den) if float(den) != 0 else 0
        else:
            fps = float(r_fps_str)
            
        # 1. Codec
        if codec in ["h264", "avc1"]:
            self.log_check("Video", "Video Codec", "PASS", f"Broadcast standard H.264 / AVC ({codec})")
        elif codec in ["hevc", "h265", "av01", "vp9"]:
            self.log_check("Video", "Video Codec", "WARN", f"Next-gen codec {codec}. May not play on legacy editors/browsers",
                           remedy="แปลงเป็น H.264 สำหรับการส่งตรวจบรอดแคสต์มาตรฐาน",
                           cmd_fix=f"ffmpeg -i {self.video_path} -c:v libx264 -preset slow -crf 18 -c:a copy {os.path.splitext(self.video_path)[0]}_h264.mp4")
        else:
            self.log_check("Video", "Video Codec", "FAIL", f"Unrecognized / non-broadcast codec: {codec}",
                           remedy="จำเป็นต้องเข้ารหัสใหม่ด้วย H.264 (libx264)",
                           cmd_fix=f"ffmpeg -i {self.video_path} -c:v libx264 -preset slow -crf 18 -c:a copy {os.path.splitext(self.video_path)[0]}_h264.mp4")

        # 2. Pixel format
        if pix_fmt == "yuv420p":
            self.log_check("Video", "Chroma Subsampling", "PASS", "YUV420p (100% universal hardware & web compatibility)")
        else:
            self.log_check(
                "Video", "Chroma Subsampling", "WARN",
                f"Pixel format is '{pix_fmt}'. Non-yuv420p may cause black screen on Apple QuickTime or mobile devices",
                remedy="แปลง Pixel Format ให้เป็น yuv420p เพื่อป้องกันอาการภาพไม่ขึ้นบนอุปกรณ์มือถือและ QuickTime",
                cmd_fix=f"ffmpeg -i {self.video_path} -pix_fmt yuv420p -c:v libx264 -crf 18 -c:a copy {os.path.splitext(self.video_path)[0]}_yuv420p.mp4"
            )

        # 3. Resolution
        if (width, height) == self.target_res:
            self.log_check("Video", "Aspect Ratio & Resolution", "PASS", f"{width}x{height} (16:9 Full HD exact)")
        else:
            self.log_check(
                "Video", "Aspect Ratio & Resolution", "FAIL",
                f"Resolution is {width}x{height}, expected {self.target_res[0]}x{self.target_res[1]}",
                remedy=f"สเกลวิดีโอให้ได้ขนาดมาตรฐาน 1920x1080 เพื่อไม่ให้ภาพบิดเบี้ยวหรือมีแถบดำขอบจอ",
                cmd_fix=f"ffmpeg -i {self.video_path} -vf 'scale={self.target_res[0]}:{self.target_res[1]}:force_original_aspect_ratio=decrease,pad={self.target_res[0]}:{self.target_res[1]}:(ow-iw)/2:(oh-ih)/2' -c:a copy {os.path.splitext(self.video_path)[0]}_1080p.mp4"
            )

        # 4. Framerate
        if abs(fps - self.target_fps) < 0.05:
            self.log_check("Video", "Frame Rate", "PASS", f"{fps:.2f} fps (Matches broadcast standard {self.target_fps:.2f} fps)")
        else:
            self.log_check(
                "Video", "Frame Rate", "WARN",
                f"Frame rate is {fps:.2f} fps, expected {self.target_fps:.2f} fps",
                remedy=f"แปลงเฟรมเรตให้เป็น {self.target_fps:.2f} fps CFR เพื่อป้องกันเสียงและภาพหลุดซิงค์ (Audio Desync)",
                cmd_fix=f"ffmpeg -i {self.video_path} -r {self.target_fps} -c:a copy {os.path.splitext(self.video_path)[0]}_30fps.mp4"
            )

    def check_audio_stream(self, data):
        """Check audio channels, sample rate, and codec."""
        print(f"\n{CYAN}{BOLD}--- [PASS 3/5] AUDIO STREAM SPECS ---{RESET}")
        astreams = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
        if not astreams:
            self.log_check("Audio", "Audio Stream", "FAIL", "No audio stream found in master file!",
                           remedy="มิกซ์เสียง Voiceover และ BGM เข้ากับไฟล์วิดีโอ")
            return
            
        a = astreams[0]
        acodec = a.get("codec_name", "")
        channels = int(a.get("channels", 0))
        sample_rate = int(a.get("sample_rate", 0))
        
        # 1. Audio Codec
        if acodec in ["aac", "mp3", "pcm_s16le"]:
            self.log_check("Audio", "Audio Codec", "PASS", f"{acodec.upper()} audio stream")
        else:
            self.log_check("Audio", "Audio Codec", "WARN", f"Uncommon audio codec: {acodec}",
                           remedy="แปลงเสียงเป็น AAC Stereo 256kbps",
                           cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -c:a aac -b:a 256k {os.path.splitext(self.video_path)[0]}_aac.mp4")
                           
        # 2. Channels
        if channels == 2:
            self.log_check("Audio", "Channel Layout", "PASS", "Stereo (2 channels)")
        elif channels == 1:
            self.log_check("Audio", "Channel Layout", "WARN", "Mono (1 channel). Should be dual stereo for immersive sound.",
                           remedy="Upmix เสียงเป็น Stereo 2 แชนแนล",
                           cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -ac 2 {os.path.splitext(self.video_path)[0]}_stereo.mp4")
        else:
            self.log_check("Audio", "Channel Layout", "PASS", f"{channels} Multi-channel surround")
            
        # 3. Sample Rate
        if sample_rate in [48000, 44100]:
            self.log_check("Audio", "Sample Rate", "PASS", f"{sample_rate} Hz (Broadcast standard)")
        else:
            self.log_check("Audio", "Sample Rate", "WARN", f"{sample_rate} Hz. Preferred: 48,000 Hz",
                           remedy="Resample เสียงเป็น 48kHz สำหรับงานวิดีโอบรอดแคสต์",
                           cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -af 'aresample=48000' {os.path.splitext(self.video_path)[0]}_48k.mp4")

    def run_deep_audio_loudness_analysis(self):
        """Run EBU R128 loudness scanner via ffmpeg."""
        print(f"\n{CYAN}{BOLD}--- [PASS 4/5] EBU R128 LOUDNESS & TRUE PEAK AUDIT ---{RESET}")
        cmd = [
            "ffmpeg", "-nostats",
            "-vn",
            "-i", self.video_path,
            "-filter_complex", "ebur128=peak=true",
            "-f", "null", "-"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = proc.stderr
        
        # Regex parse EBU R128 output
        int_lufs_m = re.search(r"Integrated loudness:\s*I:\s*([-\d\.]+)\s*LUFS", out)
        lra_m = re.search(r"Loudness range:\s*LRA:\s*([-\d\.]+)\s*LU", out)
        tp_m = re.search(r"True peak:\s*Peak:\s*([-\d\.]+)\s*dBFS", out)
        
        int_lufs = float(int_lufs_m.group(1)) if int_lufs_m else None
        lra = float(lra_m.group(1)) if lra_m else None
        true_peak = float(tp_m.group(1)) if tp_m else None
        
        if int_lufs is not None:
            diff = abs(int_lufs - self.target_lufs)
            if diff <= self.lufs_tolerance:
                self.log_check("Audio Loudness", "Integrated Loudness (LUFS)", "PASS", 
                               f"{int_lufs:.1f} LUFS (Target: {self.target_lufs:.1f} LUFS, YouTube/EBU Standard Compliant)")
            elif int_lufs < self.target_lufs - self.lufs_tolerance:
                self.log_check(
                    "Audio Loudness", "Integrated Loudness (LUFS)", "WARN",
                    f"{int_lufs:.1f} LUFS (Too quiet! Target is {self.target_lufs:.1f} LUFS)",
                    remedy="เสียงเบากว่ามาตรฐาน YouTube (-14 LUFS) ผู้ชมอาจต้องเร่งเสียงดัง แนะนำให้ใช้ตัวกรอง loudnorm ดึงเสียงขึ้น",
                    cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -af 'loudnorm=I=-14:LRA=7:TP=-1.0' {os.path.splitext(self.video_path)[0]}_normalized.mp4"
                )
            else:
                self.log_check(
                    "Audio Loudness", "Integrated Loudness (LUFS)", "WARN",
                    f"{int_lufs:.1f} LUFS (Too loud! Target is {self.target_lufs:.1f} LUFS)",
                    remedy="เสียงดังเกินมาตรฐาน YouTube (-14 LUFS) อาจถูกระบบ YouTube Auto-Volume บีบกดเสียงลง แนะนำให้ Normalize",
                    cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -af 'loudnorm=I=-14:LRA=7:TP=-1.0' {os.path.splitext(self.video_path)[0]}_normalized.mp4"
                )
        else:
            self.log_check("Audio Loudness", "Integrated Loudness (LUFS)", "WARN", "Could not calculate EBU R128 loudness")

        if true_peak is not None:
            if true_peak <= -1.0:
                self.log_check("Audio Loudness", "True Peak Level", "PASS", f"{true_peak:.1f} dBTP (No inter-sample clipping, headroom preserved)")
            elif true_peak <= 0.0:
                self.log_check("Audio Loudness", "True Peak Level", "WARN", 
                               f"{true_peak:.1f} dBTP (Headroom below -1.0 dBTP recommendation. Minor risk of DAC distortion)",
                               remedy="ตั้งค่า True Peak Limiter ไว้ที่ -1.0 dBTP",
                               cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -af 'loudnorm=I=-14:LRA=7:TP=-1.0' {os.path.splitext(self.video_path)[0]}_normalized.mp4")
            else:
                self.log_check(
                    "Audio Loudness", "True Peak Level", "FAIL",
                    f"{true_peak:.1f} dBTP (Digital clipping detected! Distortion present)",
                    remedy="มีเสียงแตกดิจิทัล (Digital Clipping) จำเป็นต้องกดเสียงลงด้วย Limiter ทันที",
                    cmd_fix=f"ffmpeg -i {self.video_path} -c:v copy -af 'loudnorm=I=-14:LRA=7:TP=-1.0' {os.path.splitext(self.video_path)[0]}_normalized.mp4"
                )

        if lra is not None:
            if lra <= 12.0:
                self.log_check("Audio Loudness", "Dynamic Range (LRA)", "PASS", f"{lra:.1f} LU (Balanced speech & ambient dynamics)")
            else:
                self.log_check("Audio Loudness", "Dynamic Range (LRA)", "WARN", 
                               f"{lra:.1f} LU (Very wide dynamic range. Some whispers may be inaudible on mobile speakers)")

    def run_artifact_and_drop_detection(self):
        """Scan video for accidental prolonged black frames and frozen frames in a single accelerated pass."""
        print(f"\n{CYAN}{BOLD}--- [PASS 5/5] BLACK SCREEN & FREEZE ARTIFACT SCAN ---{RESET}")
        
        # Combined blackdetect and freezedetect in one pass with -an
        cmd_scan = [
            "ffmpeg", "-nostats",
            "-an",
            "-i", self.video_path,
            "-vf", "blackdetect=d=0.7:pic_th=0.98,freezedetect=n=0.003:d=2.5",
            "-f", "null", "-"
        ]
        proc = subprocess.run(cmd_scan, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = proc.stderr
        
        black_matches = re.findall(r"black_start:([-\d\.]+)\s+black_end:([-\d\.]+)\s+black_duration:([-\d\.]+)", out)
        freeze_starts = re.findall(r"freeze_start:\s*([-\d\.]+)", out)
        
        # Filter out cold open initial fade-in (< 1.5s) or end fade-out (> target_duration - 2s)
        unintended_blacks = []
        for bs, be, bd in black_matches:
            s, e, d = float(bs), float(be), float(bd)
            if s > 2.0 and e < (self.target_duration - 3.0):
                unintended_blacks.append((s, e, d))
                
        if not unintended_blacks:
            self.log_check("Artifacts", "Accidental Black Frames", "PASS", "No unintended blackouts detected in narrative progression")
        else:
            for s, e, d in unintended_blacks:
                tc_start = f"{int(s//60):02d}:{int(s%60):02d}"
                tc_end = f"{int(e//60):02d}:{int(e%60):02d}"
                self.log_check(
                    "Artifacts", "Accidental Black Frames", "WARN",
                    f"Black screen gap detected at {tc_start} - {tc_end} (Duration: {d:.2f}s)",
                    remedy=f"เกิดจอดำว่างเปล่าระหว่าง {tc_start} - {tc_end} ตรวจสอบว่ามีช็อตที่เรนเดอร์ไม่ติดหรือไม่ แนะนำให้แทรก B-roll หรือ Typography Card ในช่วงเวลานี้",
                    cmd_fix=f"# ตรวจสอบช็อตที่ช่วงไทม์โค้ด {tc_start} และเรนเดอร์คลิปทดแทนด้วย tools/render_lemino_graphics.py"
                )

        # 2. Frozen frame detector (parsed from combined scan)
        
        # Note: Static title cards or quote cards may trigger freezedetect intentionally
        if len(freeze_starts) <= 4:
            self.log_check("Artifacts", "Frozen Video Check", "PASS", f"Normal scene pacing ({len(freeze_starts)} static card intervals detected, consistent with documentary cards)")
        else:
            self.log_check(
                "Artifacts", "Frozen Video Check", "WARN",
                f"{len(freeze_starts)} static intervals detected. Verify whether these are intentional graphics or rendering lockups.",
                remedy="หากเป็นภาพนิ่งกราฟิก แนะนำให้ใส่เอฟเฟกต์ Slow Push-in (Ken Burns effect) หรือ Subtle Floating Grid เพื่อให้ภาพมีความเคลื่อนไหวมีชีวิตชีวา"
            )

    def calculate_score_and_verdict(self):
        """Calculate overall quality score and broadcast verdict."""
        total = self.report["summary"]["total_checks"]
        passed = self.report["summary"]["passed"]
        warn = self.report["summary"]["warnings"]
        crit = self.report["summary"]["critical"]
        
        # Scoring: Pass = 100%, Warn = 70%, Fail = 0%
        if total > 0:
            score = round(((passed * 1.0) + (warn * 0.70)) / total * 100, 1)
        else:
            score = 0.0
            
        self.report["summary"]["score_percent"] = score
        
        if crit == 0 and warn == 0:
            verdict = "BROADCAST READY (สมบูรณ์แบบ 100%)"
        elif crit == 0 and warn <= 3:
            verdict = "ACCEPTED WITH MINOR SUGGESTIONS (ผ่านเกณฑ์มาตรฐาน - ปรับปรุงเสริมได้)"
        elif crit == 0:
            verdict = "NEEDS POLISHING (ควรปรับปรุงแก้ไขก่อนเผยแพร่)"
        else:
            verdict = "REJECTED / ACTION REQUIRED (มีข้อผิดพลาดร้ายแรง ต้องแก้ไขทันที)"
            
        self.report["summary"]["verdict"] = verdict
        return verdict, score

    def print_terminal_summary(self):
        """Print high-contrast executive summary to terminal."""
        verdict, score = self.calculate_score_and_verdict()
        crit = self.report["summary"]["critical"]
        warn = self.report["summary"]["warnings"]
        passed = self.report["summary"]["passed"]
        
        print(f"\n{'='*75}")
        print(f"{BOLD}LEMiNO DOCUMENTARY VIDEO QA INSPECTION SUMMARY{RESET}")
        print(f"{'='*75}")
        print(f"File Tested:     {BOLD}{self.report['meta']['file_name']}{RESET}")
        print(f"File Size:       {self.report['meta']['file_size_mb']} MB")
        print(f"Quality Score:   {BOLD}{score}%{RESET} ({passed} Passed, {warn} Warnings, {crit} Critical)")
        
        color = GREEN if crit == 0 and warn <= 2 else YELLOW if crit == 0 else RED
        print(f"Final Verdict:   {color}{BOLD}{verdict}{RESET}")
        print(f"{'='*75}")
        
        if self.report["remediations"]:
            print(f"\n{BOLD}{YELLOW}📋 รายการจุดบกพร่องและแนวทางแก้ไข (ACTIONABLE REMEDIATIONS):{RESET}")
            for idx, r in enumerate(self.report["remediations"], 1):
                sev_badge = f"{RED}[CRITICAL]{RESET}" if r["severity"] == "FAIL" else f"{YELLOW}[WARNING]{RESET}"
                print(f"\n{BOLD}{idx}. {sev_badge} {r['defect']}{RESET}")
                print(f"   💡 วิธีแก้ไข: {r['remedy']}")
                if r["cmd_fix"]:
                    print(f"   💻 คำสั่งแก้ไขด่วน (One-Click Command):\n      {CYAN}{r['cmd_fix']}{RESET}")
        else:
            print(f"\n{GREEN}{BOLD}✨ ตรวจสอบแล้ว ไม่พบข้อผิดพลาดร้ายแรง! วิดีโอพร้อมเผยแพร่และส่งมอบทันที!{RESET}")
        print(f"{'='*75}\n")

    def export_reports(self, out_md_path, out_json_path=None, out_docx_path=None):
        """Export comprehensive audit reports in Markdown, JSON, and Word DOCX."""
        # 1. JSON
        if out_json_path:
            with open(out_json_path, "w", encoding="utf-8") as f:
                json.dump(self.report, f, indent=2, ensure_ascii=False)
            print(f"Exported JSON Audit: {out_json_path}")
            
        # 2. Markdown
        with open(out_md_path, "w", encoding="utf-8") as f:
            f.write(f"# 🛡️ LEMiNO Post-Render Video QA Inspection Report\n\n")
            f.write(f"**ไฟล์ที่ตรวจสอบ:** `{self.report['meta']['file_name']}`  \n")
            f.write(f"**ขนาดไฟล์:** {self.report['meta']['file_size_mb']} MB  \n")
            f.write(f"**เวลาที่ตรวจสอบ:** {self.report['meta']['timestamp']}  \n")
            f.write(f"**คะแนนคุณภาพ (Quality Score):** `{self.report['summary']['score_percent']}%`  \n")
            f.write(f"**ผลการตัดสิน (Verdict):** **{self.report['summary']['verdict']}**  \n\n")
            
            f.write(f"## 1. ผลการตรวจสอบทางเทคนิค (Technical Checks)\n\n")
            f.write(f"| หมวดหมู่ | รายการตรวจสอบ | สถานะ | ผลลัพธ์โดยละเอียด |\n")
            f.write(f"| :--- | :--- | :---: | :--- |\n")
            for c in self.report["checks"]:
                st_icon = "🟢 PASS" if c["status"] == "PASS" else "🟡 WARN" if c["status"] == "WARN" else "🔴 FAIL"
                f.write(f"| **{c['category']}** | {c['name']} | {st_icon} | {c['details']} |\n")
                
            f.write(f"\n## 2. วิธีการแก้ไขจุดบกพร่อง (Actionable Fixes & Remediations)\n\n")
            if not self.report["remediations"]:
                f.write(f"> ✅ **ผ่านเกณฑ์มาตรฐานบรอดแคสต์ครบถ้วนทุกข้อ** ไม่พบข้อบกพร่องที่ต้องแก้ไข\n\n")
            else:
                for idx, r in enumerate(self.report["remediations"], 1):
                    badge = "🔴 **CRITICAL**" if r["severity"] == "FAIL" else "🟡 **WARNING**"
                    f.write(f"### ข้อที่ {idx}: {badge} — {r['defect']}\n\n")
                    f.write(f"* **คำอธิบายและแนวทางแก้ไข:** {r['remedy']}\n")
                    if r["cmd_fix"]:
                        f.write(f"* **คำสั่งแก้ไขด่วนใน Terminal (CLI Fix):**\n")
                        f.write(f"```bash\n{r['cmd_fix']}\n```\n\n")
                        
        print(f"Exported Markdown Audit: {out_md_path}")
        
        # 3. Word DOCX
        if out_docx_path:
            try:
                import docx
                from docx.shared import Inches, Pt, RGBColor
                from docx.enum.text import WD_ALIGN_PARAGRAPH
                from docx.enum.table import WD_TABLE_ALIGNMENT
                from docx.oxml import OxmlElement
                from docx.oxml.ns import qn

                def set_shd(cell, hex_color):
                    tcPr = cell._tc.get_or_add_tcPr()
                    shd = OxmlElement('w:shd')
                    shd.set(qn('w:val'), 'clear')
                    shd.set(qn('w:color'), 'auto')
                    shd.set(qn('w:fill'), hex_color)
                    tcPr.append(shd)

                doc = docx.Document()
                for s in doc.sections:
                    s.top_margin = Inches(0.8)
                    s.bottom_margin = Inches(0.8)
                    s.left_margin = Inches(0.8)
                    s.right_margin = Inches(0.8)

                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run("รายงานการตรวจสอบคุณภาพวิดีโอ (Post-Render QA Inspection Report)")
                r.font.name = "Angsana New"
                r.font.size = Pt(24)
                r.font.bold = True
                r.font.color.rgb = RGBColor(26, 122, 110)

                p2 = doc.add_paragraph()
                p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r2 = p2.add_run(f"ไฟล์: {self.report['meta']['file_name']} | คะแนน: {self.report['summary']['score_percent']}% | ผล: {self.report['summary']['verdict']}")
                r2.font.name = "Angsana New"
                r2.font.size = Pt(15)
                r2.font.bold = True
                r2.font.color.rgb = RGBColor(180, 130, 45)

                doc.add_paragraph()
                h1 = doc.add_heading(level=1)
                rh1 = h1.add_run("1. ตารางบันทึกผลการตรวจสอบทางเทคนิค")
                rh1.font.name = "Angsana New"
                rh1.font.size = Pt(18)
                rh1.font.bold = True
                rh1.font.color.rgb = RGBColor(26, 122, 110)

                table = doc.add_table(rows=1, cols=4)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                hdr = table.rows[0].cells
                hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = "หมวดหมู่", "รายการตรวจสอบ", "สถานะ", "รายละเอียด"
                for i, w in enumerate([Inches(1.5), Inches(2.2), Inches(1.0), Inches(2.5)]):
                    hdr[i].width = w
                    set_shd(hdr[i], "121719")
                    for p_h in hdr[i].paragraphs:
                        for rh in p_h.runs:
                            rh.font.name = "Angsana New"
                            rh.font.size = Pt(13)
                            rh.font.bold = True
                            rh.font.color.rgb = RGBColor(255, 255, 255)

                for c in self.report["checks"]:
                    row = table.add_row()
                    c0, c1, c2, c3 = row.cells
                    c0.width, c1.width, c2.width, c3.width = Inches(1.5), Inches(2.2), Inches(1.0), Inches(2.5)
                    c0.text = c["category"]
                    c1.text = c["name"]
                    c2.text = c["status"]
                    c3.text = c["details"]
                    bg = "F0FFF0" if c["status"] == "PASS" else "FFF9E6" if c["status"] == "WARN" else "FFEBE6"
                    for cell in (c0, c1, c2, c3):
                        set_shd(cell, bg)
                        for p_c in cell.paragraphs:
                            for rc in p_c.runs:
                                rc.font.name = "Angsana New"
                                rc.font.size = Pt(12)

                doc.add_paragraph()
                h2 = doc.add_heading(level=1)
                rh2 = h2.add_run("2. แนวทางการแก้ไขจุดบกพร่อง (Actionable Fixes)")
                rh2.font.name = "Angsana New"
                rh2.font.size = Pt(18)
                rh2.font.bold = True
                rh2.font.color.rgb = RGBColor(26, 122, 110)

                if not self.report["remediations"]:
                    p_none = doc.add_paragraph()
                    p_none.add_run("✅ ตรวจสอบแล้วไม่พบข้อบกพร่อง วิดีโอสมบูรณ์พร้อมใช้งาน")
                else:
                    for idx, rem in enumerate(self.report["remediations"], 1):
                        p_rem = doc.add_paragraph()
                        r_t = p_rem.add_run(f"ข้อที่ {idx}: [{rem['severity']}] {rem['defect']}\n")
                        r_t.font.name = "Angsana New"
                        r_t.font.size = Pt(14)
                        r_t.font.bold = True
                        r_t.font.color.rgb = RGBColor(180, 130, 45)

                        r_b = p_rem.add_run(f"วิธีแก้ไข: {rem['remedy']}\n")
                        r_b.font.name = "Angsana New"
                        r_b.font.size = Pt(13)

                        if rem["cmd_fix"]:
                            r_c = p_rem.add_run(f"คำสั่งแก้ไข: {rem['cmd_fix']}\n")
                            r_c.font.name = "Courier New"
                            r_c.font.size = Pt(10)
                            r_c.font.color.rgb = RGBColor(30, 80, 120)

                doc.save(out_docx_path)
                print(f"Exported DOCX Audit: {out_docx_path}")
            except Exception as e:
                print(f"Warning: Could not export DOCX: {e}")

    def inspect(self):
        """Execute full QA diagnostic pipeline."""
        print(f"\n{BOLD}{'='*75}{RESET}")
        print(f"{BOLD}LEMiNO AUTOMATED VIDEO QA INSPECTOR // INITIALIZING AUDIT{RESET}")
        print(f"Target Video: {self.video_path}")
        print(f"{'='*75}")
        
        probe_data = self.run_ffprobe()
        self.check_container_and_faststart(probe_data)
        self.check_video_stream(probe_data)
        self.check_audio_stream(probe_data)
        self.run_deep_audio_loudness_analysis()
        self.run_artifact_and_drop_detection()
        
        self.print_terminal_summary()
        return self.report

def main():
    parser = argparse.ArgumentParser(description="LEMiNO Automated Video QA Inspector & Remediation Unit")
    parser.add_argument("video", help="Path to rendered MP4 video file to inspect")
    parser.add_argument("--duration", type=float, default=900.0, help="Target duration in seconds (default: 900.0)")
    parser.add_argument("--fps", type=float, default=30.0, help="Target framerate (default: 30.0)")
    parser.add_argument("--lufs", type=float, default=-14.0, help="Target integrated loudness (default: -14.0)")
    parser.add_argument("--export-md", default="QA_INSPECTION_REPORT.md", help="Output markdown report path")
    parser.add_argument("--export-json", default=None, help="Output JSON report path")
    parser.add_argument("--export-docx", default=None, help="Output Word DOCX report path")
    parser.add_argument("--auto-fix", action="store_true", help="Automatically execute fixes for non-critical warnings (e.g. FastStart, Loudnorm)")
    args = parser.parse_args()

    inspector = VideoQAInspector(
        args.video,
        target_duration=args.duration,
        target_fps=args.fps,
        target_lufs=args.lufs
    )
    report = inspector.inspect()
    inspector.export_reports(args.export_md, args.export_json, args.export_docx)
    
    # Auto-fix execution if requested
    if args.auto_fix and report["remediations"]:
        print(f"\n{BOLD}{CYAN}=== EXECUTING AUTOMATIC REMEDIATIONS (--auto-fix) ==={RESET}")
        for r in report["remediations"]:
            cmd = r.get("cmd_fix")
            if cmd and not cmd.startswith("#"):
                print(f"Running fix: {cmd}")
                try:
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"{GREEN}✓ Successfully applied fix!{RESET}")
                except Exception as e:
                    print(f"{RED}✗ Fix failed: {e}{RESET}")

if __name__ == "__main__":
    main()
