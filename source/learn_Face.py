import cv2 as cv
import numpy as np

face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

def FaceExtract(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    
    if faces == ():
        return None
    
    for (x, y, w, h)in faces:
        cropped_face = img[y:y+h, x:x+w]
    
    return cropped_face

if __name__ == '__main__':
    count = 0
    dataPath = './data'
    while True:
        frame = cv.imread(dataPath+'/'+str(count)+'.jpg')
        if FaceExtract(frame) is not None:
            count += 1
            face = cv.resize(FaceExtract(frame), (200, 200))
            face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
            file_name_path = 'faces/user'+str(count)+'.jpg'
            cv.imwrite(file_name_path, face)
        else:
            print(str(count)+"Face Not Fount")
            count += 1
            pass
            
        if cv.waitKey(1) == 13 or count == 100:
            break
        
    print("Sample Collecting Complete")