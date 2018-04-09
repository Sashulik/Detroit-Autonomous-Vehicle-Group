import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr

def demonstrate_image_undistort(imgs, use_simple=False):

    img_mgr = ImgMgr()

    for fname in imgs:

        # Read in the image and undistort it
        img = mpimg.imread(fname)
        undistorted = img_mgr.undistort(img, use_simple)

        # Display the original and undistorted images
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
        f.set_tight_layout(True)
        ax1.imshow(img)
        ax1.set_title('Original Image', fontsize=15)
        ax2.imshow(undistorted)
        ax2.set_title('Undistorted Image', fontsize=15)
        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

test_images = glob.glob('test_images_s1_1296x972/*.jpg')

demonstrate_image_undistort(test_images[3:4])
