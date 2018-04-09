import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon

from davg.lanefinding.Thresholds import Thresholds
from davg.lanefinding.VidFrames import VidFrames
from davg.lanefinding.Pipeline import Pipeline

def demonstrate_image_processing_on_video_frames():

    pipeline = Pipeline()

    left_fit = []
    right_fit = []

    for img in VidFrames.extract_frames('video/stream1', start_time=22.0, interval=0.1, max_images=3):

        # Uncomment this code to further visualize some of the intermediate states
        # of the image processing pipeline.

        img = cv2.resize(img, (pipeline.img_mgr.default_width, pipeline.img_mgr.default_height))

        undistorted = pipeline.img_mgr.undistort(img)
        undistorted_masked = pipeline.birdseye.apply_cropping_mask(undistorted)
        undistorted_warped = pipeline.birdseye.warp(undistorted_masked)

        print (undistorted_warped.shape)

        binary = Thresholds.combined_thresh(undistorted)
        binary_warped = pipeline.birdseye.warp(binary)

        print (binary_warped.shape)

        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 8))
        f.set_tight_layout(True)

        ax1.imshow(undistorted)
        ax1.set_title('Undistorted', fontsize=15)
        ax1.add_patch(Polygon(pipeline.birdseye.src, True, edgecolor='#ff0000', fill=False))

        ax2.imshow(undistorted_warped)
        ax2.set_title('Undistorted -> Warped', fontsize=15)
        ax2.add_patch(Polygon(pipeline.birdseye.dst, True, edgecolor='#ff0000', fill=False))

        ax3.imshow(binary, cmap='gray')
        ax3.set_title('Undistorted -> Thresholded', fontsize=15)
        ax3.add_patch(Polygon(pipeline.birdseye.src, True, edgecolor='#ff0000', fill=False))

        ax4.imshow(binary_warped, cmap='gray')
        ax4.set_title('Thresholded -> Warped', fontsize=15)
        ax4.add_patch(Polygon(pipeline.birdseye.dst, True, edgecolor='#ff0000', fill=False))

        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

        if ((len(left_fit) == 0) or (len(right_fit) == 0)):
            left_fit, right_fit = pipeline.visualize_lanes_using_windows(img)
        else:
            left_fit, right_fit = pipeline.visualize_lines_from_fit(img, left_fit, right_fit)

# UNCOMMENT TO RUN
demonstrate_image_processing_on_video_frames()
