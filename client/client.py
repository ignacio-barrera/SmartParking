from picamera2 import Picamera2
import time
import requests
import datetime
import cv2

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1640, 1232)})
picam2.configure(config)
picam2.start()

SERVER_URL = 'http://192.168.100.177:5000/upload'
CAMERA_ID = 'R-Parking01'

def send_image(data):
    picam2.capture_file('image.jpg')

    with open('image.jpg', 'rb') as img_file:
        files = {'image': img_file}
        current_time = datetime.datetime.now().isoformat()
        data = {
            'camera_id': CAMERA_ID,
            'timestamp': current_time,
            'data': data
        }
        response = requests.post(SERVER_URL, files=files, data=data)
        print(response.text)

while True:
    send_image("some data from " + CAMERA_ID)
    time.sleep(5)