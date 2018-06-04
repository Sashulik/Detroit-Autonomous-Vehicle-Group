# How To Run Gen3Car 'Cyclops' (OpenMV Car)

## 1. Intro to control algorithms
https://www.youtube.com/watch?v=4Y7zG48uHRo <br />
Note: The same concepts apply to controlling anything, not just cars: Robots, airplanes, etc
PID was invented by a US Navy sailor tasked with autonomously steering boats. He derived the P, I and D terms by watching helmsman steer boats. His 1922 system was better than the sailors, but was not implemented due to resistance from sailors.

## 2. Install the IDE
2.1. Install the OpenMV IDE https://openmv.io/pages/download 

## 3. Grab the code from github and put it in the IDE: https://github.com/Sashulik/Detroit-Autonomous-Vehicle-Group/tree/master/02-OpenMV <br /> 
3.1. Download file "MVPRacer_Calibration_Red_rev02.py" <br /> 
Run it on the car (Ask someone for a quick how to) <br />
3.2. Modify the PID (look for !!! in the code) <br />
3.3. Run it and see how it goes <br />
3.4. Modify the code by the !!! to make it fail <br />
3.5. Modify the code so it succeeds but is different the the original values

## 4. Get the car to follow a different color line (see if can figure it out on your own or ask)

## 5. Optimize for faster lap time <br />
5.1. Switch to inside color <br />
5.2. Increase car speed <br />
5.3. Tune the PID
