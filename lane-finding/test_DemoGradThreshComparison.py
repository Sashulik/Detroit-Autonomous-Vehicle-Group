import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform
from davg.lanefinding.Thresholds import Thresholds
from davg.lanefinding.DiagnosticScreen import DiagnosticScreen

img_mgr = ImgMgr()
birdseye = BirdsEyeTransform()

def demonstrate_gradient_threshold_comparison(fname,
                                    grad_ksize=27, mag_ksize=27, dir_ksize=15,
                                    gradx_min=30, gradx_max=120,
                                    grady_min=30, grady_max=120,
                                    mag_min=25, mag_max=120,
                                    dir_min=0.7, dir_max=np.pi/2):

    global img_mgr, birdseye

    img = mpimg.imread(fname)
    img = img_mgr.undistort(img)

    masked = birdseye.apply_cropping_mask(img)
    img = birdseye.warp(masked)

    gry = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gry_rgb = cv2.cvtColor(gry, cv2.COLOR_GRAY2RGB)

    gradx = Thresholds.abs_sobel_thresh(gry, orient='x', sobel_kernel=grad_ksize, thresh=(gradx_min, gradx_max))
    grady = Thresholds.abs_sobel_thresh(gry, orient='y', sobel_kernel=grad_ksize, thresh=(grady_min, grady_max))
    mag_binary = Thresholds.grad_magnitude_thresh(gry, sobel_kernel=mag_ksize, thresh=(mag_min, mag_max))
    dir_binary = Thresholds.grad_direction_thresh(gry, sobel_kernel=dir_ksize, thresh=(dir_min, dir_max))

    screen = DiagnosticScreen.compose_2x3_screen(diag1=img, diag2=gradx, diag3=grady,
                       diag4=gry_rgb, diag5=mag_binary, diag6=dir_binary,
                       title1="Original", title2="Sobel X", title3="Sobel Y",
                       title4="Grayscale", title5="Magnitude", title6="Direction")
    plt.figure(figsize=(12,4))
    plt.imshow(screen)
    plt.axis('off')
    plt.show()

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_gradient_threshold_comparison(test_images[0])
