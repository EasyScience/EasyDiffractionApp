import mss
import cv2
import pathlib
import numpy as np
from threading import Thread
from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QApplication


class ScreenRecorder(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.frame_rate = 24
        self.out_fname = 'tutorial.mp4'
        self.codecs = {
            'mp4': 'mp4v'
        }

        self.is_app_running = True

        self.device_pixel_ratio = QApplication.primaryScreen().devicePixelRatio()
        self.screen_size = QApplication.primaryScreen().size()
        self.screen_rect = QApplication.primaryScreen().geometry()

        self.mss_frame_rect = self.default_mss_frame_rect()

        QApplication.instance().aboutToQuit.connect(self.onAboutToQuit)

    def cv2_frame_size(self):
        return (
            int(self.mss_frame_rect['width'] * self.device_pixel_ratio),
            int(self.mss_frame_rect['height'] * self.device_pixel_ratio)
        )

    def default_mss_frame_rect(self):
        return {
            'top': self.screen_rect.y(),
            'left': self.screen_rect.x(),
            'width': self.screen_rect.width(),
            'height': self.screen_rect.height()
        }

    def set_mss_frame_rect(self, frame_rect=None, margin_rect=None):
        if frame_rect is None:
            self.mss_frame_rect = self.default_mss_frame_rect()
            return
        self.mss_frame_rect = frame_rect.toVariant()
        self.set_mss_frame_rect_margins(margin_rect)

    def set_mss_frame_rect_margins(self, margin_rect=None):
        if margin_rect is None:
            return
        margin_rect = margin_rect.toVariant()
        self.mss_frame_rect['top'] -= margin_rect['top']
        self.mss_frame_rect['left'] -= margin_rect['left']
        self.mss_frame_rect['width'] += margin_rect['left'] + margin_rect['right']
        self.mss_frame_rect['height'] += margin_rect['top'] + margin_rect['bottom']
        if self.mss_frame_rect['top'] < 0:
            self.mss_frame_rect['top'] = 0
        if self.mss_frame_rect['left'] < 0:
            self.mss_frame_rect['left'] = 0
        if self.mss_frame_rect['left'] + self.mss_frame_rect['width'] > self.screen_rect.width():
            self.mss_frame_rect['width'] -= self.screen_rect.width() - self.mss_frame_rect['left']
        if self.mss_frame_rect['top'] + self.mss_frame_rect['height'] > self.screen_rect.height():
            self.mss_frame_rect['height'] -= self.screen_rect.height() - self.mss_frame_rect['top']

    def video_codec(self):
        ext = pathlib.Path(self.out_fname).suffix
        ext = ext.replace('.', '')
        codec = self.codecs[ext]
        return cv2.VideoWriter_fourcc(*codec)

    def onAboutToQuit(self):
        self.is_app_running = False

    def recording(self):
        out = cv2.VideoWriter(self.out_fname, self.video_codec(), self.frame_rate, self.cv2_frame_size())
        with mss.mss() as sct:
            while self.is_app_running:
                screenshot = sct.grab(self.mss_frame_rect)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
        cv2.destroyAllWindows()
        out.release()

    @Slot('QVariant', 'QVariant')
    def startRecording(self, frame_rect=None, margin_rect=None):
        self.set_mss_frame_rect(frame_rect, margin_rect)
        thread = Thread(target=self.recording)
        thread.start()
