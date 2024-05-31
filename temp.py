import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2
import json

def image_receive():
    image_hub = imagezmq.ImageHub()

    while True:
        data_str, jpg_buffer = image_hub.recv_jpg()
        image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype="uint8"), -1)
        #convert data into dictionary
        data = json.loads(data_str)
        cv2.imshow(data['name'], image)
        
        #Print data, or do anything else you might need
        print(data)

        cv2.waitKey(1)
        image_hub.send_reply(b'OK')

try:
    image_receive()
finally:
    cv2.destroyAllWindows()