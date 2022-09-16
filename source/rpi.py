import requests
import os
import cv2 as cv

def FaceExtract(img):
    global face_classifier
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is ():
        return None
    
    for (x, y, w, h)in faces:
        cropped_face = img[y:y+h, x:x+w]
        
    return cropped_face
    
def SendFaceData():
    count = 0
    global requestUrl
    
    cap = cv.VideoCapture(0)
    if cap.isOpened() == False:
        exit()
    
    while True:
        filename = str(count+200)+'.jpg'
        ret, img = cap.read()
        
        if FaceExtract(img) is not None:
            count += 1
            face = cv.resize(FaceExtract(img), (200, 200))
            face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
            cv.imwrite(filename, face)
        else:
            print("Face Not Found")
            continue
            
        
        files = {'file': open(filename, 'rb')}
        response = requests.post(requestUrl+'/upload', files=files)
        os.remove(filename)
        
        if response.status_code == 200:
            print(str(count)+"file Send Success")
        
        if cv.waitKey(1) == 13 or count == 2000:
            break
        
    cap.release()


if __name__ == '__main__':
    face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    requestUrl = "http://192.168.0.43:5000"
    SendFaceData()