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
    frame[y:y+height,x:x+width]=tile

def PutTileAlpha(tile,x,y,alpha,frame):
    if alpha>0.0:
        height, width, channels = tile.shape
        dst=np.empty((height,width,3),dtype=np.uint8)
        cv2.addWeighted(frame[y:y+height,x:x+width],1-alpha,tile,alpha,0.0,dst)
        frame[y:y+height,x:x+width]=dst




#Animate frames here






#frame_count=24

shift_reg_width=800
shift_reg_width2=int(shift_reg_width/2)
shift_reg_height=300
shift_reg_height2=int(shift_reg_height/2)
shift_reg_font_size=4.0
shift_reg_font_name=cv2.FONT_HERSHEY_DUPLEX
shift_reg_font_thickness=3
size=cv2.getTextSize("74HC595",shift_reg_font_name,shift_reg_font_size,shift_reg_font_thickness)
text_width=size[0][0]
text_height=size[0][1]

num_font_size=3.5
num_font_name=cv2.FONT_HERSHEY_DUPLEX
num_font_thickness=3
size=cv2.getTextSize("0",num_font_name,num_font_size,num_font_thickness)
num0_width=size[0][0]
size=cv2.getTextSize("1",num_font_name,num_font_size,num_font_thickness)
num1_width=size[0][0]
num_height=size[0][1]
num_height2=int(num_height/2)
#num0_color=(255,0,0)
num0_color=(255,0,192)
num1_color=(0,255,0)

num_speed=-40
shift_speed=-30

height_offset=100

pin_height=25
pin_thickness=25
pin_color=(128,128,128) #used for lines too
class TopPin:
    x=0
    color=(0,0,0)
    def __init__(self,x,color):
        self.x=x
        self.color=color
pin_x=[]
for i in range(8):
    pin_x.append(TopPin(center_x-shift_reg_width2+int((i+0.5)*shift_reg_width/8),pin_color))

data_line_y=center_y-int(shift_reg_height2/2)+height_offset

clock_line_y=center_y+height_offset
clock_line_color=pin_color

latch_line_y=center_y+int(shift_reg_height2/2)+height_offset
latch_line_color=pin_color

led_body_width2=30
led_body_height=int(led_body_width2*4/3)
led_base_width2=int(led_body_width2*4/3)
led_base_height=int(led_body_height*0.25)
led_pin_width=int(led_body_width2/4)
led_pin_width2=int(led_pin_width/2)
led_pin_height=led_body_width2+led_body_height
led_pin_offset_x=int(led_body_width2/2)
led_height=led_body_width2+led_body_height+led_base_height+led_pin_height
led_width=led_base_width2*2
led_width2=int(led_width/2)

led_base_color_off=(0,0,128)
led_body_color_off=(0,0,128)
led_base_color_on=(0,0,255)
led_body_color_on=(0,0,255)
led_pin_color=pin_color

def draw_led(x,y,frame,onoroff):
    if (onoroff):
        base_color=led_base_color_on
        body_color=led_body_color_on
    else:
        base_color=led_base_color_off
        body_color=led_body_color_off
    #Left leg
    cv2.rectangle(frame,(x-led_pin_offset_x-led_pin_width2,y+led_body_width2+led_body_height+led_base_height),(x-led_pin_offset_x+led_pin_width-led_pin_width2,y+led_body_width2+led_body_height+led_base_height+led_pin_height),led_pin_color,-1)
    #Right leg
    cv2.rectangle(frame,(x+led_pin_offset_x-led_pin_width2,y+led_body_width2+led_body_height+led_base_height),(x+led_pin_offset_x+led_pin_width-led_pin_width2,y+led_body_width2+led_body_height+led_base_height+led_pin_height),led_pin_color,-1)
    #Top curve
    cv2.circle(frame,(x,y+led_body_width2),led_body_width2,body_color,-1)
    #Body
    cv2.rectangle(frame,(x-led_body_width2,y+led_body_width2),(x+led_body_width2,y+led_body_width2+led_body_height),body_color,-1)
    #Base
    cv2.rectangle(frame,(x-led_base_width2,y+led_body_width2+led_body_height),(x+led_base_width2,y+led_body_width2+led_body_height+led_base_height),body_color,-1)

