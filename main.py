import pygame
import sys
import random
import gtts
import os
import coordinate_finder
import camera_inp
import time
import distance
import cv2
import mediapipe as mp
import pandas as pd
from camera_inp import dc
import csv
import threading
from queue import Queue
from Camera_init import *







pygame.init()
coordinates=[]
global count
count = 0
global calibration
calibration=False
res = (1280, 720)
color = (255, 255, 255)
screen = pygame.display.set_mode(res)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
width = screen.get_width()
height = screen.get_height()
alphabets=[0,0,0,0,0,0]

screen = pygame.display.set_mode(res)
smallfont = pygame.font.SysFont('Corbel', 300)

shared_data = Queue()

class HandGestureDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.coordinates_index = [0, 0, 0]
        self.arr = pd.read_csv('mydata.csv')
        self.touch = False
        self.csv_filename = 'hand_depth_wrt_screen.csv'
        self.dc=DepthCamera
            # Create a new CSV file with headers if it doesn't exist
        with open(self.csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['x', 'y', 'z', 'screen'])  # Add your column headers here

    def detect_hand(self):
        
        while(True):
            ret, depth_frame, depth_img, color_frame=self.dc.get_frame()
            depth_img = cv2.resize(depth_img, (w, h))
            depth_frame = cv2.resize(depth_frame, (w, h))
            color_frame = cv2.resize(color_frame, (w, h))
            imgRGB = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)  
            results = self.hands.process(imgRGB)
            results=self.hands.process(imgRGB)
            # print(results.multi_hand_landmarks)
            if results.multi_hand_landmarks:
                for handlms in results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(color_frame, handlms)
                    for id, lm in enumerate(handlms.landmark):
                        if id == 8:
                            h, w, c = color_frame.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            self.coordinates_index[0] = cx
                            self.coordinates_index[1] = cy
                            self.coordinates_index[3] = depth_img[cy, cx]
                            self.compare_dist(self.coordinates_index)
                            print(cx,cy)
                            cv2.circle(color_frame, (cx, cy), 1, (255, 0, 0), cv2.FILLED)

    def touch_detected(self):
        return [self.touch, self.coordinates_index]

    def compare_dist(self, coordinates_index):
        temp = [0, 0, 0, 0]
        temp[0] = coordinates_index[0]
        temp[1] = coordinates_index[1]
        temp[2] = coordinates_index[2]
        temp[4] = self.arr(coordinates_index[0], coordinates_index[1])
        with open(self.csv_filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(temp)
        if (self.arr(coordinates_index[0], coordinates_index[1]) >= coordinates_index[2] - 50 and self.arr(coordinates_index[0], coordinates_index[1]) <= coordinates_index[2] + 50):
            self.touch = True


def calibration_():
    global coordinates
    clock = pygame.time.Clock()
    fps = 10
    clock.tick(fps)
    global calibration
    global count
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()
    #red

    if(count>=0 and count<10):
        screen.fill((255, 0, 0))

    if(count==12):
        camera_inp.get_img(0)
    # camera_inp.get_img(0)
    if(count>=15 and count<20):
        # blue
        print("green")
        screen.fill((0, 255, 0))


    if(count==22):
    # camera_inp.get_img(1)
        camera_inp.get_img(2)
    if (count>=28 and count<35):
        # blue
        print("blue")
        screen.fill((0, 0, 255))

    if (count==38):
        # camera_inp.get_img(1)
        camera_inp.get_img(1)
    # faceCam.end()
    if(count>=39):
        coordinates, coordinate_game, coordinate_calc=coordinate_finder.read_images()
        distance.take_dist(coordinate_calc,coordinate_game )
    if(distance.dist_status()):
        calibration=True
    print(count)

def game_init():
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()



    screen.fill((60, 25, 60))


def game_start():
    global count
    screen.fill((60, 25, 60))
    while True:

        if(calibration==False):
            print("calibration")
            calibration_()
        if(calibration==True):
            # print("game runing")
            
            var=hand_detector.touch_detected()
            if(var[0]):
                hand_detector.touch=False
                coord=[]
                coord[0]=shared_data.get()
                if(coord[0]==None):
                    continue
                coord[1]=shared_data.get()
                if(coord[1]==None):
                    continue
                new_color = (0, 0, 0) 
                pygame.draw.circle(screen, new_color, (coord[0], coord[1]), 5)
    # Set the color of the specific pixel
                # for x in range(-10,10):
                #     for y in range(-10,10):
                #         #####################################################
                #         #apply the condition of boundry
                #         screen.set_at((coord[0]+x, coord[1]+y), new_color)

    # Update the display
            pygame.display.flip()
        count+=1
        pygame.display.update()


hand_detector = HandGestureDetector()

thread1 = threading.Thread(target=game_start).start()

thread2 = threading.Thread(target=hand_detector.detect_hand()).start()
    
