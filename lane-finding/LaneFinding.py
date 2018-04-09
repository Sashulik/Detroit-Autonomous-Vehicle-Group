import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os.path

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform
from davg.lanefinding.Thresholds import Thresholds
from davg.lanefinding.DiagnosticScreen import DiagnosticScreen

def get_birdseye_binary_warped(img, undistort=True):
    ''' Convenience method.
    Undistorts an image (using previously determined globally accessible
    calibration data), warps it to the birdseye view, converting it to a uint8
    after warping, then applying the combined threshold.
    Optionally: skip the undistort step.
    '''
    global img_mgr, birdseye

    if (undistort):
        undistorted = img_mgr.undistort(img)
    else:
        undistorted = img

    # Warp to birds-eye view
    masked = birdseye.apply_cropping_mask(undistorted)
    warped = birdseye.warp(masked)

    # Apply the thresholds
    return thresholds.davg_thresh(warped)

img_mgr = ImgMgr()
birdseye = BirdsEyeTransform()
thresholds = Thresholds()
diagscreen = DiagnosticScreen()
