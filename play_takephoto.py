import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import cv2
from takephoto import *

faceDetected = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0);

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.simpandata)
        id=self.ui.lineEdit.text()
        name = self.ui.lineEdit_2.text()
        insertOrUpdate(id, name)

    def insertOrUpdate(Id, Name):
        conn = sqlite3.connect("FacaBase.db")
        cmd = "SELECT * FROM People WHERE ID="+str(Id)
        cursor = conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
        if(isRecordExist==1):
            cmd = "UPDATE People SET Name="+str(Name)+"WHERE ID="+str(Id)
        else:
            cmd="INSERT INTO People(ID,Name) Values("+str(Id)+","+str(Name)+")"
        conn.execute(cmd)
        conn.commit()
        conn.close()

    def simpandata(self):
        
        while(True):
            sampleNum=0;
            ret, img = cam.read();
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=faceDetected.detectMultiScale(gray,1.3,5);
            for(x,y,w,h) in faces:
                sampleNum=sampleNum+1;
                cv2.imwrite("dataset/User."+self.ui.lineEdit.text()+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
                cv2.rectangle(img,(w,y),(x+w,y+h),(0,0,255),2)
                cv2.waitKey(100);
            cv2.imshow("Wajah",img);
            cv2.waitKey(1);
            if (sampleNum>20):
                break;
    
        cam.release()
        cv2.destroyAllWindows()
    

