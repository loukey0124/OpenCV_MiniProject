from urllib import response
import RPi.GPIO as GPIO                    # RPi.GPIO에 정의된 기능을 GPIO라는 명칭으로 사용
import time                                # time 모듈
import requests
import os
import cv2 as cv
from time import sleep

face_classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
requestUrl = 'http://192.168.0.43:5000'

servo_pin = 27 
Echo_pin = 18
Trig_pin = 17
Led_pin = 4

GPIO.setmode(GPIO.BCM)                      # GPIO 이름은 BCM 명칭 사용
GPIO.setup(Trig_pin, GPIO.OUT)              # Trig=17 초음파 신호 전송핀 번호 지정 및 출력지정
GPIO.setup(Echo_pin, GPIO.IN)               # Echo=18 초음파 수신하는 수신 핀 번호 지정 및 입력지정

GPIO.setup(servo_pin, GPIO.OUT)             # servo = 27
servo  = GPIO.PWM(servo_pin, 50)            # 서보 동작 주파수 50
servo.start(0)                              # 0.6ms

GPIO.setup(Led_pin, GPIO.OUT)               # LED_pin

# requestUrl = "http://192.168.0.177:5000/upload"
# files = {'file': open('capImage.jpg', 'rb')}

print ('Press SW or input Ctrl+C to quit')   # 메세지 화면 출력


def FaceExtract(img):
   gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
   faces = face_classifier.detectMultiScale(gray,1.3,5)
   if faces is ():
      return None

   for (x, y, w, h)in faces:
      cropped_face = img[y:y+h, x:x+w]

   return cropped_face

def CapImage():
    global requestUrl
    filename = 'face.jpg'
    
    cap = cv.VideoCapture(0)
    if cap.isOpened() == False:
        exit()
    
    ret, img = cap.read()
    while FaceExtract(img) is None:
        print("Face Not Found")
        ret, img = cap.read()
        
    cv.imwrite(filename, img)
    files = {'file': open(filename, 'rb')}
    response = requests.post(requestUrl+'/upload', files=files)
    os.remove(filename)
        
    if response.status_code == 200:
            print("file Send Success")


def upload():
   requestUrl = 'http://192.168.0.43:5000/confirmFace'
   
   response = requests.get(requestUrl)
   if response.status_code == 200:
      print(response.text)
      return int(response.text)
   return 0

   
try:
    while True:
            GPIO.output(Trig_pin, False)         
            time.sleep(0.5)

            GPIO.output(Trig_pin, True)          # 10us 펄스를 내보낸다.
            time.sleep(0.00001)            # Python에서 이 펄스는 실제 100us 근처가 될 것이다
            GPIO.output(Trig_pin, False)         # 하지만 HC-SR04 센서는 이 오차를 받아준다

            while GPIO.input(Echo_pin) == 0:     # 18번 핀이 OFF 되는 시점을 시작 시간으로 잡는다
               start = time.time()

            while GPIO.input(Echo_pin) == 1:     # 18번 핀이 다시 ON 되는 시점을 반사파 수신시간으로 잡는다
               stop = time.time()

            time_interval = stop - start      # 초음파가 수신되는 시간으로 거리를 계산한다
            distance = time_interval * 17000
            distance = round(distance, 2)
            
            print ('Distance => ', distance, 'cm')
            if distance <= 10:
               #얼굴인식 관련코드
               CapImage()
               sleep(0.5)
               if upload() >= 88:
                  print('Door Open')
                  servo.ChangeDutyCycle(9) #90도 회전
                  print('LED On')
                  GPIO.output(Led_pin,True)
                  
                  time.sleep(2)
                  
                  print('Door Close')
                  servo.ChangeDutyCycle(2.5) #0도로 회전
                  print('LED Off')
                  GPIO.output(Led_pin,False)
                  time.sleep(1)
                  
               else:
                  continue
               
except KeyboardInterrupt:                  # Ctrl-C 입력 시
    GPIO.cleanup()                         # GPIO 관련설정 Clear
    print ('bye~')
               
