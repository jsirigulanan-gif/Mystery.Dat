#!/usr/bin/env python3
import argparse
import os
import subprocess

def upload_folder(local_path, remote_folder):
    target = f"gdrive:Vids Exports/{remote_folder}"
    print(f"Uploading {local_path} to {target}...")
    cmd = ["rclone", "copy", local_path, target, "-P", "--drive-chunk-size", "64M"]
    subprocess.run(cmd, check=True)
    print("Upload complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Master Episode to Google Drive")
    parser.add_argument("--file", required=True, help="Local file to upload")
    parser.add_argument("--dest", required=True, help="Destination folder inside Vids Exports")
    args = parser.parse_args()
    upload_folder(args.file, args.dest)
