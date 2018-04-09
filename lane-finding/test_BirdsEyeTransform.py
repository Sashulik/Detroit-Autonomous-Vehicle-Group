import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform

img_mgr = ImgMgr()
birdseye = BirdsEyeTransform()

def demonstrate_birdseye_transform(imgs):

    global img_mgr, birdseye

    for fname in imgs:

        img = mpimg.imread(fname)
        undistorted = img_mgr.undistort(img, False)

        # Pre-process the image by masking out stuff
        undistorted_masked = birdseye.apply_cropping_mask(undistorted)

        undistorted_warped = birdseye.warp(undistorted_masked)

        f, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(16, 4))
        f.set_tight_layout(True)

        ax0.imshow(img)
        ax0.set_title('Original', fontsize=30)

        ax1.imshow(undistorted)
        ax1.set_title('Undistorted Masked', fontsize=30)
        ax1.add_patch(Polygon(birdseye.src, True, edgecolor='#ff0000', fill=False))

        ax2.imshow(undistorted_warped)
        ax2.set_title('Undistorted -> Warped', fontsize=30)
        ax2.add_patch(Polygon(birdseye.dst, True, edgecolor='#ff0000', fill=False))

        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_birdseye_transform(test_images[3:4])
