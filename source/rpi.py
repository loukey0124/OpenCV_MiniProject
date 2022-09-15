from urllib import response
from wsgiref.util import request_uri
import numpy as np
import requests
from picamera import PiCamera
from time import sleep
import os

def CapData():
    count = 0
    global requestUrl
    
    cam.start_preview()
    while True:
        filename = str(count)+'.jpg'
        cam = PiCamera()
        
        sleep(1)
        cam.capture(filename)
        files = {'file': open(filename, 'rb')}
        response = requests.post(requestUrl+'/upload', files=files)
        os.remove(filename)
        
        if response.status_code == 200:
            print(count+"file Send Success")
        
        if count == 100:
            break
        
    cam.stop_preview()
    


if __name__ == '__main__':
    requestUrl = "http://192.168.0.43:5000"  
    while True:
        resp = requests.post(requestUrl)
        if resp == "nodata":
            CapData()
            
        sleep(1)