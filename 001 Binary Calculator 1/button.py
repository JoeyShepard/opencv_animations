#https://medium.com/@enriqueav/how-to-create-video-animations-using-python-and-opencv-881b18e41397

import numpy as np
import cv2
import time
import sys
import math
import ctypes
import datetime

start_time=time.time()

#Video output
width = 1280
height = 720
FPS = 24
#seconds = 10
center_x=int(width/2)
center_y=int(height/2)


#Bottom info ribbon
ribbon_height=80
ribbon_slider_offset=0.1
ribbon_slider_X1=int(width*ribbon_slider_offset)
ribbon_slider_X2=int(width*(1.0-ribbon_slider_offset))
ribbon_slider_width=ribbon_slider_X2-ribbon_slider_X1

ribbon_frame=np.empty((ribbon_height,width,3),dtype=np.uint8)
cv2.rectangle(ribbon_frame,(0,0),(width,ribbon_height),(128,0,0),-1)
cv2.line(ribbon_frame,(ribbon_slider_X1,int(ribbon_height/2)),(ribbon_slider_X2,int(ribbon_height/2)),(0,255,255))

#Window
title="Animation"
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow(title,width,height+ribbon_height)

#Frame buffer
frame_buffer=np.empty((height+ribbon_height,width,3),dtype=np.uint8)

#Frame info
frame_time=int(1000/FPS)
frames=[]

def Accel75(index,max_index):
    if max_index in [0,1]:
        return 0
    if index>=(max_index-1):
        return 1
    temp_x=index/(max_index-1)
    return 2*temp_x-temp_x**2






#Animate frames here






frame_count=24

button_size=300
button_size2=int(button_size/2)
button_leg=50
leg_thickness=75
leg_thickness2=int(leg_thickness/2)
leg_color=(64,64,64)
button_radius=int(button_size2*0.7)

button_body=np.empty((button_size,button_size,3),dtype=np.uint8)
dst=np.empty((button_size,button_size,3),dtype=np.uint8)
#Square base
cv2.rectangle(button_body,(0,0),(button_size,button_size),(160,160,160),-1)
#Circle
cv2.circle(button_body,(button_size2,button_size2),button_radius,(0,0,0),-1)

for i in range(frame_count):
    frames.append(np.empty((height,width,3),dtype=np.uint8))
    index=len(frames)-1
    cv2.rectangle(frames[index],(0,0),(width,height),(255,255,255),-1)
    #Left leg
    cv2.line(frames[index],(center_x-button_size2+leg_thickness2,center_y-button_size2-button_leg),(center_x-button_size2+leg_thickness2,center_y+button_size2+button_leg),leg_color,leg_thickness)
    #Right leg
    cv2.line(frames[index],(center_x+button_size2-leg_thickness2,center_y-button_size2-button_leg),(center_x+button_size2-leg_thickness2,center_y+button_size2+button_leg),leg_color,leg_thickness)
    #Button body
    alpha=i/27
    beta=1-alpha
    cv2.addWeighted(frames[index][center_y-button_size2:center_y+button_size2,center_x-button_size2:center_x+button_size2],alpha,button_body,beta,0.0,dst)
    frames[index][center_y-button_size2:center_y+button_size2,center_x-button_size2:center_x+button_size2]=dst





#Animation stops here




def DrawFrame(index):
    frame_buffer[0:height,0:width]=frames[index]
    frame_buffer[height:height+ribbon_height,0:width]=ribbon_frame
    if len(frames) in [0,1]:
        pointer_X=ribbon_slider_X1
    else:
        pointer_X=int((ribbon_slider_width*index/(len(frames)-1))+ribbon_slider_X1)
    cv2.circle(frame_buffer,(pointer_X,int(height+(ribbon_height/2))),10,(0,255,255))
    #cv2.drawContours(frame_buffer, [triangle_cnt], 0, (0,255,0), -1)
    cv2.putText(frame_buffer,str(index+1)+"/"+str(len(frames)),(0,height+ribbon_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,255,255),1)
    cv2.imshow(title,frame_buffer)

running=True
frame_index=0
while True:
    if running==False:
        key=0
        key=cv2.waitKeyEx(0)
        if key in [-1,27]:
            sys.exit()
        elif key==32:
            if frame_index==len(frames):
                frame_index=0
            running=True
        elif key==2424832:   #Left key
            if frame_index>0:
                if frame_index==len(frames):
                    frame_index-=2
                else:
                    frame_index-=1
                DrawFrame(frame_index)
        elif key==2555904:   #Right key
            if frame_index<len(frames)-1:
                frame_index+=1
                DrawFrame(frame_index)
        elif key==13:       #Enter key
            #Save video
            answer=ctypes.windll.user32.MessageBoxW(0,"Export to video?", "Save video", 4)
            if answer==6:   #Yes
                current_time=datetime.datetime.now()
                file_name=str(current_time.year)+                   \
                        str(current_time.month).zfill(2)+           \
                        str(current_time.day).zfill(2)+"-"+         \
                        str(current_time.hour).zfill(2)+"."+        \
                        str(current_time.minute).zfill(2)+"."+      \
                        str(current_time.second).zfill(2)+".avi"

                fourcc = cv2.VideoWriter_fourcc(*'MP42')
                video = cv2.VideoWriter(file_name, fourcc, float(FPS), (width, height))
                for i,frame in enumerate(frames):
                    #DrawFrame(i)
                    #cv2.waitKey(1)  #Otherwise doesn't update screen
                    video.write(frame)
                video.release()
                ctypes.windll.user32.MessageBoxW(0,"Saved to "+file_name, "Save video", 1)

        else:
            #print(key)
            pass

    if running==True:
        DrawFrame(frame_index)
        frame_index+=1
        if frame_index==len(frames):
            running=False
        else:
            key=cv2.waitKey(frame_time)
            if key==-1:
                #Timer expired or window closed
                pass
            elif key==32:
                running=False

