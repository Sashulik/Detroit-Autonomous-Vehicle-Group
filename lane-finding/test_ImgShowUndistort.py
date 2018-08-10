import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr

def demonstrate_image_undistort(img_mgr, imgs, scale=0.25, w_factor=1.0, h_factor=0.95):

    for fname in imgs:

        # Read in the image and undistort it
        img = mpimg.imread(fname)
        undistorted_simple = img_mgr.undistort(img, simple=True)

        undistorted_custom = img_mgr.undistort(img, scale=scale, w_factor=w_factor, h_factor=h_factor)

        # Display the original and undistorted images
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3))
        f.set_tight_layout(True)
        ax1.imshow(img)
        ax1.set_title('Original Image', fontsize=15)
        ax2.imshow(undistorted_simple)
        ax2.set_title('Undistorted Simple', fontsize=15)
        ax3.imshow(undistorted_custom)
        ax3.set_title('Undistorted Custom ({},{},{})'.format(scale, w_factor, h_factor), fontsize=15)
        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()

img_mgr = ImgMgr()
if img_mgr.calibrated is True:
    test_images = glob.glob('test_images_s1_1296x972/*.jpg')
    demonstrate_image_undistort(img_mgr, test_images[3:4], h_factor=0.92)

    test_images = glob.glob('data/tub_8_18-03-31/*.jpg')
    demonstrate_image_undistort(img_mgr, test_images[15:16], h_factor=0.92)

img_mgr = ImgMgr(dst_image_shape=[320,240], grid_shape=[8,6],
    calibration_file_base="elp170_calibration_data",
    calibration_img_glob='ELP170CalibrationImages/320x240/*.jpeg',
    display_checkerboard=True)
if img_mgr.calibrated is True:
    test_images = glob.glob('ELP170CalibrationImages/320x240/*.jpeg')
    demonstrate_image_undistort(img_mgr, test_images[0:21], h_factor=0.8)
