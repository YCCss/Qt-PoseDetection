#姿势识别
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui

from Ui_MainWindow import Ui_MainWindow
from human_pose import HumanPose
from face_detection import FaceDetection
from face_mesh import FaceMesh
from hand_pose import HandPose

def messageDialog(title, content):
    '''
    弹警告或者提示消息框
    :param title: 框的名字
    :param content: 提示的信息
    :return:
    '''
    msg_box = QMessageBox(QMessageBox.Warning, title, content)
    msg_box.exec_()

class Ui_main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Ui_main, self).__init__()
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.detection = [HumanPose(),  # 建立姿态检测对象
                          FaceDetection(), # 建立人脸检测对象
                          FaceMesh(), # 建立人脸网格检测对象
                          HandPose() # 建立手势检测对象
                          ]
        self.choice_mode = 0 #检测模式选择
        self.setWindowIcon(QIcon('icon.png'))
        #文件类型的flag
        self.camera_flag = False
        self.video_flag = False
        self.figure_flag = False

        self.setupUi(self)
        self.connection()
        self.show()

    def open_camera(self):
        if self.video_flag or self.figure_flag:
            messageDialog('waring', '请关闭其他设备')
            return
        if not self.camera_flag:
            self.camera_flag = True
        else:
            self.camera_flag = False

        if self.timer_camera.isActive() == False: #如果定时器未启动
            self.cap = cv2.VideoCapture()  # 视频流
            self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
            flag = self.cap.open(self.CAM_NUM) #参数0，表示内置摄像头
            if flag == False:
                messageDialog('waring', '摄像头打开不成功')
            else:
                self.timer_camera.start(30) #定时器开始
                # 计时30ms，30ms取一帧图像
                self.camera.setText('关闭相机')
        else:
            self.timer_camera.stop() #关闭定时器
            self.cap.release() #释放视频流
            self.label.clear() #清空视频显示区域
            self.camera.setText('打开相机')

    def show_camera(self):
        flag, self.image = self.cap.read() #从视频中读取一帧
        if not flag:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label.clear()  # 清空视频显示区域
            self.video.setText('选择视频')
            self.camera.setText('打开相机')
            self.camera_flag = False
            self.video_flag = False

        else:
            show = cv2.resize(self.image, (640, 480)) #重置图片大小
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB) #BGR转RGB

            show = self.detection[self.choice_mode].findObj(show)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    def open_video(self):
        if self.camera_flag or self.figure_flag:
            messageDialog('waring', '请关闭其他设备')
            return
        if not self.video_flag:
            self.video_flag = True
        else:
            self.video_flag = False


        if self.timer_camera.isActive() == False:  # 如果定时器未启动
            directory = QFileDialog.getOpenFileName(self, "选择文件", "./",
                                                    "mp4 (*.mp4);;All Files (*);;Text Files (*.txt)")
            if (directory[0].lower().endswith(('.avi', '.rm', '.rmvb', '.flv', '.mp4', '.mov'))):
                pass
            else:
                messageDialog('waring', '请选择正确的图片格式')
                self.video_flag = False
                return

            self.cap = cv2.VideoCapture()  # 视频流
            flag = self.cap.open(directory[0])  # 打开视频文件
            if flag == False:
                messageDialog('waring', '视频打开不成功')
            else:
                self.timer_camera.start(30)  # 定时器开始
                # 计时30ms，30ms取一帧图像
                self.video.setText('关闭视频')
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label.clear()  # 清空视频显示区域
            self.video.setText('选择视频')

    def open_figure(self):
        if self.camera_flag or self.video_flag:
            messageDialog('waring', '请关闭其他设备')
            return

        directory = QFileDialog.getOpenFileName(self, "选择文件", "./",
                                                "All Files (*);;Text Files (*.txt)")
        if (directory[0].lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
            pass
        else:
            messageDialog('waring', '请选择正确的图片格式')
            return

        image = cv2.imread(directory[0])
        show = cv2.resize(image, (640, 480))  # 重置图片大小
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # BGR转RGB

        show = self.detection[self.choice_mode].findObj(show)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage

    # def ComBoxaddItem(self):
    #     '''
    #     向QComboBox控件中添加条目
    #     :return:
    #     '''
    #     self.modess.addItem('face_detection')
    #     self.modess.addItem('face_mesh')
    #     self.modess.addItem('hand_pose')
    #     self.modess.addItem('human_pose')

    def selectionchange(self):
        # a = self.modess.currentText() #选中的文本内容
        self.choice_mode = self.modess.currentIndex()
        # print(a, self.choice_mode)

    def connection(self):
        '''
        按键绑定
        :return:
        '''
        self.camera.clicked.connect(self.open_camera)
        self.video.clicked.connect(self.open_video)
        self.figure.clicked.connect(self.open_figure)
        self.timer_camera.timeout.connect(self.show_camera) #定时器显示视频
        self.modess.currentIndexChanged.connect(self.selectionchange) #当QComboBox的下拉改变时触发绑定事件

        self.exit.clicked.connect(self.close)  # 若该按键被点击，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ca = Ui_main()
    sys.exit(app.exec_())