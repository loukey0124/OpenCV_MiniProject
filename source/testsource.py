import cv2 as cv 
import numpy as np
from os import listdir
from os.path import isfile, join
data_path = 'faces/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))] 
# faces폴더에 있는 파일 리스트 얻기

Training_Data, Labels = [], []
#파일 개수 만큼 루프

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    if images in None:
        continue
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)
if len(Labels) == 0:
    print("There is no data to train.")
    exit()
Labels = np.asarray(Labels, dtype=np.int32)
model = cv.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Model Training Complete")

#### 여긴 Part1.py와 거의 동일 
face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size = 0.5):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv.resize(roi, (200,200))
    return img,roi   #검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달
#### 여기까지 Part1.py와 거의 동일 
#카메라 열기 
cap = cv.VideoCapture(0)

while True:
    #카메라로 부터 사진 한장 읽기 
    ret, frame = cap.read()
    # 얼굴 검출 시도 
    image, face = face_detector(frame)
    try:
        #검출된 사진을 흑백으로 변환 
        face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
        #위에서 학습한 모델로 예측시도
        result = model.predict(face)
        #result[1]은 신뢰도이고 0에 가까울수록 자신과 같다는 뜻이다. 
        if result[1] < 500:
            #????? 어쨋든 0~100표시하려고 한듯 
            confidence = int(100*(1-(result[1])/300))
            # 유사도 화면에 표시 
            display_string = str(confidence)+'% Confidence it is user'
        cv.putText(image,display_string,(100,120), cv.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
        #75 보다 크면 동일 인물로 간주해 UnLocked! 
        if confidence > 75:
            # cv.putText(image, "Unlocked", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv.imshow('Face Cropper', image)
        else:
           #75 이하면 타인.. Locked!!! 
            # cv.putText(image, "Locked", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv.imshow('Face Cropper', image)
    except:
        #얼굴 검출 안됨 
        # cv.putText(image, "Face Not Found", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv.imshow('Face Cropper', image)
        pass
    if cv.waitKey(1)==13:
        break
cap.release()