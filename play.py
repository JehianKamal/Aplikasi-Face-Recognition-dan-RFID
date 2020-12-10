"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

from ui_main_window import *
from takephoto import Ui_MainWindow

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        


    # view camera
    def viewCam(self):
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
        rec = cv2.face.LBPHFaceRecognizer_create();
        rec.read("recognizer\\trainingData.yml")
        id = 0
        path = 'dataset'
        font=cv2.FONT_HERSHEY_SIMPLEX
        def getProfile(id):
            conn=sqlite3.connect("FacaBase.db")
            cmd = "SELECT * FROM People WHERE ID="+str(id)
            cursor=conn.execute(cmd)
            profile=None
            for row in cursor:
                profile=row
            conn.close()
            return profile

        def loadData(id):
            conn=sqlite3.connect("database/"+str(id)+".db")
            cmd = "SELECT * FROM BUKU"
            cursor=conn.execute(cmd)
            self.ui.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(cursor):
                self.ui.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            conn.close() 



        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            print(conf)
            if (conf<50):
                profile=getProfile(id)
                if (profile!=None):
                    print(str(profile[1]))
                    cv2.putText(image,str(profile[1]),(x,y+h),font,1,(0,255,0),2,cv2.LINE_AA);
                    self.ui.lineEdit_2.setText(str(id))
                    self.ui.lineEdit.setText(str(profile[1]))
                    self.ui.lineEdit_6.setText(str(profile[2]))
                    loadData(self.ui.lineEdit_2.text())
                    
            else:
                print("Unknown")
                cv2.putText(image,"Tidak diketahui",(x,y+h),font,1,(0,0,255),2,cv2.LINE_AA);

        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")
            


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
