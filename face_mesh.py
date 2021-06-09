import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

class FaceMesh:
    def __init__(self):
        self.drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

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

        self.results = self.face_mesh.process(img)
        if self.results.multi_face_landmarks:
            if draw:
                for face_landmarks in self.results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=img,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=self.drawing_spec,
                        connection_drawing_spec=self.drawing_spec)
        return img