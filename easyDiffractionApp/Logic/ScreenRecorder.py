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

        QApplication.instance().aboutToQuit.connect(self.onAboutToQuit)

    def cv2_frame_size(self):
        return (
            int(self.screen_size.width() * self.device_pixel_ratio),
            int(self.screen_size.height() * self.device_pixel_ratio)
        )

    def mss_screen_rect(self):
        return {
            'top': self.screen_rect.y(),
            'left': self.screen_rect.x(),
            'width': self.screen_rect.width(),
            'height': self.screen_rect.height()
        }

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
                screenshot = sct.grab(self.mss_screen_rect())
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
        cv2.destroyAllWindows()
        out.release()

    @Slot()
    def startRecording(self):
        thread = Thread(target=self.recording)
        thread.start()
