import cv2,os
import sys
import numpy as np

facecascade=cv2.CascadeClassifier('Classifier/haarcascade_frontalface_default.xml')

recognizer=cv2.face.EigenFaceRecognizer_create()
#recognizer=cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Training Data/trainingDataEigen.yml")


video=cv2.VideoCapture(0)

#read data from textfile rollnos
def FileRead():
    Info = open("Rollno's.txt", "r")
    global Rollno
    Rollno = {}
    while (True):                                   
        Line = Info.readline()
        if Line == '':
            break
        split= Line.split(",")
        key=split[0]
        val=split[1]
        valedit=len(val)-1
        val=val[0:valedit]
        Rollno[int(key)] = val
    print(Rollno)
    return Rollno       
FileRead()          

ID=0
fontface=cv2.FONT_HERSHEY_DUPLEX
fontscale=.9
fontcolor=(255,255,255)
while True:
    ret,img=video.read()
    img = cv2.flip(img, 1)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=facecascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(75,238,255),2)
        ID,conf=recognizer.predict( cv2.resize(gray[y:y+h,x:x+w],(300,300)))
        print(ID,round(conf))
        if(conf<5500):
           #ID="Present"
            cv2.putText(img,Rollno.get(ID),(x+h-145,y-50),fontface,fontscale,fontcolor)
            cv2.putText(img,"Present",(x+h-135,y-20),fontface,fontscale,fontcolor)
           #conf=" {0}%".format(round(100-conf))
        else:
            ID="Not Registered"
            cv2.putText(img,str(ID),(x+h-175,y-20),fontface,fontscale,fontcolor)
            conf=" {0}%".format(round(100-conf))
        
        #cv2.putText(img,str(ID),(x+h-100,y-20),fontface,fontscale,fontcolor)
        #cv2.putText(img,str(conf),(x+h,y-20),fontface,fontscale,fontcolor)

        
    #cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('image', 600,600) 
    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       sys.exit()
       cv2.destroyAllWindows()





 

