import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import os.path

from davg.lanefinding.Pipeline import Pipeline

def demonstrate_sliding_windows(data):

    pipeline = Pipeline()

    for idx in range(len(data)):

        # Read in a test image
        img = mpimg.imread(data[idx])

        print ("img.shape", img.shape)

        # Process it
        left_fit, right_fit = pipeline.visualize_lanes_using_windows(img)

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_sliding_windows(test_images[0:2])
