import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform

def demonstrate_center_shift():

    img_mgr = ImgMgr()
    birdseye = BirdsEyeTransform()

    #src_img = np.zeros((720, 1280), dtype=np.uint8)
    src_img = np.zeros((972, 1296), dtype=np.uint8)

    center_marker = np.int32([(src_img.shape[1]//2 - 1,0), (src_img.shape[1]//2 - 1,src_img.shape[0])])
    print("center_marker", center_marker)
    cv2.polylines(src_img, [center_marker], False, 255, 1)

    dst_img = birdseye.warp(src_img)

    dst_bottom_nonzeros = dst_img[dst_img.shape[0]-1].nonzero()
    print("dst_bottom_nonzeros", dst_bottom_nonzeros)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    f.set_tight_layout(True)

    birdseye.draw_src_on_img_gray(src_img, intensity=127, thickness=2)
    ax1.imshow(src_img, cmap='gray')

    birdseye.draw_dst_on_img_gray(dst_img, intensity=127, thickness=2)
    ax2.imshow(dst_img, cmap='gray')

    plt.show()

# UNCOMMENT TO RUN
demonstrate_center_shift()
