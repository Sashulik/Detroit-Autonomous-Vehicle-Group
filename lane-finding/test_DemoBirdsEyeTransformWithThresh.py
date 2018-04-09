import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform
from davg.lanefinding.Thresholds import Thresholds

img_mgr = ImgMgr()
birdseye = BirdsEyeTransform()

def demonstrate_birdseye_transform_with_thresholds(imgs):

    global img_mgr, birdseye

    for fname in imgs:

        img = mpimg.imread(fname)
        undistorted = img_mgr.undistort(img)
        undistorted_masked = birdseye.apply_cropping_mask(undistorted)
        undistorted_warped = birdseye.warp(undistorted_masked)

        binary = Thresholds.combined_thresh(undistorted)
        binary_warped = birdseye.warp(binary)

        undistorted_warped_binary = Thresholds.combined_thresh(undistorted_warped)

        f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10, 10))
        f.set_tight_layout(True)

        ax1.imshow(undistorted)
        ax1.set_title('Undistorted', fontsize=15)
        ax1.add_patch(Polygon(birdseye.src, True, edgecolor='#ff0000', fill=False))

        ax2.imshow(undistorted_warped)
        ax2.set_title('Undistorted -> Warped', fontsize=15)
        ax2.add_patch(Polygon(birdseye.dst, True, edgecolor='#ff0000', fill=False))

        ax3.imshow(binary, cmap='gray')
        ax3.set_title('Undistorted -> Thresholded', fontsize=15)
        ax3.add_patch(Polygon(birdseye.src, True, edgecolor='#ff0000', fill=False))

        ax4.imshow(binary_warped, cmap='gray')
        ax4.set_title('Thresholded -> Warped', fontsize=15)
        ax4.add_patch(Polygon(birdseye.dst, True, edgecolor='#ff0000', fill=False))

        f.delaxes(ax5)

        ax6.imshow(undistorted_warped_binary, cmap='gray')
        ax6.set_title('Undistorted -> Warped -> Thresholded', fontsize=15)
        ax6.add_patch(Polygon(birdseye.dst, True, edgecolor='#ff0000', fill=False))

        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_birdseye_transform_with_thresholds([test_images[0]])
