import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class HandPose:
    def __init__(self):
        self.handpose = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

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

        self.results = self.handpose.process(img)
        if self.results.multi_hand_landmarks:
            if draw:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return img