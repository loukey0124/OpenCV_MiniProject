import RPi.GPIO as GPIO                    # RPi.GPIO에 정의된 기능을 GPIO라는 명칭으로 사용
import time                                # time 모듈

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

print ('Press SW or input Ctrl+C to quit')   # 메세지 화면 출력

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
                
                #if(True) 라면
                servo.ChangeDutyCycle(2.5) #0도로 회전
                print('Duty :',servo.ChangeDutyCycle)
                time.sleep(0.5)
                servo.ChangeDutyCycle(6) #90도 회전
                print('Duty :',servo.ChangeDutyCycle)
                time.sleep(1.0)
                servo.ChangeDutyCycle(2.5) #0도로 회전
                print('Duty :',servo.ChangeDutyCycle)
                time.sleep(0.5)
                GPIO.output(Led_pin,True)
                print('LED On')
                time.sleep(2)
                GPIO.output(Led_pin,False)
                print('LED Off')
                time.sleep(2)
        
                



except KeyboardInterrupt:                  # Ctrl-C 입력 시
    GPIO.cleanup()                         # GPIO 관련설정 Clear
    print ('bye~')