from urllib import response
from wsgiref.util import request_uri
import numpy as np
import requests
from picamera import PiCamera
from time import sleep
import os
import cv2 as cv

face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

def FaceExtract(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is ():
        return None
    
    for (x, y, w, h)in faces:
        cropped_face = img[y:y+h, x:x+w]
        
    return cropped_face
    
def CapData():
    count = 0
    global requestUrl
    
    cap = cv.VideoCapture(0)
    if cap.isOpened() == False:
        exit()
    
    while True:
        filename = str(count)+'.jpg'
        ret, img = cap.read()
        
        if FaceExtract(img) is not None:
            count += 1
            face = cv.resize(FaceExtract(img), (200, 200))
            face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
            cv.imwrite(filename, face)
        else:
            print("Face Not Fount")
            continue
            
        
        files = {'file': open(filename, 'rb')}
        response = requests.post(requestUrl+'/upload', files=files)
        os.remove(filename)
        
        if response.status_code == 200:
            print(str(count)+"file Send Success")
        
        if cv.waitKey(1) == 13 or count == 100:
            break
        
    cap.release()

if __name__ == '__main__':
    requestUrl = "http://192.168.0.43:5000"  
    CapData()