import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

class FaceDetection:
    def __init__(self):
        self.face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    def findObj(self, img, draw=True):
        '''

        :param img: 输入图片
        :param draw: 绘制人脸框
        :return: 绘制好的人脸图片
        '''
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except:
            print("遇到些问题")
        self.results = self.face_detection.process(img)
        if self.results.detections:
            for detection in self.results.detections:
                if draw:
                    mp_drawing.draw_detection(img, detection)
        return img