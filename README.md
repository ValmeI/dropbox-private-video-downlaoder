# dropbox-private-video-downlaoder

Download videos from Dropbox when the link is restricting downloads.

**How to use:**
1. Open the script and set your Dropbox HLS audio and video URLs:
    ```python
    AUDIO_URL = "https://.../audio_filename.m3u8?bps=128000&type=audio""
    VIDEO_URL = "https://.../video_filename.m3u8?is_prewarmed=true"
    ```
   You need to provide both the audio and video stream URLs.

2. Run the script with Python.

3. The merged video will appear in the `Videos` folder.

**Requirements:**
- Python 3
- FFmpeg installed and available in your system PATH
