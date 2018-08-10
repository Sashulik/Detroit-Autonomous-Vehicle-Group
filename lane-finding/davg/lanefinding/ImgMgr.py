import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os.path

class ImgMgr:
    '''
    '''
    def __init__(self, calibrate_on_missing=False, dst_image_shape=None, grid_shape=None,
        calibration_file_base="camera_calibration_data",
        calibration_img_glob='RaspiWideAngleCalibrationImages/cali*.jpg',
        display_checkerboard=False):

        self.default_width = 1296
        #self.default_height = 994
        self.default_height = 972

        self.grid_width = 9
        self.grid_height = 6

        # If a different shape is specified, use it
        if dst_image_shape is not None:
            self.default_width = int(dst_image_shape[0])
            self.default_height = int(dst_image_shape[1])

        if grid_shape is not None:
            self.grid_width = int(grid_shape[0])
            self.grid_height = int(grid_shape[1])

        # Internal values
        self.objpoints = None
        self.imgpoints = None

        self.mtx = None
        self.dist = None
        self.calibrated = False

        # If both calibration data files exist, just load the data
        if (os.path.exists(calibration_file_base + "_mtx.txt") and
            os.path.exists(calibration_file_base + "_dist.txt")):
            self.load_calibration_data(file_name=calibration_file_base)

        else:

            if calibrate_on_missing is False:
                print ("WARN: Calibration configuration not loaded.")
                return

            # Otherwise, perform the calibration and save the calibration data
            cal_images = glob.glob(calibration_img_glob)
            if cal_images is None:
                print ("WARN: Calibration images could not be loaded.")
                return

            self.prepare_calibration_points(cal_images, display=display_checkerboard)
            self.perform_calibration()
            self.save_calibration_data(file_name=calibration_file_base)

        if self.mtx is not None and self.dist is not None:
            self.calibrated = True

        # Print out the calibration data just to be sure
        #print (self.mtx)
        #print ()
        #print (self.dist)

    def prepare_calibration_points(self, cal_images, display=False):

        objp = np.zeros((self.grid_width*self.grid_height,3), np.float32)
        objp[:,:2] = np.mgrid[0:self.grid_width,0:self.grid_height].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d points in real world space
        self.imgpoints = [] # 2d points in image plane.

        # Step through the list and search for chessboard corners
        if display:
            plt.figure(figsize=(6,12))
            #plt.tight_layout()

        i = 1

        for fname in cal_images:

            print ("INFO: Processing image {}".format(i))

            img = mpimg.imread(fname)
            img_sm = cv2.resize(img, (self.default_width, self.default_height))
            img = img_sm

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            altered = False

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (self.grid_width,self.grid_height),None)

            # If found, add object points, image points
            if ret == True:
                self.objpoints.append(objp)
                self.imgpoints.append(corners)

                # Draw and display the corners
                if display:
                    img = cv2.drawChessboardCorners(img, (self.grid_width,self.grid_height), corners, ret)
                    altered = True

            if display:
                # show all images, even those that didn't have grid_width x grid_height corners
                ax = plt.subplot(7,3,i)
                ax.imshow(img)
                if (altered):
                    ax.set_title("{}x{} FOUND".format(self.grid_width, self.grid_height))
                else:
                    ax.set_title("{}x{} NOT FOUND".format(self.grid_width, self.grid_height))

            i += 1

        if display:
            plt.show()

        print ("INFO: Done processing calibration images.")

    def perform_calibration(self, img_size=None):

        if self.objpoints is None or len(self.objpoints) == 0:
            raise ValueError('WARN: objpoints is not initialized!')

        if self.imgpoints is None or len(self.imgpoints) == 0:
            raise ValueError('WARN: imgpoints is not initialized!')

        if img_size is None:
            img_size=(self.default_width, self.default_height)

        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, img_size, None, None)

        print ("INFO: Done calibrating camera.")

    def undistort(self, img, simple=False, scale=0.25, w_factor=1.0, h_factor=1.0):

        img = cv2.resize(img, (self.default_width, self.default_height))

        if simple:
            return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)

        h, w = img.shape[:2]
        newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx,
            self.dist, (w,h), scale, (int(w_factor*w), int(h_factor*h)), True)

        mapx,mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, newCameraMtx, (w,h), 5)
        return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    def save_calibration_data(self, file_name="camera_calibration_data"):

        np.savetxt(file_name + '_mtx.txt', self.mtx, delimiter=',')
        np.savetxt(file_name + '_dist.txt', self.dist, delimiter=',')

        print ("INFO: Camera calibration data saved for {}.".format(file_name))

    def load_calibration_data(self, file_name="camera_calibration_data"):

        self.mtx = np.loadtxt(file_name + '_mtx.txt', delimiter=',')
        self.dist = np.loadtxt(file_name + '_dist.txt', delimiter=',')

        print ("INFO: Camera calibration data loaded for {}.".format(file_name))
