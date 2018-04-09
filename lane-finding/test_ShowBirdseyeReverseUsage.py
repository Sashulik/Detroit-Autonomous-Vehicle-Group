import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Polygon

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform

def demonstrate_birdseye_reverse_usage():

    img_mgr = ImgMgr()
    birdseye = BirdsEyeTransform()

    # Create a blank white image that represents the result of a birdeye warp
    dst_img = np.ones((720, 1280), dtype=np.uint8)*255

    # "Unwarp" the image to the aleged source
    src_img = birdseye.unwarp(dst_img)

    # Determine the bounding box of the non-zero values from the unwarped image
    src_img_nonzeros = src_img.nonzero()
    x_min = min(src_img_nonzeros[1])
    x_max = max(src_img_nonzeros[1])
    y_min = min(src_img_nonzeros[0])
    y_max = max(src_img_nonzeros[0])

    #print("src_img_nonzeros", src_img_nonzeros)

    print("{} {} {} {}".format(x_min, x_max, y_min, y_max))

    # Get the polygon points that define the "unwarped" birdseye view
    poly = []
    poly.append((x_min, y_max))
    poly.append((x_min, min(src_img_nonzeros[0][src_img_nonzeros[1] == x_min])))
    poly.append((min(src_img_nonzeros[1][src_img_nonzeros[0] == y_min]), y_min))
    poly.append((max(src_img_nonzeros[1][src_img_nonzeros[0] == y_min]), y_min))
    poly.append((x_max, min(src_img_nonzeros[0][src_img_nonzeros[1] == x_max])))
    poly.append((x_max, y_max))
    print("poly", poly)

    # Display the results
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    f.set_tight_layout(True)

    # Draw the simulated birdseye
    birdseye.draw_dst_on_img_gray(dst_img, intensity=127, thickness=2)
    ax1.imshow(dst_img, cmap='gray')

    # Draw the simulated original source image with the birdseye src coords and
    # the polygon defining how the original was unwarped
    birdseye.draw_src_on_img_gray(src_img, intensity=127, thickness=2)
    ax2.imshow(src_img, cmap='gray')
    ax2.add_patch(Polygon(np.float32(poly), True, edgecolor='#ff0000', fill=False))

    plt.show()

# UNCOMMENT TO RUN
demonstrate_birdseye_reverse_usage()
