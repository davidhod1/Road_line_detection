import cv2

class Video:
    def __init__(self, video_source):
        self.videoSource = video_source
        self.video = cv2.VideoCapture(video_source)

        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def getFrame(self):
        if self.video.isOpened():
            ret,frame = self.video.read()

            if not ret:
                self.video = cv2.VideoCapture(self.videoSource)
                ret, frame = self.video.read()

            if ret:
                return ret, frame

    def __del__(self):
        if self.video.isOpened():
            self.video.release()