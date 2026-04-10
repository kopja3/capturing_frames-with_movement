from __future__ import annotations

import base64
import os
import tempfile
from dataclasses import dataclass, asdict
from typing import Annotated, Any

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

try:
    from ultralytics import YOLO
except Exception as exc:  # pragma: no cover
    YOLO = None
    YOLO_IMPORT_ERROR = str(exc)
else:
    YOLO_IMPORT_ERROR = None


@dataclass
class Settings:
    model_weights: str = os.getenv("BIRD_MODEL_WEIGHTS", "yolo11n.pt")
    confidence: float = float(os.getenv("MODEL_CONFIDENCE", "0.25"))
    default_frame_step: int = int(os.getenv("VIDEO_FRAME_STEP", "3"))
    motion_resize_width: int = int(os.getenv("MOTION_RESIZE_WIDTH", "640"))
    motion_min_area: int = int(os.getenv("MOTION_MIN_AREA", "1800"))
    enable_motion_gate: bool = os.getenv("ENABLE_MOTION_GATE", "1") != "0"
    allow_origins: str = os.getenv("ALLOW_ORIGINS", "*")


settings = Settings()
app = FastAPI(title="Bird Detection API With Stable Foreground Mask", version="1.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allow_origins.split(",") if origin.strip()] or ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
model_error = YOLO_IMPORT_ERROR
if YOLO is not None:
    try:
        model = YOLO(settings.model_weights)
    except Exception as exc:  # pragma: no cover
        model_error = str(exc)


class MotionGate:
    def __init__(self) -> None:
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=300,
            varThreshold=32,
            detectShadows=False,
        )
        self.prev_gray: np.ndarray | None = None
        self.warmup_left = 25

    def detect(self, frame: np.ndarray) -> tuple[bool, list[dict[str, int]], np.ndarray, bool, float, float]:
        h, w = frame.shape[:2]
        if w > settings.motion_resize_width:
            scale = settings.motion_resize_width / float(w)
            resized = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        else:
            scale = 1.0
            resized = frame

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if self.warmup_left > 0:
            self.warmup_left -= 1
            self.subtractor.apply(gray, learningRate=0.1)
            empty = np.zeros_like(gray)
            if scale != 1.0:
                empty = cv2.resize(empty, (w, h), interpolation=cv2.INTER_NEAREST)
            self.prev_gray = gray
            return False, [], empty, False, 0.0, 0.0

        mask = self.subtractor.apply(gray, learningRate=0.002)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)

        changed_ratio = cv2.countNonZero(mask) / float(mask.size)
        mean_delta = 0.0
        if self.prev_gray is not None:
            mean_delta = abs(float(gray.mean()) - float(self.prev_gray.mean()))
        self.prev_gray = gray

        flicker_rejected = changed_ratio > 0.35 and mean_delta > 8.0
        if flicker_rejected:
            empty = np.zeros_like(mask)
            if scale != 1.0:
                empty = cv2.resize(empty, (w, h), interpolation=cv2.INTER_NEAREST)
            return False, [], empty, True, changed_ratio, mean_delta

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        boxes: list[dict[str, int]] = []
        motion = False
        for contour in cnts:
            if cv2.contourArea(contour) < settings.motion_min_area:
                continue
            x, y, bw, bh = cv2.boundingRect(contour)
            boxes.append({
                "x": int(x / scale),
                "y": int(y / scale),
                "w": int(bw / scale),
                "h": int(bh / scale),
            })
            motion = True

        if scale != 1.0:
            mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)

        return motion, boxes, mask, False, changed_ratio, mean_delta


shared_motion_gate = MotionGate()


def ensure_model_ready() -> None:
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "YOLO-mallia ei voitu ladata. Tarkista ultralytics-asennus ja painotiedosto. "
                f"Nykyinen painotiedosto: {settings.model_weights}. Virhe: {model_error}"
            ),
        )


