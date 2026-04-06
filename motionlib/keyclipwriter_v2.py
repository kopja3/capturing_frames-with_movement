from collections import deque
import cv2


class KeyClipWriter:
    def __init__(self, bufSize=32):
        self.bufSize = bufSize
        self.frames = deque(maxlen=bufSize)
        self.writer = None
        self.recording = False

    def update(self, frame):
        if frame is None:
            return
        self.frames.append(frame.copy())
        if self.recording and self.writer is not None:
            self.writer.write(frame)

    def start_with_frame(self, outputPath, fourcc, fps, frame):
        if frame is None:
            raise RuntimeError("start_with_frame() needs a valid frame")

        if len(self.frames) == 0:
            self.frames.append(frame.copy())

        (h, w) = self.frames[0].shape[:2]
        self.writer = cv2.VideoWriter(outputPath, fourcc, fps, (w, h), True)
        if not self.writer.isOpened():
            raise RuntimeError(f"Could not open video writer for '{outputPath}'")

        for f in self.frames:
            self.writer.write(f)
        self.recording = True

    def finish(self):
        if self.writer is not None:
            self.writer.release()
        self.writer = None
        self.recording = False
