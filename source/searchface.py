import cv2 as cv
import numpy as np
from os import listdir
from PIL import Image
from os.path import isfile, join
import os

global confidence

def face_detector(img):
    face_classifier = cv.CascadeClassifier('./source/haarcascade_frontalface_default.xml')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv.resize(roi, (200,200))
    return img,roi   

def learnFace():
    face_cascade = cv.CascadeClassifier('./source/haarcascade_frontalface_default.xml')
    model = cv.face.LBPHFaceRecognizer_create()
    data_path = './data/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    Training_Data, Labels = [], []
    for i, files in enumerate(onlyfiles):    
        image_path = data_path + onlyfiles[i]
        images = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        faces = face_cascade.detectMultiScale(images, scaleFactor=1.3, minNeighbors=5)
        if images is None:
            continue     
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)
    if len(Labels) == 0:
        exit()
    Labels = np.asarray(Labels, dtype=np.int32)
    #모델 생성 
    model = cv.face.LBPHFaceRecognizer_create()
    #학습 시작 
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    model.save("face-trainner.yml")

def ImageMatching(model):
    while True:
        frame = cv.imread('./data/face.jpg')
        image, face = face_detector(frame)
        face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
        result = model.predict(face) 
        if result[1] < 500:
            confidence = int(100*(1-(result[1])/300))
        os.remove('./data/face.jpg')
        return confidence
    
def GetModel():
    model = cv.face.LBPHFaceRecognizer_create()
    model.read("face-trainner.yml")
    return model