def decode_image(content: bytes) -> np.ndarray:
    arr = np.frombuffer(content, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Kuvan dekoodaus epäonnistui.")
    return frame


def encode_mask_png(mask: np.ndarray) -> str:
    ok, encoded = cv2.imencode('.png', mask)
    if not ok:
        raise HTTPException(status_code=500, detail='Maskin PNG-koodaus epäonnistui.')
    return base64.b64encode(encoded.tobytes()).decode('ascii')


def run_bird_model(frame: np.ndarray) -> list[dict[str, Any]]:
    ensure_model_ready()
    results = model.predict(frame, conf=settings.confidence, verbose=False)
    result = results[0]

    detections: list[dict[str, Any]] = []
    if result.boxes is None or len(result.boxes) == 0:
        return detections

    xyxy = result.boxes.xyxy.cpu().numpy().astype(int)
    conf = result.boxes.conf.cpu().numpy()
    cls = result.boxes.cls.cpu().numpy().astype(int)
    names = result.names

    for (x1, y1, x2, y2), score, class_id in zip(xyxy, conf, cls):
        label = str(names[int(class_id)])
        if label.lower() != 'bird':
            continue
        detections.append({
            'label': label,
            'confidence': float(score),
            'x1': int(x1),
            'y1': int(y1),
            'x2': int(x2),
            'y2': int(y2),
            'cx': int((x1 + x2) / 2),
            'cy': int((y1 + y2) / 2),
        })

    return detections


def analyze_frame(frame: np.ndarray, motion_gate: MotionGate) -> dict[str, Any]:
    motion_boxes: list[dict[str, int]] = []
    motion_detected = True
    motion_mask_png_base64 = None
    flicker_rejected = False
    changed_ratio = 0.0
    mean_delta = 0.0

    if settings.enable_motion_gate:
        motion_detected, motion_boxes, motion_mask, flicker_rejected, changed_ratio, mean_delta = motion_gate.detect(frame)
        motion_mask_png_base64 = encode_mask_png(motion_mask)

    detections: list[dict[str, Any]] = []
    if motion_detected or not settings.enable_motion_gate:
        detections = run_bird_model(frame)

    return {
        'frame_width': int(frame.shape[1]),
        'frame_height': int(frame.shape[0]),
        'motion_detected': motion_detected,
        'motion_boxes': motion_boxes,
        'motion_mask_png_base64': motion_mask_png_base64,
        'detections': detections,
        'flicker_rejected': flicker_rejected,
        'changed_ratio': changed_ratio,
        'mean_luma_delta': mean_delta,
    }


@app.get('/health')
def health() -> dict[str, Any]:
    return {
        'ok': True,
        'model_loaded': model is not None,
        'model_weights': settings.model_weights,
        'model_error': model_error,
    }


@app.get('/config')
def config() -> dict[str, Any]:
    return {
        'settings': asdict(settings),
        'model_loaded': model is not None,
        'model_error': model_error,
    }


@app.post('/detect-frame')
async def detect_frame(file: Annotated[UploadFile, File(...)]) -> dict[str, Any]:
    content = await file.read()
    frame = decode_image(content)
    return analyze_frame(frame, shared_motion_gate)


@app.post('/detect-video')
async def detect_video(
    file: Annotated[UploadFile, File(...)],
    frame_step: int = Query(default=settings.default_frame_step, ge=1, le=60),
) -> dict[str, Any]:
    ensure_model_ready()

    suffix = os.path.splitext(file.filename or 'video.mp4')[1] or '.mp4'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    if not cap.isOpened():
        os.unlink(tmp_path)
        raise HTTPException(status_code=400, detail='Videon avaaminen epäonnistui.')

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    frame_index = 0
    processed_frames = 0
    matches: list[dict[str, Any]] = []
    local_motion_gate = MotionGate()

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            if frame_index % frame_step != 0:
                frame_index += 1
                continue

            analysis = analyze_frame(frame, local_motion_gate)
            processed_frames += 1

            if analysis['detections']:
                matches.append({
                    'frame_index': frame_index,
                    'time_sec': (frame_index / fps) if fps > 0 else None,
                    'motion_detected': analysis['motion_detected'],
                    'motion_boxes': analysis['motion_boxes'],
                    'motion_mask_png_base64': analysis['motion_mask_png_base64'],
                    'detections': analysis['detections'],
                    'flicker_rejected': analysis['flicker_rejected'],
                    'changed_ratio': analysis['changed_ratio'],
                    'mean_luma_delta': analysis['mean_luma_delta'],
                })

            frame_index += 1
    finally:
        cap.release()
        os.unlink(tmp_path)

    return {
        'fps': fps,
        'frame_step': frame_step,
        'processed_frames': processed_frames,
        'matches': matches,
    }
