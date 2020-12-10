import cv2,os
import numpy as np
from PIL import Image
import pickle
import sqlite3

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read("recognizer\\trainingData.yml")
id=0
path ='dataset'

font=cv2.FONT_HERSHEY_SIMPLEX

#test = input('masukkan nama test')
def getProfile(id):
    conn=sqlite3.connect("FacaBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile


while(True):
    ret, img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])    
        if (conf<50):
            profile=getProfile(id)
            if (profile!=None):
                print(str(profile[1]))
                cv2.putText(img,str(profile[1]),(x,y+h),font,1,(0,0,255),2,cv2.LINE_AA);
        else:
            print("Unknown")
            cv2.putText(img,"Tidak diketahui",(x,y+h),font,1,(0,0,255),2,cv2.LINE_AA);
            
        cv2.imshow("Recognize", img);
        key = cv2.waitKey(1)
        if(key == ord('q')):
            break;
ca.release()
cv2.destroyAllWindows()
    
