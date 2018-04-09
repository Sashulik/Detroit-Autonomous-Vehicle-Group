import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os.path

class ImgMgr:
    '''
    '''
    def __init__(self, dst_image_shape=None,
        calibration_file_base="camera_calibration_data",
        calibration_img_glob='RaspiWideAngleCalibrationImages/cali*.jpg'):

        self.default_width = 1296
        #self.default_height = 994
        self.default_height = 972

        # If a different shape is specified, use it
        if dst_image_shape is not None:
            self.default_width = int(dst_image_shape[0])
            self.default_height = int(dst_image_shape[1])

        # Internal values
        self.objpoints = None
        self.imgpoints = None

        self.mtx = None
        self.dist = None

        # If both calibration data files exist, just load the data
        if (os.path.exists(calibration_file_base + "_mtx.txt") and
            os.path.exists(calibration_file_base + "_dist.txt")):
            self.load_calibration_data()
        else:
            # Otherwise, perform the calibration and save the calibration data
            cal_images = glob.glob(calibration_img_glob)
            self.prepare_calibration_points(cal_images, display=False)
            self.perform_calibration()
            self.save_calibration_data()

        # Print out the calibration data just to be sure
        #print (self.mtx)
        #print ()
        #print (self.dist)

    def prepare_calibration_points(self, cal_images, display=False):

        objp = np.zeros((6*9,3), np.float32)
        objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d points in real world space
        self.imgpoints = [] # 2d points in image plane.

        # Step through the list and search for chessboard corners
        if display:
            plt.figure(figsize=(20,30))

        i = 1

        for fname in cal_images:

            print ("processing image {}".format(i))

            img = mpimg.imread(fname)
            img_sm = cv2.resize(img, (self.default_width, self.default_height))
            img = img_sm

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            altered = False

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

            # If found, add object points, image points
            if ret == True:
                self.objpoints.append(objp)
                self.imgpoints.append(corners)

                # Draw and display the corners
                if display:
                    img = cv2.drawChessboardCorners(img, (9,6), corners, ret)
                    altered = True

            if display:
                # show all images, even those that didn't have 9x6 corners
                ax = plt.subplot(7,3,i)
                ax.imshow(img)
                if (altered):
                    ax.set_title("9x6 FOUND")
                else:
                    ax.set_title("9x6 NOT FOUND")

            i += 1

        if display:
            plt.show()

        print ("Done processing calibration images.")

    def perform_calibration(self, img_size=None):

        if self.objpoints is None or len(self.objpoints) == 0:
            raise ValueError('objpoints is not initialized!')

        if self.imgpoints is None or len(self.imgpoints) == 0:
            raise ValueError('imgpoints is not initialized!')

        if img_size is None:
            img_size=(self.default_width, self.default_height)

        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, img_size, None, None)

        print ("Done calibrating camera.")

    def undistort(self, img, simple=False):

        img = cv2.resize(img, (self.default_width, self.default_height))

        if simple:
            return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

        h, w = img.shape[:2]
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (int(1.44*w),h))

        mapx,mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, newCameraMtx, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        return dst

    def save_calibration_data(self, file_name="camera_calibration_data"):

        np.savetxt(file_name + '_mtx.txt', self.mtx, delimiter=',')
        np.savetxt(file_name + '_dist.txt', self.dist, delimiter=',')

        print ("Camera calibration data saved.")

    def load_calibration_data(self, file_name="camera_calibration_data"):

        self.mtx = np.loadtxt(file_name + '_mtx.txt', delimiter=',')
        self.dist = np.loadtxt(file_name + '_dist.txt', delimiter=',')

        print ("Camera calibration data loaded.")
