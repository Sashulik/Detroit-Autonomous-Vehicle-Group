# Detroit-Autonomous-Vehicle-Group

## Steps to add and activate conda environment on your wndows/linux/Mac OS

After you clone/unzip the repo, type the following commands (without the single quotes) in your terminal/command prompt to import and verify the conda environment. Make sure you install miniconda first on your PC. To do that please follow the steps in the link https://conda.io/docs/install/quick.html

1. Verify the conda install - 'conda --version'
2. Import environment.yml (replace environment with the environment name if it is different) - 'conda env create -f environment.yml'
3. To list all the environments available on your PC - 'conda info --envs' or 'conda env list'
4. Activate the DAVG environment:
  * linux/MAC OS X - 'source activate DAVG'
  * Windows - 'activate DAVG'
  
5. Connect the Arduino via USB.
6. On your PC (Windows), go to Device Manager, choose Ports (COM & LPT), then verify that the USB Serial Device (COM4) is present.
 If not, go to the Arduino web site and download and install the driver: (https://www.arduino.cc/)

7. On your PC, navigate to the "test" folder of the DAVG repo. Run the rc_control_test.py test script:
  python rc_control_test.py

If only one com port is available, it will be automatically seleted. If there are more than one available, you will be prompted to select the appropriate one.

8. A pygame window should appear. In order to steer with the keyboard, the pygame window must be in the forefront. Only the arrow keys work. You should hear relays clicking when working properly.

More information in the link https://conda.io/docs/using/envs.html
