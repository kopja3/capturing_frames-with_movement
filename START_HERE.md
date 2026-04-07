# Start here

This repository now has two clear entry points.

## 1) Stable Python motion detector

Use this as the main program:

```bash
python3 -m pip install -r requirements.txt
python3 motion_capture_main.py --conf cfg/mog.json
```

Video file input:

```bash
python3 motion_capture_main.py --conf cfg/mog.json --video /path/to/video.mp4
```

Why this file:
- checks that a video file really opens
- keeps a pre-motion frame buffer
- starts video writing safely without the empty-buffer crash

## 2) Local browser demo

Open this file in a browser:

- `LOCAL_WEB_MOTION_DETECTION.html`

Then:
- choose a local video file
- click **Aloita analyysi**
- the page analyzes the video locally in the browser
- the video does not need to be uploaded to a server

Notes:
- the browser demo is a simple local proof of concept
- the Python version is better if you want saved clips and snapshots