def draw_shift_reg(index):
    #8 data lines
    for j in range(8):
        #cv2.line(frames[index],(center_x-shift_reg_width2+int((j+0.5)*shift_reg_width/8),center_y-shift_reg_height2+height_offset),(center_x-shift_reg_width2+int((j+0.5)*shift_reg_width/8),center_y-shift_reg_height2+height_offset-pin_height),pin_color,pin_thickness)
        cv2.line(frames[index],(pin_x[j].x,center_y-shift_reg_height2+height_offset),(pin_x[j].x,center_y-shift_reg_height2+height_offset-pin_height),pin_x[j].color,pin_thickness)
    #Data line
    cv2.line(frames[index],(center_x,data_line_y),(width,data_line_y),pin_color,pin_thickness)
    #Clock line
    cv2.line(frames[index],(center_x,clock_line_y),(width,clock_line_y),clock_line_color,pin_thickness)
    #Latch line
    cv2.line(frames[index],(center_x,latch_line_y),(width,latch_line_y),latch_line_color,pin_thickness)
    #Body
    cv2.rectangle(frames[index],(center_x-shift_reg_width2,center_y-shift_reg_height2+height_offset),(center_x+shift_reg_width2,center_y+shift_reg_height2+height_offset),(64,64,64),-1)
    #Shift reg title
    cv2.putText(frames[index],"74HC595",(int(center_x-text_width/2),int(latch_line_y+text_height/2)),shift_reg_font_name,shift_reg_font_size,(192,192,192),shift_reg_font_thickness)

def new_frame_only():
    frames.append(np.empty((height,width,3),dtype=np.uint8))
    index=len(frames)-1
    cv2.rectangle(frames[index],(0,0),(width,height),(255,255,255),-1)
    return index

def new_frame():
    frames.append(np.empty((height,width,3),dtype=np.uint8))
    index=len(frames)-1
    cv2.rectangle(frames[index],(0,0),(width,height),(255,255,255),-1)
    draw_shift_reg(index)
    return index

pattern=[1,0,0,1,1,0,1,0]

class draw_num:
    x=None
    y=None
    width=0
    text=""
    color=None
    visible=False

    def __init__(self,x,y,width2,text,color,visible):
        self.x=x
        self.y=y
        self.width2=width2
        self.text=text
        self.color=color
        self.visible=visible

    def draw(self,index,offset_x=0):
        if self.visible:
            cv2.putText(frames[index],self.text,(self.x-self.width2+offset_x,self.y),num_font_name,num_font_size,self.color,num_font_thickness)
            #cv2.line(frames[index],(self.x-self.width2+offset_x,0),(self.x-self.width2+offset_x,width),(0,0,0),1)
            #cv2.line(frames[index],(self.x+self.width2+offset_x,0),(self.x+self.width2+offset_x,width),(0,0,0),1)

#Pause 2 seconds
for i in range(FPS*2):
    new_frame()
    pass


num_list=[]

