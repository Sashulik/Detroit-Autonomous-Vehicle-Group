import numpy as np
import cv2

class Thresholds:

    @staticmethod
    def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
        '''
        Applies Sobel filter in the x or y direction, takes the absolute
        value and applies the specified threshold.
        '''

        # 1) Convert to grayscale if necessary
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        # 2) Take the derivative in x or y given orient = 'x' or 'y'
        if orient == 'x':
            sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
        else:
            sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

        # 3) Take the absolute value of the derivative or gradient
        abs_sobel = np.absolute(sobel)

        # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
        scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))

        # 5) Create a mask of 1's where the scaled gradient magnitude
        #    is > thresh_min and < thresh_max
        binary_output = np.zeros_like(scaled_sobel)
        binary_output[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1

        # 6) Return this mask as the binary_output image
        return binary_output

    @staticmethod
    def grad_magnitude_thresh(img, sobel_kernel=3, thresh=(0, 255)):
        '''
        Applies a Sobel in the x and y directions, computes the magnitude
        of the gradient, then applies the specified threshold
        '''

        # 1) Convert to grayscale if necessary
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        # 2) Take the gradient in x and y separately
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

        # 3) Calculate the magnitude
        abs_sobel = np.power(np.add(np.power(sobelx,2),np.power(sobely,2)), 0.5)

        # 4) Scale to 8-bit (0 - 255) and convert to type = np.uint8
        scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))

        # 5) Create a binary mask where magnitude thresholds are met
        binary_output = np.zeros_like(scaled_sobel)
        binary_output[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1

        # 6) Return this mask as the binary_output image
        return binary_output

    @staticmethod
    def grad_direction_thresh(img, sobel_kernel=3, thresh=(0, np.pi/2)):
        '''
        Applies a Sobel in the x and y directions, then computes the
        direction of the gradient and applies the specified threshold.
        '''

        # 1) Convert to grayscale if necessary
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        # 2) Take the gradient in x and y separately
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

        # 3) Take the absolute value of the x and y gradients
        abs_sobelx = np.absolute(sobelx)
        abs_sobely = np.absolute(sobely)

        # 4) Use np.arctan2(abs_sobely, abs_sobelx) to calculate the direction of the gradient
        dir_sobel = np.arctan2(abs_sobely, abs_sobelx)

        # 5) Create a binary mask where direction thresholds are met
        binary_output = np.zeros_like(dir_sobel)
        binary_output[(dir_sobel >= thresh[0]) & (dir_sobel <= thresh[1])] = 1

        # 6) Return this mask as the binary_output image
        return binary_output

    @staticmethod
    def color_thresh(img, cvt=cv2.COLOR_RGB2HLS, channel=2, thresh=(0,255)):
        ''' Selects a single color channel and applies a min/max threshold
            to the values, returning a binary mask for the pixels that meet
            the specified thresholds.
            By default, converts from RGB to HLS space and uses the Saturation
            channel.
        '''

        # 1) Convert to the specified colorspace
        if cvt != False:
            alt = cv2.cvtColor(img, cvt)
        else:
            alt = img

        # 2) Select the specified channel from the colorspace
        single_channel = alt[:,:,channel]

        # 3) Create a binary mask where the channel thresholds are met
        binary_output = np.zeros_like(single_channel)
        binary_output[(single_channel >= thresh[0]) & (single_channel <= thresh[1])] = 1

        # 4) Return this mask as the binary_output image
        return binary_output

    @staticmethod
    def davg_thresh(img, lumsat_thresh=(100, 255)):
        # Convert the RGB to useful formats
        gry = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)

        # Take the average of adding the L and S channels from the HLS encoding and then apply
        # the appropriate thresholds
        lumsat = (np.float32(hls[:,:,1]) + np.float32(hls[:,:,2]))//2
        lumsat_binary = np.zeros_like(gry)
        lumsat_binary[(lumsat >= lumsat_thresh[0]) & (lumsat <= lumsat_thresh[1])] = 1

        return np.uint8(lumsat_binary)

    @classmethod
    def combined_thresh(cls, img):
        return cls.davg_thresh(img)
