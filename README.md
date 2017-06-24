# Detroit-Autonomous-Vehicle-Group

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
    For linux you must give permissions to the serial ports first. Insturctions below:
     Step 1: Determine com port (ls /dev/tty* with USB plugged in; then unplug the USB and re-run the code. This will show you which port is turning on and off and that is the port you need to connect to. Most likely it will be /dev/ttyACM0)
     Step 2: Run the following command - "sudo chmod 666 /dev/ttyACM0" (this should be the com port)
      
```

If only one com port is available, it will be automatically seleted. If there are more than one available, you will be prompted to select the appropriate one.

2. A pygame window should appear. In order to steer with the keyboard, the pygame window must be in the forefront. Only the arrow keys work. You should hear relays clicking when working properly.

### Test the video streaming

1. On the PC you want to view the vide on, run the `stream_server_test.py` script in "server-controller/tests" to start listening.
2. On the Raspberry Pi in the project directory, edit the stream_client.py file to use the IP address of the computer listening for the video connection.
3. Run the stream_client.py script to start sending the video. 



