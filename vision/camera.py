import os
import threading
import time
import cv2
#import pyrealsense2 as rs
import numpy as np

img = [None]
video: cv2.VideoCapture

def cam_task():
    global img
    while True:
        if video.isOpened():
            ret, frame = video.read()
            if ret:
                img[0] = cv2.flip(frame, -1)
            time.sleep(1/30)
                

def camera_init() -> bool:
    global video
    video = cv2.VideoCapture(4)
    if not video.isOpened():
        return False
    threading.Thread(target=cam_task).start()
    while img[0] is None:
        time.sleep(0.01)
    return True
    

def get_camera_img():
    return img[0]

if __name__ == '__main__':
    camera_init()
    while True:
        cv2.imshow('img', get_camera_img())
        if cv2.waitKey(30) == ord('q'):
            exit()