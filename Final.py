from typing import Sized
import cv2 as cv
import os 
import time
import numpy as np
#importing coordinates of lane marking from file named as cor
from cor import *


#videographic input data

cap = cv.VideoCapture("video1.mp4")

object_detector = cv.createBackgroundSubtractorMOG2()
ret, frame = cap.read()

detec = []

min_width=20
 # min height
min_height=20
# permissible error value
offset=10

#Position of detection lines
#value in up is less than down
line_position_up=400
line_position_down=435

max_speed = 140

right_corner=800
left_corner=0
 #FPS of video
delay= 1700

# print(frame.shape)
dist = 4
matches = []
verify1,verify2,verify3,verify4,verify5,verify6 = 0,0,0,0,0,0
speed = [0,0,0,0,0,0]

cars = 0
truck = 0

recorded=-100
last=0
pos=0

def for_lane(corr,num,cx,cy):
    global verify1,tim1,tim2,speed,recorded,cars,truck
    recorded=-100
    if (cx >= corr[2][0]and cx <=corr[3][0] and cy <= corr[2][1]+offset and cy >= corr[2][1]-offset):
        cv.line(frame, (corr[0][0], corr[0][1]), (corr[1][0], corr[1][1]), (0, 255, 0),
                 2)  # Changes color of the line
        tim1 = time.time()  # Initial time
        verify1 = 1

                
    if (verify1 == 1 and cx >= corr[0][0]and cx<=corr[1][0] and cy >= corr[0][1]-offset and cy<=corr[0][1]+offset):
        cv.line(frame, (corr[2][0], corr[2][1]), (corr[3][0], corr[3][1]), (0, 0, 255), 2)
        tim2 = time.time()
        if tim2 >tim1:
            speed[num-1] =int((dist / ((tim2 - tim1)))*3.6)
            speed[num-1] = min(speed[num-1],max_speed)
            
            print("Car Entered lane "+str(num))
            print("Speed in (km/s) is:", speed[num-1])
            print("Car Left lane "+str(num))
            recorded=h
        verify1 = 0
    if(recorded<60 and recorded>0):
        cars+=1
        print("car is detected : "+str(cars)) 
    elif(recorded>=60):
        truck+=1
        print("truck is detected : "+str(truck)) 
    recorded=-100

bloch=(0, 0, 255)

while True:
    ret, frame = cap.read()
    tempo = float(1/delay)
    time.sleep(tempo)
    # cropped = frame1[100:1700, 100:1400]
    grey = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    # grey=frame1
    eroded = cv.erode(grey, (7,7), iterations=3)
    blur = cv.GaussianBlur(eroded,(3,3),20)
    blur = cv.bilateralFilter(blur, 10, 35, 25)
    img_sub = object_detector.apply(blur)
    dilat = cv.dilate(img_sub,np.ones((5,5)))
    # threshold,thresh_inv =cv.threshold(dilat, 110,255, cv.THRESH_BINARY)
    # #tweak values inside kernel
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    dilated = cv.morphologyEx (dilat, cv. MORPH_CLOSE , kernel)
    closing = cv.morphologyEx (dilated, cv. MORPH_CLOSE , kernel)
    
    contours, _ = cv.findContours(closing, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # cv.imshow('frame',closing)

    for i in range(0,6):
        cv.line(frame, (coord[i][0][0], coord[i][0][1]), (coord[i][1][0], coord[i][1][1]), (0, 0, 255), 2)  # First horizontal line
        cv.line(frame, (coord[i][0][0], coord[i][0][1]), (coord[i][2][0], coord[i][2][1]), (0, 0, 255), 2)  # Vertical left line
        cv.line(frame, (coord[i][2][0], coord[i][2][1]), (coord[i][3][0], coord[i][3][1]), (0, 0, 255), 2)  # Second horizontal line
        cv.line(frame, (coord[i][1][0], coord[i][1][1]), (coord[i][3][0], coord[i][3][1]), (0, 0, 255), 2)  # Vertical right line


    for cnt in contours:
        area = cv.contourArea(cnt)

        if area > 100:
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame,(x-5,y-5), (x+w+5,y+h+5),(0,255,0), 2)
            cx = int(x+w/2)
            cy = int(y+h/2)
            cv.circle(frame,(cx,cy),3,(0,0,255),-1)
            matches.append((cx, cy))

            for i in range(0,6):
                for_lane(coord[i],i+1,cx,cy)
            
            prada=[(10,35),(10,75),(10,105),(300,35),(300,70),(300,105)]

            for i in range(0,6):
                cv.putText(frame,"Speed lane" +str(i+1)+" : "+ str(speed[i]) + "km/hr",prada[i],cv.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)


    cv.putText(frame, "Cars count = "+str(cars), (10, 140), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),1)
    cv.putText(frame, "Truck count = "+str(truck), (10, 175), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255),1)
    # cv.resize(frame,(10,1500))
    
    cv.imshow("Frame", frame)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()



