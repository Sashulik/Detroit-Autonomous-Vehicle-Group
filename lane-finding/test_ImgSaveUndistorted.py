import glob
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr

def demonstrate_undistort_save(test_images):

    img_mgr = ImgMgr()

    for i, fname in enumerate(test_images):
        img = mpimg.imread(fname)
        undistorted = img_mgr.undistort(img)
        mpimg.imsave("undistortion/undistorted_image{}.jpg".format(i), undistorted)

test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_undistort_save(test_images[3:4])
