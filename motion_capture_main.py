from motionlib.keyclipwriter_safe import KeyClipWriter
from motionlib.conf import Conf
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import signal
import time
import sys
import cv2
import os

kcw = None
conf = None
stream = None
threaded_stream = False


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def build_subtractor(name: str):
    name = name.upper()
    if name == "MOG2":
        return cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
    if name == "KNN":
        return cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0, detectShadows=True)

    bgsegm = getattr(cv2, "bgsegm", None)
    if bgsegm is None:
        raise RuntimeError("This subtractor needs opencv-contrib-python. Use MOG2 or KNN, or install opencv-contrib-python.")

    mapping = {
        "CNT": bgsegm.createBackgroundSubtractorCNT,
        "GMG": bgsegm.createBackgroundSubtractorGMG,
        "MOG": bgsegm.createBackgroundSubtractorMOG,
        "GSOC": bgsegm.createBackgroundSubtractorGSOC,
        "LSBP": bgsegm.createBackgroundSubtractorLSBP,
    }
    if name not in mapping:
        raise ValueError(f"Unsupported background subtractor: {name}")
    return mapping[name]()


def open_stream(video_path: str, conf: Conf):
    if video_path:
        print(f"[INFO] opening video file '{video_path}'")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video file: {video_path}")
        return cap, False

    print("[INFO] starting video stream...")
    use_picamera = bool(conf.get("picamera", False))
    camera_src = conf.get("camera_src", 0)
    if use_picamera:
        vs = VideoStream(usePiCamera=True).start()
    else:
        vs = VideoStream(src=camera_src).start()
    time.sleep(conf.get("warmup_seconds", 2.0))
    return vs, True


def read_frame(stream, threaded: bool):
    if threaded:
        return stream.read()
    grabbed, frame = stream.read()
    if not grabbed:
        return None
    return frame


def close_stream(stream, threaded: bool):
    if stream is None:
        return
    if threaded:
        stream.stop()
    else:
        stream.release()


def signal_handler(sig, frame):
    global kcw, conf, stream, threaded_stream
    print("\n[INFO] stopping...")
    if conf is not None:
        print(f"[INFO] output directory: {conf['output_path']}")
    if kcw is not None and kcw.recording:
        kcw.finish()
    close_stream(stream, threaded_stream)
    cv2.destroyAllWindows()
    sys.exit(0)


def main():
    global kcw, conf, stream, threaded_stream

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
    ap.add_argument("-v", "--video", type=str, help="path to optional input video file")
    args = vars(ap.parse_args())

    conf = Conf(args["conf"])
    ensure_dir(conf["output_path"])
    stream, threaded_stream = open_stream(args.get("video"), conf)
    signal.signal(signal.SIGINT, signal_handler)

    fgbg = build_subtractor(conf.get("bg_sub", "MOG2"))
    e_kernel = np.ones(tuple(conf["erode"]["kernel"]), dtype="uint8")
    d_kernel = np.ones(tuple(conf["dilate"]["kernel"]), dtype="uint8")

    kcw = KeyClipWriter(bufSize=conf.get("keyclipwriter_buffersize", 32))
    frames_without_motion = 0
    frames_since_snap = 0

    images = " and images..." if conf.get("write_snaps", False) else "..."
    print(f"[INFO] detecting motion and storing videos{images}")

    while True:
        full_frame = read_frame(stream, threaded_stream)
        if full_frame is None:
            break

        frames_since_snap += 1
        frame = imutils.resize(full_frame, width=conf.get("resize_width", 500))

        # Keep a pre-motion buffer so clips start a bit before the motion event.
        kcw.update(frame)

        mask = fgbg.apply(frame)
        mask = cv2.erode(mask, e_kernel, iterations=conf["erode"].get("iterations", 1))
        mask = cv2.dilate(mask, d_kernel, iterations=conf["dilate"].get("iterations", 2))

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        motion_this_frame = False

        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            (rx, ry, rw, rh) = cv2.boundingRect(c)
            x, y, radius = int(x), int(y), int(radius)
            if radius < conf.get("min_radius", 8):
                continue

            motion_this_frame = True
            frames_without_motion = 0
            timestring = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            if conf.get("annotate", True):
                cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), (0, 255, 0), 2)

            should_write_snap = frames_since_snap >= conf.get("frames_between_snaps", 20)
            if conf.get("write_snaps", False) and should_write_snap:
                snap_path = os.path.join(conf["output_path"], f"{timestring}.jpg")
                cv2.imwrite(snap_path, full_frame)
                frames_since_snap = 0

            if not kcw.recording:
                video_path = os.path.join(conf["output_path"], f"{timestring}.avi")
                fourcc = cv2.VideoWriter_fourcc(*conf.get("codec", "MJPG"))
                kcw.start_with_frame(video_path, fourcc, conf.get("fps", 20), frame)

        if not motion_this_frame:
            frames_without_motion += 1

        if kcw.recording and frames_without_motion >= conf.get("keyclipwriter_buffersize", 32):
            kcw.finish()

        if conf.get("display", True):
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    if kcw.recording:
        kcw.finish()
    close_stream(stream, threaded_stream)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
