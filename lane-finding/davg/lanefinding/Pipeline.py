import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from davg.lanefinding.ImgMgr import ImgMgr
from davg.lanefinding.BirdsEyeTransform import BirdsEyeTransform
from davg.lanefinding.Thresholds import Thresholds
from davg.lanefinding.LaneMath import LaneMath
from davg.lanefinding.Prediction import Prediction
from davg.lanefinding.Line import Line
from davg.lanefinding.DiagnosticScreen import DiagnosticScreen

class Pipeline():

    def __init__(self):
        self.img_mgr = ImgMgr()
        self.birdseye = BirdsEyeTransform()
        pass

    def get_birdseye_binary_warped(self, img, undistort=True):
        ''' Convenience method.
        Undistorts an image (using previously determined globally accessible
        calibration data), warps it to the birdseye view, converting it to a uint8
        after warping, then applying the combined threshold.
        Optionally: skip the undistort step.
        '''

        if (undistort):
            undistorted = self.img_mgr.undistort(img)
        else:
            undistorted = img

        # Warp to birds-eye view
        masked = self.birdseye.apply_cropping_mask(undistorted)
        warped = self.birdseye.warp(masked)

        # Apply the thresholds
        return Thresholds.davg_thresh(warped)

    def find_lane_lines_using_windows(self, binary_warped):

        # This code was taken from the Udacity 'Finding the Lines' section of the
        # Advanced Lane Finding lesson
        # https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/2b62a1c3-e151-4a0e-b6b6-e424fa46ceab/lessons/40ec78ee-fb7c-4b53-94a8-028c5c60b858/concepts/c41a4b6b-9e57-44e6-9df9-7e4e74a1a49a

        # Assuming you have created a warped binary image called "binary_warped"
        # Take a histogram of the bottom half of the image
        histogram = np.sum(binary_warped[int(binary_warped.shape[0]*0.75):,:], axis=0)

        # Create an output image to draw on and visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255

        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]//2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # Choose the number of sliding windows
        nwindows = 15

        # Set height of windows
        window_height = np.int(binary_warped.shape[0]//nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated for each window
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Set the width of the windows +/- margin
        margin = 100

        # Set minimum number of pixels found to recenter window
        minpix = 40

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):

            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height  # bottom of image - (next window count * window height)
            win_y_high = binary_warped.shape[0] - window*window_height     # bottom of image - (curr window count * window height)
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin

            # Draw the windows on the visualization image
            cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 2)
            cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2)

            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)

            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        # Color the non-zero values that are part of the lanes
        out_img[lefty, leftx] = [255, 0, 0]
        out_img[righty, rightx] = [0, 0, 255]

        # Fit a second order polynomial to each
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        return left_fit, right_fit, out_img

    def visualize_lanes_using_windows(self, img):

        # Undistort, threshold, warp
        binary_warped = self.get_birdseye_binary_warped(img)

        left_fit, right_fit, out_img = self.find_lane_lines_using_windows(binary_warped)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )
        left_fitx = LaneMath.eval_poly_at(ploty, left_fit)
        right_fitx = LaneMath.eval_poly_at(ploty, right_fit)

        # Visualize the lines
        plt.figure()
        plt.imshow(out_img)
        plt.plot(left_fitx, ploty, color='yellow')
        plt.plot(right_fitx, ploty, color='yellow')
        plt.xlim(0, 1296)
        plt.ylim(972, 0)
        plt.show()

        left_curverad_px, right_curverad_px = LaneMath.get_curve_radii_in_pixels(ploty, left_fit, right_fit)
        print("left curve {:.3f} px, right curve {:.3f} px".format(left_curverad_px, right_curverad_px))

        left_curverad_m, right_curverad_m = LaneMath.get_curve_radii_in_meters(ploty, left_fitx, right_fitx)
        print("left curve {:.3f} m, right curve {:.3f} m".format(left_curverad_m, right_curverad_m))

        lane_center_px = LaneMath.get_lane_center_in_pixels(ploty, left_fit, right_fit)
        lane_offset_m = LaneMath.get_lane_offset_in_meters(binary_warped.shape[1], lane_center_px)
        print("lane center {:.3f} px, offset from lane center {:.3f} m".format(lane_center_px, lane_offset_m))

        return left_fit, right_fit

    def find_lane_lines_from_fit(self, binary_warped, left_fit, right_fit):

        # Create an image to draw on and an image to show the selection window
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255

        # Assume you now have a new warped binary image
        # from the next frame of video (also called "binary_warped")
        # It's now much easier to find line pixels!
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Set the width of the windows +/- margin
        margin = 100

        # Determine the location of the left and right lane indices
        left_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] - margin)) & (nonzerox < (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] + margin)))
        right_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] - margin)) & (nonzerox < (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] + margin)))

        # Again, extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        # Color in left and right line pixels
        out_img[lefty, leftx] = [255, 0, 0]
        out_img[righty, rightx] = [0, 0, 255]

        # Fit a second order polynomial to each
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        return left_fit, right_fit, out_img

    def visualize_lines_from_fit(self, img, l_fit, r_fit):

        # Undistort, threshold, warp
        binary_warped = self.get_birdseye_binary_warped(img)

        left_fit, right_fit, out_img = self.find_lane_lines_from_fit(binary_warped, l_fit, r_fit)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )
        left_fitx = LaneMath.eval_poly_at(ploty, left_fit)
        right_fitx = LaneMath.eval_poly_at(ploty, right_fit)

        # Set the width of the windows +/- margin
        margin = 100

        # Generate a polygon to illustrate the search window area
        # And recast the x and y points into usable format for cv2.fillPoly()
        left_line_window1 = np.array([np.transpose(np.vstack([left_fitx-margin, ploty]))])
        left_line_window2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx+margin, ploty])))])
        left_line_pts = np.hstack((left_line_window1, left_line_window2))

        right_line_window1 = np.array([np.transpose(np.vstack([right_fitx-margin, ploty]))])
        right_line_window2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx+margin, ploty])))])
        right_line_pts = np.hstack((right_line_window1, right_line_window2))

        # Create an image to show the selection window
        window_img = np.zeros_like(out_img)
        cv2.fillPoly(window_img, np.int_([left_line_pts]), (0,255, 0))
        cv2.fillPoly(window_img, np.int_([right_line_pts]), (0,255, 0))

        # Draw the selection window onto the output image
        result = cv2.addWeighted(out_img, 1, window_img, 0.3, 0)

        plt.figure()
        plt.imshow(result)
        plt.plot(left_fitx, ploty, color='yellow')
        plt.plot(right_fitx, ploty, color='yellow')
        plt.xlim(0, 1296)
        plt.ylim(972, 0)
        plt.show()

        left_curverad_px, right_curverad_px = LaneMath.get_curve_radii_in_pixels(ploty, left_fit, right_fit)
        print("left curve {:.3f} px, right curve {:.3f} px".format(left_curverad_px, right_curverad_px))

        left_curverad_m, right_curverad_m = LaneMath.get_curve_radii_in_meters(ploty, left_fitx, right_fitx)
        print("left curve {:.3f} m, right curve {:.3f} m".format(left_curverad_m, right_curverad_m))

        lane_center_px = LaneMath.get_lane_center_in_pixels(ploty, left_fit, right_fit)
        lane_offset_m = LaneMath.get_lane_offset_in_meters(binary_warped.shape[1], lane_center_px)
        print("lane center {:.3f} px, offset from lane center {:.3f} m".format(lane_center_px, lane_offset_m))

        return left_fit, right_fit

    @staticmethod
    def measure_relative_line_curvature(line_fitx):
        len_fitx = len(line_fitx)
        avg_top_fitx = np.mean(line_fitx[:len_fitx//3]).astype(int)
        avg_mid_fitx = np.mean(line_fitx[len_fitx//3:(2*len_fitx)//3]).astype(int)
        avg_bot_fitx = np.mean(line_fitx[(2*len_fitx)//3:]).astype(int)

        top_diff = avg_top_fitx - avg_mid_fitx
        bot_diff = avg_mid_fitx - avg_bot_fitx

        return top_diff, bot_diff

    @staticmethod
    def lines_are_similar(y, line1_fit, line2_fit):
        ''' TODO: Implement this if necessary '''
        #line_diff = np.subtract(right_fitx, left_fitx).astype(int)
        #line_mean = np.mean(line_diff).astype(int)
        #print("TODO: Implement lines_are_similar (l1:{} l2:{})".format(line1_fit, line2_fit))
        return True

    @staticmethod
    def find_line_indices_using_sliding_windows(binary_warped, nonzerox, nonzeroy, margin=100):
        '''
        Define the line finding algorithms using the Line class, do some predictive
        assumptions, check sanity of findings, fallback if necessary
        '''

        # Assuming you have created a warped binary image called "binary_warped"
        # Take a histogram of the bottom half of the image
        histogram = np.sum(binary_warped[int(binary_warped.shape[0]*0.75):,:], axis=0)

        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]//2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # Choose the number of sliding windows
        nwindows = 15

        # Set height of windows
        window_height = np.int(binary_warped.shape[0]//nwindows)

        # Current positions to be updated for each window
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Set minimum number of pixels found to recenter window
        minpix = 50

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        left_lane_windows = []
        right_lane_windows = []

        # Step through the windows one by one
        for window in range(nwindows):

            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window+1)*window_height  # bottom of image - (next window count * window height)
            win_y_high = binary_warped.shape[0] - window*window_height     # bottom of image - (curr window count * window height)
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin

            # Save the window rect coordinates for drawing later
            left_lane_windows.append([(win_xleft_low,win_y_low),(win_xleft_high,win_y_high)])
            right_lane_windows.append([(win_xright_low,win_y_low),(win_xright_high,win_y_high)])

            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)

            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

        # Concatenate the arrays of indices
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        return left_lane_inds, right_lane_inds, left_lane_windows, right_lane_windows

    @staticmethod
    def plot_line(img, x, y, color=(255,255,0), thickness=2):
        ''' Takes an image and two arrays of x and y points similar to matplotlib
            and writes the lines onto the image. If the points are floats, they
            are rounded and converted to ints to satisfy opencv.
        '''
        points = np.rint(np.vstack([x,y]).T).astype(int)
        cv2.polylines(img, [points], False, color, thickness)

    def find_lane_lines(self, binary_warped, margin=100, method='sliding_windows',
                        prev_left_line=None, prev_right_line=None, produce_out_img=True):

        # This code was adapted from the Udacity 'Finding the Lines' section of the
        # Advanced Lane Finding lesson
        # https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/2b62a1c3-e151-4a0e-b6b6-e424fa46ceab/lessons/40ec78ee-fb7c-4b53-94a8-028c5c60b858/concepts/c41a4b6b-9e57-44e6-9df9-7e4e74a1a49a

        ####
        # 1. Try to identify the lane lines in the image

        # Identify the x and y positions of all non-zero valued pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Try to select only the points related to the the lines

        # If we have a previous line, use the 'previous fit' method to get the indexes
        # of the nonzero values associated with the lines
        if ((method == 'previous_fit') and
            (prev_left_line is not None) and (prev_left_line.detected != False) and
            (prev_right_line is not None) and (prev_right_line.detected != False)):

            # Grab the fitx points along the line for all of the non-zero pixel y-values
            left_nonzerofitx = LaneMath.eval_poly_at(nonzeroy, prev_left_line.best_fit)
            right_nonzerofitx = LaneMath.eval_poly_at(nonzeroy, prev_right_line.best_fit)

            # Grab the indices of any non-zero pixels that are within the specified margin of the fitx points
            left_lane_inds = ((nonzerox > (left_nonzerofitx - margin)) & (nonzerox < (left_nonzerofitx + margin)))
            right_lane_inds = ((nonzerox > (right_nonzerofitx - margin)) & (nonzerox < (right_nonzerofitx + margin)))

            # Initialize empty arrays for the windows, which are not used for this method but will
            # be consulted later for drawing to the output image.
            left_lane_windows, right_lane_windows = [], []
        else:
            # Otherwise fall back to the sliding windows method
            left_lane_inds, right_lane_inds, left_lane_windows, right_lane_windows = self.find_line_indices_using_sliding_windows(binary_warped, nonzerox, nonzeroy, margin=margin)

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        # Generate y values for plotting and fitting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )

        # Fit a second order polynomial using any historical information if possible
        # Otherwise, just use the non-zero pixels we detected
        #left_fit, left_history_heatmap = fit_from_history_heatmap(leftx, lefty, ploty, prev_line=prev_left_line, img=binary_warped)
        #right_fit, right_history_heatmap = fit_from_history_heatmap(rightx, righty, ploty, prev_line=prev_right_line, img=binary_warped)

        # Fit a second order polynomial to each group of pixels
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        if (produce_out_img):
            # Create an output image to draw on and visualize the result and
            # Color the non-zero values that are part of the lanes
            #out_img = np.dstack((left_history_heatmap, np.zeros_like(left_history_heatmap), right_history_heatmap))

            # Create an output image to draw on and visualize the result and
            # Color the non-zero values that are part of the lanes
            out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
            out_img[lefty, leftx] = [255, 0, 0]
            out_img[righty, rightx] = [0, 0, 255]

            # Draw the windows on the visualization image (if there are any to draw)
            for rect_points in left_lane_windows:
                cv2.rectangle(out_img, rect_points[0], rect_points[1], (0,255,0), 2)
            for rect_points in right_lane_windows:
                cv2.rectangle(out_img, rect_points[0], rect_points[1], (0,255,0), 2)

        ####
        # 2. Now check the sanity of the curves we tried to detect

        sane_left = True
        sane_right = True

        # Generate x-values for plotting and conversion to meters
        left_fitx = LaneMath.eval_poly_at(ploty, left_fit)
        right_fitx = LaneMath.eval_poly_at(ploty, right_fit)

        # Calculate the curvature radius in pixels at the bottom of the image
        y_eval = np.max(ploty)
        left_radius_of_curvature_px = LaneMath.get_curve_radius(y_eval, left_fit)
        right_radius_of_curvature_px = LaneMath.get_curve_radius(y_eval, right_fit)

        # Calculate the curvature radius in meters
        # The image size and fitx values need to be specified since the x- and y-
        # values need to be scaled before fitting a line and evaluating at a point.
        left_radius_of_curvature_m = LaneMath.get_curve_radius_in_meters(ploty, left_fitx)
        right_radius_of_curvature_m = LaneMath.get_curve_radius_in_meters(ploty, right_fitx)

        # - Check that Left and Right curvature is not too small (<100)
        if (left_radius_of_curvature_m < 100):
            print("WARNING: left_radius_of_curvature_m < 100:", left_radius_of_curvature_m)
            sane_left = False

        if (right_radius_of_curvature_m < 100):
            print("WARNING: right_radius_of_curvature_m < 100:", right_radius_of_curvature_m)
            sane_right = False

        # - Check that Left and Right have similar curvature
        left_shape = self.measure_relative_line_curvature(left_fitx)
        #print("left_shape", left_shape)
        right_shape = self.measure_relative_line_curvature(right_fitx)
        #print("right_shape", right_shape)

        # - Check that Left and Right are separated by approximately the right distance horizontally
        line_diff = np.subtract(right_fitx, left_fitx).astype(int)
        line_mean = np.mean(line_diff).astype(int)

        if (line_mean > 825) or (line_mean < 525):
            print("WARNING: mean line_diff out of range: 525 > {} > 825".format(line_mean))
            sane_left = False
            sane_right = False

        # - Check that Left and Right are roughly parallel
        norm_line_diff = line_diff - line_mean
        #print("norm_line_diff", norm_line_diff)
        max_line_x_diff = np.max(np.abs(norm_line_diff))
        max_line_x_thresh = 140

        if (max_line_x_diff > max_line_x_thresh):
            print("WARNING: max line x diff {} > thresh {}".format(max_line_x_diff, max_line_x_thresh))
            sane_left = False
            sane_right = False

        ####
        # 3. Depending on the sanity check results and past history, figure out what values to use going forward

        left_line = Line()
        left_line.detected_fit = left_fit
        left_line.detected_pixelsx = leftx
        left_line.detected_pixelsy = lefty

        right_line = Line()
        right_line.detected_fit = right_fit
        right_line.detected_pixelsx = rightx
        right_line.detected_pixelsy = righty

        if (sane_left):
            left_line.detected = True
        else:
            if (prev_left_line is not None):
                left_line.detected = self.lines_are_similar(ploty, prev_left_line.best_fit, left_fit)

        if (sane_right):
            right_line.detected = True
        else:
            if (prev_right_line is not None):
                right_line.detected = self.lines_are_similar(ploty, prev_right_line.best_fit, right_fit)

        if ((left_line.detected is False) and (prev_left_line is not None)):
            # Predict based on history available in recent_fitxs
            left_line.used_fitx = prev_left_line.predict_next_fitx()
            left_line.used_fit = np.polyfit(ploty, left_line.used_fitx, 2)
        else:
            # Either the line was detected successfully, so use it, or
            # we don't have any history to use, so we have no choice but use the fit we have.
            # The sliding windows method will be used next time anyway.
            left_line.used_fit = left_fit
            left_line.used_fitx = left_fitx

        if ((right_line.detected is False) and (prev_right_line is not None)):
            # Predict based on history available in recent_fitxs
            right_line.used_fitx = prev_right_line.predict_next_fitx()
            right_line.used_fit = np.polyfit(ploty, right_line.used_fitx, 2)
        else:
            # Either the line was detected successfully, so use it, or
            # we don't have any history to use, so we have no choice but use the fit we have.
            # The sliding windows method will be used next time anyway.
            right_line.used_fit = right_fit
            right_line.used_fitx = right_fitx

        ###
        # 4. Update our recent history and best evaluations

        # Copy previous recent_fitxs values if available
        if (prev_left_line is not None):
            if (len(prev_left_line.recent_fitxs) == prev_left_line.history_depth):
                left_line.recent_fitxs = prev_left_line.recent_fitxs[1:]
            else:
                left_line.recent_fitxs = prev_left_line.recent_fitxs[:]
        # Append the new used_fitx value to the history
        left_line.recent_fitxs.append(left_line.used_fitx)

        # Copy previous recent_fitxs values if available
        if (prev_right_line is not None):
            if (len(prev_right_line.recent_fitxs) == prev_right_line.history_depth):
                right_line.recent_fitxs = prev_right_line.recent_fitxs[1:]
            else:
                right_line.recent_fitxs = prev_right_line.recent_fitxs[:]
        # Append the new used_fitx value to the history
        right_line.recent_fitxs.append(right_line.used_fitx)

        # Update the best_fit and best_fitx values
        left_line.best_fitx = Prediction.find_weighted_averages(left_line.recent_fitxs, left_line.history_depth)[-1]
        left_line.best_fit = np.polyfit(ploty, left_line.best_fitx, 2)

        right_line.best_fitx = Prediction.find_weighted_averages(right_line.recent_fitxs, right_line.history_depth)[-1]
        right_line.best_fit = np.polyfit(ploty, right_line.best_fitx, 2)

        ####
        # 5. Calculate the radius based on the best values

        left_line.radius_of_curvature_px = LaneMath.get_curve_radius(y_eval, left_line.best_fit)
        left_line.radius_of_curvature_m = LaneMath.get_curve_radius_in_meters(ploty, left_line.best_fitx)

        right_line.radius_of_curvature_px = LaneMath.get_curve_radius(y_eval, right_line.best_fit)
        right_line.radius_of_curvature_m = LaneMath.get_curve_radius_in_meters(ploty, right_line.best_fitx)

        if (produce_out_img):
            # Draw the search window on the output image if using the previous fit method
            if (method == 'previous_fit'):

                # Generate a polygon to illustrate the search window area
                # And recast the x and y points into usable format for cv2.fillPoly()
                left_line_window1 = np.array([np.transpose(np.vstack([left_fitx - margin, ploty]))])
                left_line_window2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx + margin, ploty])))])
                left_line_pts = np.hstack((left_line_window1, left_line_window2))

                right_line_window1 = np.array([np.transpose(np.vstack([right_fitx - margin, ploty]))])
                right_line_window2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx + margin, ploty])))])
                right_line_pts = np.hstack((right_line_window1, right_line_window2))

                # Create an image to show the selection window
                window_img = np.zeros_like(out_img)
                cv2.fillPoly(window_img, np.int_([left_line_pts]), (0,255, 0))
                cv2.fillPoly(window_img, np.int_([right_line_pts]), (0,255, 0))

                # Draw the selection window onto the output image
                out_img = cv2.addWeighted(out_img, 1, window_img, 0.3, 0)

            # Draw the used lines on the output image
            if (left_line.detected):
                self.plot_line(out_img, left_line.used_fitx, ploty)
            else:
                self.plot_line(out_img, left_line.used_fitx, ploty, color=(0,255,255))

            if (right_line.detected):
                self.plot_line(out_img, right_line.used_fitx, ploty)
            else:
                self.plot_line(out_img, right_line.used_fitx, ploty, color=(0,255,255))

            # Draw the best lines on the output image
            self.plot_line(out_img, left_line.best_fitx, ploty, color=(255,0,255))
            self.plot_line(out_img, right_line.best_fitx, ploty, color=(255,0,255))
        else:
            out_img = None

        return left_line, right_line, out_img

    def draw_lane_on_image(self, img, binary_warped, ploty, left_fitx, right_fitx):

        # Create an image to draw the projected lines on
        warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

        # Warp the blank back to original image space
        new_warp = self.birdseye.unwarp(color_warp)

        # Combine the result with the original image
        return cv2.addWeighted(img, 1, new_warp, 0.3, 0)

    def visualize_lanes_using_matplotlib(self, img, left_line=None, right_line=None):

        # Undistort, threshold, warp

        img = self.img_mgr.undistort(img)
        binary_warped = self.get_birdseye_binary_warped(img, undistort=False)

        # Set the width of the windows +/- margin
        margin = 100

        if ((left_line == None) or (right_line == None)):
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='sliding_windows')
        else:
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='previous_fit',
                                                             prev_left_line=left_line, prev_right_line=right_line)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )

        result = self.draw_lane_on_image(img, binary_warped, ploty, left_line.best_fitx, right_line.best_fitx)

        # Visualize the lines
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        f.tight_layout()
        ax1.imshow(out_img)
        ax1.set_title('Birds Eye', fontsize=15)
        ax1.set_xlim(0, 1296)
        ax1.set_ylim(972, 0)
        ax2.imshow(result)
        ax2.set_title('Lane detected', fontsize=15)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.)
        plt.show()

        print("left curve {:.3f} px, right curve {:.3f} px".format(left_line.radius_of_curvature_px, right_line.radius_of_curvature_px))
        print("left curve {:.3f} m, right curve {:.3f} m".format(left_line.radius_of_curvature_m, right_line.radius_of_curvature_m))

        lane_center_px = LaneMath.get_lane_center_in_pixels(ploty, left_line.best_fit, right_line.best_fit)
        lane_offset_m = LaneMath.get_lane_offset_in_meters(binary_warped.shape[1], lane_center_px)
        print("lane center {:.3f} px, offset from lane center {:.3f} m".format(lane_center_px, lane_offset_m))

        return left_line, right_line

    def visualize_lanes_using_diagnostic_screen(self, img, left_line=None, right_line=None):

        # Undistort, threshold, warp
        undistorted = self.img_mgr.undistort(img)

        # Warp to birds-eye view
        masked = self.birdseye.apply_cropping_mask(undistorted)
        warped = self.birdseye.warp(masked)

        # Convert to color spaces
        gry = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)
        hls = cv2.cvtColor(warped, cv2.COLOR_RGB2HLS)

        # Take the average of adding the L and S channels from the HLS encoding and then apply
        # the appropriate thresholds

        lumsat_thresh=(100, 255)

        lumsat = (np.float32(hls[:,:,1]) + np.float32(hls[:,:,2]))//2
        lumsat_binary = np.zeros_like(gry)
        lumsat_binary[(lumsat >= lumsat_thresh[0]) & (lumsat <= lumsat_thresh[1])] = 1

        binary_warped = np.zeros_like(lumsat_binary).astype(np.uint8)
        binary_warped[lumsat_binary == 1] = 1

        # Set the width of the windows +/- margin
        margin = 100

        if ((left_line == None) or (right_line == None)):
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='sliding_windows')
        else:
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='previous_fit',
                                                             prev_left_line=left_line, prev_right_line=right_line)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )

        undistorted_overlayed = self.draw_lane_on_image(undistorted, binary_warped, ploty, left_line.best_fitx, right_line.best_fitx)

        curverad = (left_line.radius_of_curvature_m + right_line.radius_of_curvature_m) / 2

        lane_center_px = LaneMath.get_lane_center_in_pixels(ploty, left_line.best_fit, right_line.best_fit)
        lane_offset_m = LaneMath.get_lane_offset_in_meters(binary_warped.shape[1], lane_center_px)

        screen = DiagnosticScreen.compose_diagScreen(curverad=curverad, offset=lane_offset_m,
                                    mainDiagScreen=undistorted_overlayed,
                                    diag1=warped, diag2=lumsat_binary, diag3=None, diag4=None,
                                    diag5=None, diag6=None, diag7=out_img, diag8=None, diag9=None)

        return screen, left_line, right_line

    def visualize_lane_using_basicScreen(self, img, ploty, left_line=None, right_line=None):

        img = self.img_mgr.undistort(img)
        binary_warped = self.get_birdseye_binary_warped(img, undistort=False)

        # Set the width of the windows +/- margin
        margin = 100

        if ((left_line == None) or (right_line == None)):
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='sliding_windows', produce_out_img=False)
        else:
            left_line, right_line, out_img = self.find_lane_lines(binary_warped, margin=margin, method='previous_fit',
                                                             prev_left_line=left_line, prev_right_line=right_line, produce_out_img=False)

        undistorted_overlayed = self.draw_lane_on_image(img, binary_warped, ploty, left_line.best_fitx, right_line.best_fitx)

        curverad = (left_line.radius_of_curvature_m + right_line.radius_of_curvature_m) / 2

        lane_center_px = LaneMath.get_lane_center_in_pixels(ploty, left_line.best_fit, right_line.best_fit)
        lane_offset_m = LaneMath.get_lane_offset_in_meters(binary_warped.shape[1], lane_center_px)

        screen = DiagnosticScreen.compose_basicScreen(undistorted_overlayed, curverad=curverad, offset=lane_offset_m)

        return screen, left_line, right_line
