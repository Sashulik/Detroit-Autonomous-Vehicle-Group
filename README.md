# Detroit-Autonomous-Vehicle-Group

## About us:
Welcome to the Detroit Autonomous Vehicle Group GitHub page where we are democratizing technology from Detroit, Michigan.

This site is dedicated to maintaining software/software related materials pertaining to projects worked on by the group. We are a group of technology enthusiasts who work on self-driving RC cars in order to apply concepts acquired from the Udacity Nano-Degree Program. In person meetings take place every Saturday in Ferndale, MI. For more information about the group please see links below.

## Links
1. Facebook Group Page - https://www.facebook.com/groups/416710545345864/ 
2. Instagram - https://www.instagram.com/detroitautonomousvehiclegroup/
3. Medium - https://medium.com/@DetroitAutonomousVehicleGroup
4. Meetup - https://www.meetup.com/Detroit-Autonomous-Vehicle-Meetup
5. Meeting Minutes - https://drive.google.com/drive/u/1/folders/0ByL8VeGwxrVoVk5BdDlVeWliRTQ
6. Parts Info - https://drive.google.com/drive/u/1/folders/0ByL8VeGwxrVoRmlKVHpMVUhsX28
7. Parts List Gen1Car - https://docs.google.com/spreadsheets/d/16NL_QVh4fbgr2phaQlHn6b5kDd-EuCylbFosMPntZtc/edit#gid=291899112
8. Resources - https://drive.google.com/drive/u/1/folders/0ByL8VeGwxrVoa3dkTlVENmpaUUk
9. Schematics Gen1Car - https://drive.google.com/drive/u/1/folders/0ByL8VeGwxrVoSjZkbk5TUTBWUFE
10. SDCar Project Folder - https://drive.google.com/drive/u/1/folders/0ByL8VeGwxrVoN1I3Mkg3cmRibmc
11. Share Folder - https://drive.google.com/drive/u/2/folders/0BwMKNnuQFE1MS0hOQnJUM2NZWHc
12. Slack - https://join.slack.com/t/davg/shared_invite/enQtMTk5NDQzNjE3NDYwLWE5MmY4MWU0NDM4OGUwMGNlOWMwMmRiNDc5NTRiNjEwYmEwYzIzZjUwMGE2NzE0Y2ZmZjQxNTZjMDBiNjc2MjM
13. Twitter - https://twitter.com/DAVGtech
14. YouTube - https://www.youtube.com/channel/UCF7-v2GGm9OvSbShzEHIauA/videos

-------------------------------------------------------------OPTIONAL-----------------------------------------------------------------

## Steps to add and activate conda environment on your Windows/linux/Mac OS

After you clone/unzip the repo, type the following commands (without the single quotes) in your terminal/command prompt to import and verify the conda environment. Make sure you install miniconda first on your PC. To do that please follow the steps in the link https://conda.io/docs/install/quick.html

1. Verify the conda install - 'conda --version'
2. Import environment.yml (replace environment with the environment name if it is different) - 'conda env create -f environment.yml'
3. To list all the environments available on your PC - 'conda info --envs' or 'conda env list'
4. Activate the DAVG environment:
  * linux/MAC OS X - 'source activate DAVG'
  * Windows - 'activate DAVG'

More information in the link https://conda.io/docs/using/envs.html

### Verify Arduino set-up

1. Connect the Arduino via USB.
2. On your PC (Windows), go to Device Manager, choose Ports (COM & LPT), then verify that the USB Serial Device (COM4) is present.
 If not, go to the Arduino web site and download and install the driver: (https://www.arduino.cc/)

### Raspberry PI WiFi (first time)

1. Connect the Raspberry PI to a display over HDMI and a Bluetooth mouse and keyboard.
2. Go to the network settings
   - Edit the computer name to 'DAVG-pi' (or whatever name you prefer, but DAVG-pi will be used in this document).
3. Reboot the Raspberry Pi to apply the settings.
4. Go to the WiFi settings and connect to the appropriate WiFi network.

### Connect to the Raspberry Pi via ssh

1. After the Raspberry Pi is connected to the wifi, it can be logged in over SSH.
2. Use your favorite SSH client (OpenSSH ssh client, PuTTY, etc.) to connect to 'DAVG-pi' or 'DAVG-pi.local' as necessary.
3. Log in (default credentials):

```
    Username: pi
    Password: raspberry
```
For example:
    ```ssh pi@DAVG-pi.local```

### Test the steering controls

1. On your PC, navigate to the "server-controller/test" folder of the DAVG repo. Run the rc_control_test.py test script:

```
    python rc_control_test.py
      
```
     
If only one com port is available, it will be automatically seleted. If there are more than one available, you will be prompted to select the appropriate one.


2. A pygame window should appear. In order to steer with the keyboard, the pygame window must be in the forefront. Only the arrow keys work. You should hear relays clicking when working properly.

#### For linux:
You must give permissions to the serial ports first. See instructions below:
 

Step 1: Determine com port (ls /dev/tty* with USB plugged in; then unplug the USB and re-run the code. This will show you which port is turning on and off and that is the port you need to connect to. Most likely it will be /dev/ttyACM0)


Step 2: Run the following command - "sudo chmod 666 /dev/ttyACM0" (ttyACM0 should be the com port or replace this with whatever your machine responds with)

#### For Mac:
In order to send the keyboard inputs to pygame, pygame_sdl2 must be used. Otherwise the keyboard input will be sent to the terminal window.

1. Go to https://github.com/renpy/pygame_sdl2
2. Clone the project onto your computer
3. Install the dependencies:

    brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_ttf
    
4. Build and install the pygame_sdl2 module from within the project directory:

   python setup.py install

### Test the video streaming

1. On the PC you want to view the vide on, run the `stream_server_test.py` script in "server-controller/tests" to start listening.
2. On the Raspberry Pi in the project directory, edit the stream_client.py file to use the IP address of the computer listening for the video connection.
3. Run the stream_client.py script to start sending the video.
4. !!!NOTE!!! Make sure your firewall is turned off. Otherwise will not be able to stream video. (Can make an exception in the firewall)


### Movidius Neural Compute Stick
1. Installation (Supported on RPi3 and Ubuntu 16.04): https://developer.movidius.com/start
2. YOLO NCS: https://github.com/gudovskiy/yoloNCS.git. Tiny YOLO object detection can be run on an image or webcam device.




