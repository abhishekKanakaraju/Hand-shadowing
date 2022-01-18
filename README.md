# Hand-shadowing
!!! 3D MODEL HAND TRACKING USING WEBCAM !!!!  


I have been working on a project for 5 days and I wanted to share my progress with you all.  
I wanted to develop a gesture controlled input for PC.  For the start I wanted to make a 3D hand, which shadows the movement of a human hand in real time.  I used python for the development in Spyder IDE  

How it works :
1. The program gets video input from webcam 
2. Using Mediapipe's hand tracking algorithm the program would track the coordinates (in pixels) 
3. Converting all the coordinates in pixels to 3d Coordinates 
4. Using Ursina, a game platform in python. 

The hand like model is developed and the 3d coordinates are mapped to joints and shown in the 3d screen.   

Python libraries: 
1. openCv : Get input from webcam 
2. ursina : Developing 3d module
3. math : Converting to Cartesian coordinates to spherical coordinates and calculations 
4. mediapipe: To track hand landmarks 
5. numpy : Matrix manipulation 
6. time : Finding FPS
