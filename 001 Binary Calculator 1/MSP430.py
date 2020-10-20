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




MSP430_width=400
MSP430_width2=int(MSP430_width/2)
MSP430_height=600
MSP430_color=(64,64,64)
MSP430_top=int((height-MSP430_height)/2)
MSP430_10TH=int(MSP430_height/10)
MSP430_text_color=(192,192,192)

pin_length=40
pin_color=(128,128,128)
pin_thickness=20
pins_left=["VCC","P1.0","P1.1","P1.2","P1.3","P1.4","P1.5","P2.0","P2.1","P2.2"]
pins_right=["VSS","P2.6","P2.7","TEST","RST","P1.7","P1.6","P2.5","P2.4","P2.3"]
pin_font_name=cv2.FONT_HERSHEY_DUPLEX
pin_font_size=1.5
pin_font_thickness=2
pin_font_spacing=10

pin_colors_left=[]
pin_colors_right=[]

button_size=50
button_size2=int(button_size/2)
button_circle=int(button_size*0.7)
button_circle2=int(button_circle/2)
button_offset_x=200
button_leg_thickness=5

button_base_color=(160,160,160)
button_circle_color=(0,0,0)

for i in range(10):
    pin_colors_left.append(pin_color)
    pin_colors_right.append(pin_color)

def draw_frame(index):
    for i in np.arange(0.5,10.5):
        #Left side pins
        cv2.line(frames[index],(center_x-MSP430_width2,MSP430_top+int(i*MSP430_10TH)),(center_x-MSP430_width2-pin_length,MSP430_top+int(i*MSP430_10TH)),pin_colors_left[int(i)],pin_thickness)
        #Right side pins
        cv2.line(frames[index],(center_x+MSP430_width2,MSP430_top+int(i*MSP430_10TH)),(center_x+MSP430_width2+pin_length,MSP430_top+int(i*MSP430_10TH)),pin_colors_right[int(i)],pin_thickness)
    #Body of MSP430
    cv2.rectangle(frames[index],(center_x-MSP430_width2,MSP430_top),(center_x+MSP430_width2,MSP430_top+MSP430_height),MSP430_color,-1)
    #Labels
    for i in np.arange(0.5,10.5):
        #Left side labels
        size=cv2.getTextSize(pins_left[int(i)],pin_font_name,pin_font_size,pin_font_thickness)
        text_width=size[0][0]
        text_height=size[0][1]
        cv2.putText(frames[index],pins_left[int(i)],(center_x-MSP430_width2+pin_font_spacing,MSP430_top+int(i*MSP430_10TH)+int(text_height/2)),pin_font_name,pin_font_size,pin_colors_left[int(i)],pin_font_thickness)
        #Right side labels
        size=cv2.getTextSize(pins_right[int(i)],pin_font_name,pin_font_size,pin_font_thickness)
        text_width=size[0][0]
        text_height=size[0][1]
        cv2.putText(frames[index],pins_right[int(i)],(center_x+MSP430_width2-pin_font_spacing-text_width,MSP430_top+int(i*MSP430_10TH)+int(text_height/2)),pin_font_name,pin_font_size,pin_colors_right[int(i)],pin_font_thickness)
    #MSP430G2553
    size=cv2.getTextSize("MSP430G2553",pin_font_name,pin_font_size,pin_font_thickness)
    text_width=size[0][0]
    text_height=size[0][1]+4
    title_tile=MakeTile(text_width,text_height,MSP430_color)
    cv2.putText(title_tile,"MSP430G2553",(0,text_height-3),pin_font_name,pin_font_size,MSP430_text_color,pin_font_thickness)
    temp_tile=cv2.rotate(title_tile,cv2.ROTATE_90_CLOCKWISE)

    PutTile(temp_tile,center_x-int(text_height/2),MSP430_top+int(MSP430_height/2)-int(text_width/2),frames[index])

def draw_button(x,y,frame):
    cv2.line(frame,(center_x,y),(x,y),pin_color,button_leg_thickness)
    cv2.rectangle(frame,(x-button_size2,y-button_size2),(x+button_size2,y+button_size2),button_base_color,-1)
    cv2.circle(frame,(x,y),button_circle2,button_circle_color,-1)


#Plain frame
for i in range(FPS*1):
    index=new_frame()
    draw_frame(index)

#Voltage pins
pin_colors_left[0]=(80,80,255)
pin_colors_right[0]=(80,80,255)
for i in range(FPS*1):
    index=new_frame()
    draw_frame(index)

#Programming pins
pin_colors_right[3]=(255,160,0)
pin_colors_right[4]=(255,160,0)
for i in range(FPS*1):
    index=new_frame()
    draw_frame(index)

button_list=[]

#Color port 2
for i in [1,2,7,8,9]:
    pin_colors_right[i]=(80,224,0)
    button_list.append((center_x+MSP430_width2+button_offset_x,MSP430_top+int((i+0.5)*MSP430_10TH)))
for i in [7,8,9]:
    pin_colors_left[i]=(80,224,0)
    button_list.append((center_x-MSP430_width2-button_offset_x,MSP430_top+int((i+0.5)*MSP430_10TH)))

#Port 2 without buttons
for i in range(FPS*1):
    index=new_frame()
    draw_frame(index)

#Render buttons to buffer to make transparent
button_buffer=MakeTile(width,height)
for j in button_list:
    draw_button(j[0],j[1],button_buffer)

#Port 2 with buttons fading in
for i in range(FPS*1):
    index=new_frame()
    PutTileAlpha(button_buffer,0,0,i/FPS,frames[index])
    draw_frame(index)

#Port 2 with buttons
for i in range(FPS*1):
    index=new_frame()
    for j in button_list:
        draw_button(j[0],j[1],frames[index])
    draw_frame(index)

#Color port 1
for i in [5,6]:
    pin_colors_right[i]=(255,96,192)
for i in [1,2,3,4,5,6]:
    pin_colors_left[i]=(255,96,192)

#Port 1
for i in range(FPS*1):
    index=new_frame()
    for j in button_list:
        draw_button(j[0],j[1],frames[index])
    draw_frame(index)

#SPI pins only
for i in [1,2,3,4,5]:
    pin_colors_left[i]=pin_color
for i in range(FPS*1):
    index=new_frame()
    for j in button_list:
        draw_button(j[0],j[1],frames[index])
    draw_frame(index)

#Minus sign
pin_colors_left[5]=(255,96,192)
for i in range(FPS*1):
    index=new_frame()
    for j in button_list:
        draw_button(j[0],j[1],frames[index])
    draw_frame(index)

#Zoom in
# zoom_buffer=GetTile(500,500,200,200,frames[index])
#
# for i in range(FPS*1):
#     index=new_frame()
#     for j in button_list:
#         draw_button(j[0],j[1],frames[index])
#     draw_frame(index)
#     temp_buffer=cv2.resize(zoom_buffer,(int((1+i/FPS)*200),int((1+i/FPS)*200)))
#     PutTile(temp_buffer,500,200,frames[index])





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

