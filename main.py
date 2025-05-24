import subprocess
from pathlib import Path
import shutil
import sys
import platform
import os
import concurrent.futures

VIDEOS_FOLDER = "Videos"
PROCESSING_FOLDER = "Processing_folder"
VIDEO_TITLE = "Peetri"
AUDIO_URL = "https://uc5fb06c1de14b6a81e5c8899230.previews.dropboxusercontent.com/p/hls_playlist/ACrMZyo4xDraQJRbxiFhEsEuKxo9dV3lF4gd59QTLsYjBj4yukIGVckBTMSnAQMm36DPMPVruvCpALt5Tm50UFR9JhEGlikEvjwOPxJHPiPKnKz-TXcte76_y91tPIEPJgMlERP3xmGiw2npD7GnlFT_ysMet7kbUwZ_FSa-ZOdZtJ2vCCl2U_bKUZwR88arWsI8E8LGZZvjwXDAfue4XfFCzM8qW3EOnjgxacr9XpKlTmgHybBuJajBYkN2D9_9YNy-qgfvez2xo6pO_d1u0dRHaAAzRiihiicAhBX37xfbOl16Z8zGGk-aG3gQdCxU5oE6Ft7zg18OYKD3UC4DVtlV1PoNjb1A5MdSEi9ahzogzN01N__yYbcr0VmfI2FuNSZ_qKKH4TPbiEnWv7sGVoPN/p.m3u8?bps=128000&type=audio"
VIDEO_URL = "https://uc5fb06c1de14b6a81e5c8899230.previews.dropboxusercontent.com/p/hls_master_playlist/ACqg17jmu-DG89lkJNXjW5--mZ8YLErgckPN0XCw_7oj3fXvxb8igiVU6ESyAzaG1ThVRKFw_EvIVheo6k1Pa_TUr5BezvpcwOK4JQ-8Gy4FijtKV3Pat7K3_k6Uf-XJSI6iWaE8EX-g5R_eFlYheyoqCff4Pt-t1GAXMLUHp24wVBQRqTByzzSv9vf-MXOFyMHFs1thvAD0dM0dqUK4nK9QaPwLDO5PYvQt_MXblfQh3TX5eqWObsOUzfu86yJA0EZSEgp-qxvODp14qGlZA1o0cv8tjesjfFmA19B5boEJChikFzOu-3NQR4biTo5shmQ5IzUymIuiQj32W75dkjlW/p.m3u8?is_prewarmed=true"

Path(f"{VIDEOS_FOLDER}/{VIDEO_TITLE}/{PROCESSING_FOLDER}").mkdir(parents=True, exist_ok=True)

AUDIO_OUT = f"{VIDEOS_FOLDER}/{VIDEO_TITLE}/{PROCESSING_FOLDER}/audio.m4a"
VIDEO_OUT = f"{VIDEOS_FOLDER}/{VIDEO_TITLE}/{PROCESSING_FOLDER}/video.mp4"
FINAL_OUT = f"{VIDEOS_FOLDER}/{VIDEO_TITLE}/Complete_File_{VIDEO_TITLE}.mp4"

THREADS = os.cpu_count() or 2  # Use all available CPU cores, fallback to 2


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("FFmpeg is not installed or not in PATH.")
        if platform.system() == "Darwin":  # macOS
            print("Attempting to install FFmpeg using Homebrew...")
            result = subprocess.run("brew install ffmpeg", shell=True, check=True)
            if result.returncode != 0:
                print("Failed to install FFmpeg. Please install it manually: https://ffmpeg.org/download.html")
                sys.exit(1)
        else:
            print("Please install FFmpeg and ensure it's in your PATH: https://ffmpeg.org/download.html")
            sys.exit(1)


def run_ffmpeg_command(cmd: str) -> None:
    result = subprocess.run(cmd, shell=True, check=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.returncode}")


def main() -> None:
    print("Starting the video and audio download and merge process...")
    ensure_ffmpeg()

    print("Downloading audio and video files in parallel...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [
            executor.submit(run_ffmpeg_command, f'ffmpeg -y -i "{AUDIO_URL}" -c copy {AUDIO_OUT}'),
            executor.submit(run_ffmpeg_command, f'ffmpeg -y -i "{VIDEO_URL}" -c copy {VIDEO_OUT}'),
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    print("Merging audio and video files into a final output file...")
    run_ffmpeg_command(f"ffmpeg -y -i {VIDEO_OUT} -i {AUDIO_OUT} -c copy {FINAL_OUT}")

    output_size = Path(FINAL_OUT).stat().st_size
    print(f"Output file created: {FINAL_OUT} with size {output_size} bytes")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
