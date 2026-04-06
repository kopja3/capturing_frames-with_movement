# Working motion capture setup

This repo had two structure conflicts:
- `pyimagesearch` existed as a file instead of a Python package
- `config` existed as a file instead of a directory

Because of that, the working version was added with new names:
- `motion_capture_v2.py`
- `motionlib/`
- `cfg/mog.json`
- `cfg/gmg.json`

## Install

```bash
pip install -r requirements.txt
```

## Run with camera

```bash
python motion_capture_v2.py --conf cfg/mog.json
```

## Run with a video file

```bash
python motion_capture_v2.py --conf cfg/mog.json --video birds_10min.mp4
```

## Alternative subtractor

```bash
python motion_capture_v2.py --conf cfg/gmg.json
```

## Notes

- `MOG2` works with standard OpenCV APIs.
- `GMG` needs `opencv-contrib-python`.
- Output videos and snapshots are written to `output_mog/` or `output_gmg/`.
