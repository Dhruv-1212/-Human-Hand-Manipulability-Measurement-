from Camera_init import *
import os
import shutil
import cv2
import glob
import numpy as np


# Define the frame width and height
h = 480  # y co-ordinate
w = int(1.3334*h)  # x co-ordinate
# 480, 640
# Now 650, 866 frame shape

# *********************************************** Get Images *******************************************************




def get_img(n):
    # Create the images directory if it does not exist
    list_=["red","blue","green"]

    num = 0
    a = 1
    while a:
        ret, depth_frame, depth_img, color_frame = dc.get_frame()


        color_frame = cv2.resize(color_frame, (w, h))
        if not ret:
            print("return value is", ret)
            continue

        # cv2.imshow("color_frame", color_frame)
        
        # if key_pressed == ord('q'):
        #     break

        cv2.imwrite('images/'+list_[n] + '.jpg', color_frame)
        print("image saved!")
        num += 1

        a = 0

    # dc.release()
    # cv2.destroyAllWindows()


if os.path.exists('images'):
    shutil.rmtree('images')
os.makedirs('images')

dc = DepthCamera()

