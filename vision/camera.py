import os
import threading
import time
import cv2
#import pyrealsense2 as rs
import numpy as np

img: any
video: cv2.VideoCapture

def cam_task():
    global img
    while True:
        if video.isOpened():
            ret, frame = video.read()
            if ret:
                img = frame
        time.sleep(1 / 30)

def camera_init() -> bool:
    global video
    video = cv2.VideoCapture(4)
    if not video.isOpened():
        return False
    threading.Thread(target=cam_task).start()
    return True
    

def get_camera_img():
    return img