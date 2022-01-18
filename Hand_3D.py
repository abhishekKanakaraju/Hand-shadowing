# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 02:14:34 2021

@author: abhis
"""
from ursina import *
import math
import cv2
import mediapipe as mp
import time
import HandGuesture as hg
import numpy as np

#Camera setting
cap = cv2.VideoCapture(2)
camx = 1280
camy = 720
cap.set(3,camx)
cap.set(4,camy)

#Create detector instance
detector = hg.handDetector(maxHands =1, detectionCon=0.7, trackCon=0.7)


#start app
app = Ursina()

#Output window specification  
window.title = 'My Game'                # The window title
window.borderless = False               # Show a bordertt
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = False      # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter
Text.size = 0.05
Text.default_resolution = 1080 * Text.size
info = Text(text="A powerful waterfall roaring on the mountains")
info.x = -0.5
info.y = 0.4
info.background = True
info.visible = False 

Smoothening = 7
Pervious_value = np.full((21,3),-9999, dtype='int')
Current_value = np.full((21,3),-9999, dtype='int')
Cam_value = np.zeros((21,3), dtype='int')

start = 0

def input(key):
    global start
    if held_keys['s']:
        start = 1
    if held_keys['q']:
        start = 0
    

def update():
    global Smoothening,Pervious_value,Current_value,Cam_value, Tips_3d, Bone_3d, start
    Tips_Cam = np.zeros((5,3), dtype='int')

    if start == 1:
        while True:
            Sucess, img = cap.read()
            img = detector.findHands(img)
            Righthand,Number_of_hands, lmlist = detector.findPosition(img)
            
            if len(lmlist)!=0:
                Tips_Cam = np.array(lmlist, dtype='int')[:, 1:4]
                
                if Current_value[1][1] == -9999:
                    Pervious_value[:,0] = -1*(Tips_Cam[:,0]-camx/2)
                    Pervious_value[:,1] =     camy/2-Tips_Cam[:,1]
                    Pervious_value[:,2] =     Tips_Cam[:,2]-400
                    
                Cam_value[:,0] = -1*(Tips_Cam[:,0]-camx/2)
                Cam_value[:,1] =     camy/2-Tips_Cam[:,1]
                Cam_value[:,2] =     Tips_Cam[:,2]-400
                
                Current_value[:,0] = (Pervious_value[:,0] + (Cam_value[:,0]-Pervious_value[:,0])/(Smoothening+5)).astype(int)
                Current_value[:,1] = (Pervious_value[:,1] + (Cam_value[:,1]-Pervious_value[:,1])/(Smoothening+5)).astype(int)                             
                Current_value[:,2] = (Pervious_value[:,2] + (Cam_value[:,2]-Pervious_value[:,2])/(Smoothening+10)).astype(int)
                
                for i in range(21):
                    Tips_3d[i].position = (1,1,0.5)*Current_value[i]

                
                f=0                
                for i in range (5):
                    for j in range (4):
                        p1 = j + 4*i*f
                        p2 = j + 4*i + 1
                        Bone_No = j + 4*i
                        
                        x,y,z = (np.array(Tips_3d[p1].position)-np.array(Tips_3d[p2].position))
              
                        r = math.dist(np.array(Tips_3d[p1].position),np.array(Tips_3d[p2].position))
                        theta = 90 - math.atan(y/abs(z))*180/math.pi
                        Phi =  (math.acos(x/r)*180/math.pi-90)
                        
                        
                        Bone_3d[Bone_No].position =  (1,1,1)*((np.array(Tips_3d[p1].position)+np.array(Tips_3d[p2].position))/2)
                        Bone_3d[Bone_No].scale_y = r
                        if z !=0:
                            if z > 0:
                                Bone_3d[Bone_No].rotation_x = theta
                            else:
                                Bone_3d[Bone_No].rotation_x = -1*theta
                        if r !=0:
                                Bone_3d[Bone_No].rotation_z = -1*Phi
                        f=1
                    f=0

                k=1
                for i in range (4):
                    p1 = 1 + i*4 + k
                    p2 = 5 + i*4
                    Bone_No = 20 + i
                    x,y,z = (np.array(Tips_3d[p1].position)-np.array(Tips_3d[p2].position))

                    r = math.dist(np.array(Tips_3d[p1].position),np.array(Tips_3d[p2].position))
                    theta = 90 - math.atan(y/abs(z))*180/math.pi
                    Phi =  (math.acos(x/r)*180/math.pi-90)
                    
                    
                    Bone_3d[Bone_No].position =  (1,1,1)*((np.array(Tips_3d[p1].position)+np.array(Tips_3d[p2].position))/2)
                    Bone_3d[Bone_No].scale_y = r
                    if z !=0:
                        if z > 0:
                            Bone_3d[Bone_No].rotation_x = theta
                        else:
                            Bone_3d[Bone_No].rotation_x = -1*theta
                    if r !=0:
                            Bone_3d[Bone_No].rotation_z = -1*Phi
                    k=0
                Pervious_value=Current_value
                break
            


Tips_3d =[]
Bone_3d =[]
for i in range(21):
    Tips_3d.append(Entity(model='sphere', color=color.yellow,scale=20, position=(0,0,0), rotation=(0,0,0)))
for i in range(24):
    Bone_3d.append(Entity(model='cube', color=color.brown,scale=10, position=(0,0,0), rotation=(0,0,0)))
    
# #coordinates:
# # verts = (Vec3(-200,0,0), Vec3(0,0,0))
# # lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=4), color=color.red)
# verts = (Vec3(0,0,0), Vec3(200,0,0))
# lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=8), color=color.red)
# # verts = (Vec3(0,-200,0), Vec3(0,0,0))
# # lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=4), color=color.green)
# verts = (Vec3(0,0,0), Vec3(0,200,0))
# lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=8), color=color.green)
# verts = (Vec3(0,0,-200), Vec3(0,0,0))
# lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=8), color=color.blue)
# # verts = (Vec3(0,0,0), Vec3(0,0,200))
# # lines = Entity(model=Mesh(vertices=verts, mode='line', thickness=4), color=color.blue)
# Entity(model=Grid(40, 40),scale=400,position = 0,rotation=(90,0,0))
# Entity(model=Grid(40, 40),scale=400,position = 0,rotation=(0,90,0))
# Entity(model=Grid(40, 40),scale=400,position = 0,rotation=(0,0 ,90))


EditorCamera()
app.run()
