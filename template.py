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
start_frame=0

def Accel75(index,max_index):
    if max_index in [0,1]:
        return 0
    if index>=(max_index-1):
        return 1
    temp_x=index/(max_index-1)
    return 2*temp_x-temp_x**2

def MakeTile(width,height,color=(255,255,255)):
    ret_mat=np.empty((height,width,3),dtype=np.uint8)
    cv2.rectangle(ret_mat,(0,0),(width,height),color,-1)
    return ret_mat

def GetTile(x,y,width,height,frame):
    ret_mat=MakeTile(width,height)
    np.copyto(ret_mat,frame[y:y+height,x:x+width])
    return ret_mat

def PutTile(tile,x,y,frame):
    height, width, channels = tile.shape
    #print(str(width)+"x"+str(height))
    #print("   "+str(x)+":"+str(x+width)+","+str(y)+":"+str(y+height))
    frame[y:y+height,x:x+width]=tile

def PutTileAlpha(tile,x,y,alpha,frame):
    if alpha>0.0:
        height, width, channels = tile.shape
        dst=np.empty((height,width,3),dtype=np.uint8)
        cv2.addWeighted(frame[y:y+height,x:x+width],1-alpha,tile,alpha,0.0,dst)
        frame[y:y+height,x:x+width]=dst

def new_frame():
    frames.append(np.empty((height,width,3),dtype=np.uint8))
    index=len(frames)-1
    cv2.rectangle(frames[index],(0,0),(width,height),(255,255,255),-1)
    return index


#Animate frames here


#Animation stops here


def DrawFrame(index):
    if index>=start_frame:
        frame_buffer[0:height,0:width]=frames[index]
        frame_buffer[height:height+ribbon_height,0:width]=ribbon_frame
        if len(frames) in [0,1]:
            pointer_X=ribbon_slider_X1
        else:
            pointer_X=int((ribbon_slider_width*index/(len(frames)-1))+ribbon_slider_X1)
        cv2.circle(frame_buffer,(pointer_X,int(height+(ribbon_height/2))),10,(0,255,255))
        #cv2.drawContours(frame_buffer, [triangle_cnt], 0, (0,255,0), -1)
        seconds=int(len(frames)/FPS)
        minutes=int(seconds/60)
        cv2.putText(frame_buffer,str(index+1)+"/"+str(len(frames))+" ("+str(minutes).zfill(2)+":"+str(seconds%60).zfill(2)+")",(ribbon_slider_X1,height+ribbon_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.75,(255,255,255),1)
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
        elif chr(key)>="0" and chr(key)<="9":
            if chr(key)=="0":
                frame_index=0
            else:
                frame_index=int(((key-ord("0"))/9*(len(frames)-1)))
            DrawFrame(frame_index)
        else:
            print(key)
            pass

    if running==True:
        DrawFrame(frame_index)
        frame_index+=1
        if frame_index==len(frames):
            running=False
        else:
            if frame_index>=start_frame:
                key=cv2.waitKey(frame_time)
                if key==-1:
                    #Timer expired or window closed
                    pass
                elif key==32:
                    running=False

