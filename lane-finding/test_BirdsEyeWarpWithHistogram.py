import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon

from davg.lanefinding.Pipeline import Pipeline

pipeline = Pipeline()

def demonstrate_birdseye_warp_with_histogram(imgs):

    global pipeline

    for fname in imgs:

        # Read in a test image
        img = mpimg.imread(fname)

        # Undistort, threshold, warp
        binary_warped = pipeline.get_birdseye_binary_warped(img)

        print ("binary_warped.shape {}".format(binary_warped.shape))

        # Count up occurances of 1-values of pixels for lower half of image
        histogram = np.sum(binary_warped[int(binary_warped.shape[0]*0.75):,:], axis=0)

        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255

        f, (ax1, ax2) = plt.subplots(1,2)
        f.set_tight_layout(True)

        ax1.imshow(binary_warped, cmap='gray')
        ax1.set_title("Birdseye Threshold")

        # highlight region that is being considered for histogram
        ax1.add_patch(Polygon([(0, binary_warped.shape[0]),
                               (0, int(binary_warped.shape[0]*0.75)),
                               (binary_warped.shape[1]-1, int(binary_warped.shape[0]*0.75)),
                               (binary_warped.shape[1]-1, binary_warped.shape[0])], True, alpha=0.4, color='#eeeeee'))

        ax2.plot(histogram, color='#ff0000')
        ax2.set_title("Histogram")

        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_birdseye_warp_with_histogram(test_images[0:1])