#Shift 8 bits in
for i in range(8):
    if pattern[i]==0:
        num_color=num0_color
        num_width=num0_width
    else:
        num_color=num1_color
        num_width=num1_width
    num_width2=int(num_width/2)

    #Animate numbers
    #for j in range(width,center_x+shift_reg_width2-num_width2,num_speed):
    for j in range(width,center_x+shift_reg_width2,num_speed):
        index=new_frame()
        for num in num_list:
            num.draw(index)
        cv2.putText(frames[index],str(pattern[i]),(j,data_line_y+num_height2),num_font_name,num_font_size,num_color,num_font_thickness)
        #cv2.line(frames[index],(j,0),(j,height),(0,0,0),1)

    #Add to queue
    num_list.append(draw_num(center_x+shift_reg_width2+int(shift_reg_width/16),data_line_y+num_height2,num_width2,str(pattern[i]),num_color,True))

    #Pause on first digit
    if i==0:
        for k in range(int(FPS*1)):
            index=new_frame()
            for num in num_list:
                num.draw(index)
        #Pause on data high
        clock_line_color=(0,255,0)
        for k in range(int(FPS*1)):
            index=new_frame()
            for num in num_list:
                num.draw(index)

    #Shift queue
    clock_line_color=(0,255,0)
    for k in range(0,-int(shift_reg_width/8),shift_speed):
        index=new_frame()
        for num in num_list:
            num.draw(index,k)
    clock_line_color=pin_color
    for k in range(len(num_list)):
        num_list[k].x-=int(shift_reg_width/8)
    index=new_frame()
    for num in num_list:
        num.draw(index)

    #Pause on first digit with clock down
    if i==0:
        for k in range(int(FPS*1)):
            index=new_frame()
            for num in num_list:
                num.draw(index)

#Pause
for i in range(int(FPS*0.5)):
    index=new_frame()
    for num in num_list:
        num.draw(index)

#Pulse latch line
latch_line_color=(0,255,0)
for i in range(8):
    pin_x[i].color=num_list[i].color
for i in range(1*FPS):
    index=new_frame()
    for num in num_list:
        num.draw(index)
latch_line_color=pin_color
for i in range(1*FPS):
    index=new_frame()
    for num in num_list:
        num.draw(index)

#start_frame=index

led_off_mat=MakeTile(led_width,led_height)
draw_led(led_width2,0,led_off_mat,False)
led_on_mat=MakeTile(led_width,led_height)
draw_led(led_width2,0,led_on_mat,True)

#Fade in LEDs
for i in np.arange(0.0,1.0,0.02):
    index=new_frame()
    for num in num_list:
        num.draw(index)
    for j in range(8):
        PutTileAlpha(led_off_mat,pin_x[j].x-led_width2,75,i,frames[index])

#Construct wires to LEDs
wire_list=[]
for i in range(8):
    wire_list.append(((pin_x[i].x,center_y-shift_reg_height2+height_offset-pin_height), #0=(x,y) 1
        (pin_x[i].x-led_pin_offset_x,75+led_height)))                                   #1=(x,y) 2


#Extend wires to LEDs
wire_frames=int(FPS*0.5)
for i in range(wire_frames):
    index=new_frame_only()
    for j in wire_list:
        x_diff=int((j[1][0]-j[0][0])*(1-i/wire_frames))
        y_diff=int((j[1][1]-j[0][1])*(1-i/wire_frames))
        cv2.line(frames[index],(j[1][0]-x_diff,j[1][1]-y_diff),j[0],pin_color,led_pin_width2)
    draw_shift_reg(index)
    for num in num_list:
        num.draw(index)
    for j in range(8):
        PutTileAlpha(led_off_mat,pin_x[j].x-led_width2,75,1.0,frames[index])

#Hold on wires
wire_frames=int(FPS*1)
for i in range(wire_frames):
    index=new_frame_only()
    for j in wire_list:
        cv2.line(frames[index],(j[1][0],j[1][1]),j[0],pin_color,led_pin_width2)
    draw_shift_reg(index)
    for num in num_list:
        num.draw(index)
    for j in range(8):
        PutTileAlpha(led_off_mat,pin_x[j].x-led_width2,75,1.0,frames[index])

#Light up LEDs
lit_frames=int(FPS*2)
for i in range(lit_frames):
    index=new_frame_only()
    for j in wire_list:
        cv2.line(frames[index],(j[1][0],j[1][1]),j[0],pin_color,led_pin_width2)
    draw_shift_reg(index)
    for num in num_list:
        num.draw(index)
    for j in range(8):
        if pattern[j]==1:
            PutTileAlpha(led_on_mat,pin_x[j].x-led_width2,75,1.0,frames[index])
        else:
            PutTileAlpha(led_off_mat,pin_x[j].x-led_width2,75,1.0,frames[index])










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

