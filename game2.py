import pygame
import sys
import random
import gtts
from playsound import playsound
import os
import coordinate_finder
import camera_inp
import time
import distance
import Detect




Detect.detect_init()
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
while True:

    if(calibration==False):
        print("calibration")
        calibration_()
    if(calibration==True):
        print("game runing")
        game_init()
        #here we have to do for the logic of writing
        Detect.main()

        if(Detect.hand_detected()):
            if(Detect.compare_dist()):
                coord=Detect.pixel_coordinate()
                new_color = (0, 0, 0)  # Red color

# Set the color of the specific pixel
                screen.set_at((coord[0], coord[1]), new_color)

# Update the display
        pygame.display.flip()
        

    count=count+1
    pygame.display.update()
