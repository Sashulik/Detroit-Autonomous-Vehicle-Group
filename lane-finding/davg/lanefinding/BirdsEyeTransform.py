import numpy as np
import cv2

class BirdsEyeTransform():
    ''' Class to hold the birds-eye transform information.
    '''
    def __init__(self, w=1296, h=972):

        t_y = int(0.38 * h)
        b_y = int(0.73 * h)
        tl_x = int(0.4 * w)
        tr_x = int(0.6 * w)
        bl_x = int(0.2 * w)
        br_x = int(0.8 * w)

        d_t_y = int(h*0.2)
        d_b_y = int(h-1)
        #d_l_x = int(0.15 * w * 1.1)
        #d_r_x = int(0.85 * w * 0.9)
        d_l_x = int(0.25 * w)
        d_r_x = int(0.75 * w)

        # Reference source points for the perspective transform
        #                          TL             TR             BR             BL
        self.src = np.float32([(tl_x,t_y),    (tr_x,t_y),    (br_x,b_y),    (bl_x,b_y)])

        # Reference destination points for the perspective transform
        #                          TL             TR             BR             BL
        self.dst = np.float32([(d_l_x,d_t_y), (d_r_x,d_t_y), (d_r_x,d_b_y), (d_l_x,d_b_y)])

        # The transformation matrix for the perspective warp
        self.M = cv2.getPerspectiveTransform(self.src, self.dst)

        # Inverse transformation matrix for the perspective warp
        self.Minv = cv2.getPerspectiveTransform(self.dst, self.src)

        # Points defining the ROI from the src img
        img = np.ones((w, h), dtype=np.uint8)*255
        warped = cv2.warpPerspective(img, self.Minv, (img.shape[1], img.shape[0]))
        src_img = np.rint(warped).astype(np.uint8)

        src_img_nonzeros = src_img.nonzero()
        x_min = min(src_img_nonzeros[1])
        x_max = max(src_img_nonzeros[1])
        y_min = min(src_img_nonzeros[0])
        y_max = max(src_img_nonzeros[0])

        poly = []
        poly.append((x_min, y_max))
        poly.append((x_min, min(src_img_nonzeros[0][src_img_nonzeros[1] == x_min])))
        poly.append((min(src_img_nonzeros[1][src_img_nonzeros[0] == y_min]), y_min))
        poly.append((max(src_img_nonzeros[1][src_img_nonzeros[0] == y_min]), y_min))
        poly.append((x_max, min(src_img_nonzeros[0][src_img_nonzeros[1] == x_max])))
        poly.append((x_max, y_max))

        self.roi = np.float32(poly)

    def draw_src_on_img(self, img, color=(255,0,0), thickness=2):
        ''' Takes an RGB image and draws the src points (trapezoid) directly on
            the image.
        '''
        cv2.polylines(img, [self.src.astype(int)], True, color=color, thickness=thickness)

    def draw_dst_on_img(self, img, color=(255,0,0), thickness=2):
        ''' Takes an RGB image and draws the dst points (square) directly on
            the image.
        '''
        # Perspective transforms require float points, but polylines requires ints
        cv2.polylines(img, [self.dst.astype(int)], True, color=color, thickness=thickness)

    def draw_src_on_img_gray(self, img, intensity=255, thickness=2):
        ''' Takes a grayscale image and draws the src points (trapezoid) directly on
            the image.
        '''
        cv2.polylines(img, [self.src.astype(int)], True, color=intensity, thickness=thickness)

    def draw_dst_on_img_gray(self, img, intensity=255, thickness=2):
        ''' Takes a grayscale image and draws the dst points (square) directly on
            the image.
        '''
        # Perspective transforms require float points, but polylines requires ints
        cv2.polylines(img, [self.dst.astype(int)], True, color=intensity, thickness=thickness)

    def warp(self, img):
        ''' Performs the perspective warp from src to dst. Returns the result. '''

        warped = cv2.warpPerspective(img, self.M, (img.shape[1], img.shape[0]))

        # Round floats produced by warp to ints, then convert to unsigned 8-bit
        # https://carnd-forums.udacity.com/questions/38545026/black-images
        return np.rint(warped).astype(np.uint8)

    def unwarp(self, img):
        ''' Performs the perspective warp from dst back to src. Returns the result. '''
        warped = cv2.warpPerspective(img, self.Minv, (img.shape[1], img.shape[0]))
        return np.rint(warped).astype(np.uint8)

    def apply_cropping_mask(self, img):

        # get dimensions of mask
        bottom_right_pt = self.src[2]
        bottom_left_pt = self.src[3]
        offset = 0
        bottom_right_x = int(bottom_right_pt[0] + offset)
        bottom_left_x = int(bottom_left_pt[0] - offset)

        # apply mask
        #img[:,0:bottom_left_x,:] = img[:,bottom_left_x:bottom_left_x+1,:]
        #img[:,bottom_right_x:,:] = img[:,bottom_right_x:bottom_right_x+1,:]
        img[:,0:bottom_left_x,:] = 0
        img[:,bottom_right_x:,:] = 0

        return img
