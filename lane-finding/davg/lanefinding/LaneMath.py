import numpy as np
import cv2

class LaneMath:

    @staticmethod
    def get_curve_radius(eval_value, fit_coef):
        '''
        Return the radius of the curve at the specified point.
        Using f(y) = Ay^2 + By + C
        Where y = eval_value and [A,B,C] are the fit_coef values
        Radius = [1 + (dx/dy)^2]^3/2 / |d^2x / dy^2|
               = (1 + (2Ay + B)^2)^3/2 / |2A|
        http://www.intmath.com/applications-differentiation/8-radius-curvature.php
        https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/2b62a1c3-e151-4a0e-b6b6-e424fa46ceab/lessons/40ec78ee-fb7c-4b53-94a8-028c5c60b858/concepts/2f928913-21f6-4611-9055-01744acc344f
        '''
        return ((1 + (2*fit_coef[0]*eval_value + fit_coef[1])**2)**1.5) / np.absolute(2*fit_coef[0])

    @staticmethod
    def convert_x_pixels_to_meters(values):
        return np.multiply(values, 0.00528571) # 3.7/700 meters/pixel in x dimension

    @staticmethod
    def convert_y_pixels_to_meters(values):
        return np.multiply(values, 0.04166667) # 30/720 meters/pixel in y dimension

    @classmethod
    def convert_pixels_to_meters(cls, x_values, y_values):
        ''' Convenience method. Scales x and y coordinates from the birds-eye view to their
            equivalent values in meters in real-world space.
        '''
        return cls.convert_x_pixels_to_meters(x_values), cls.convert_y_pixels_to_meters(y_values)

    @classmethod
    def get_curve_radius_in_meters(cls, ploty, x_values):
        ''' Scales plot points for a birds-eye curve from pixel coordinates to
            meters, re-performs a polyfit to get the appropriate polynomial
            coefficients, then evaluates the curve radius equation at the
            point at the bottom of the image.
        '''

        # Convert the pixel values to meter values
        conv_x, conv_y = cls.convert_pixels_to_meters(x_values, ploty)

        # Find new fit polynomial values based on the new input
        conv_fit = np.polyfit(conv_y, conv_x, 2)

        # Grab the max y-value
        y_eval = np.max(conv_y)

        # Return the radius at that point
        return cls.get_curve_radius(y_eval, conv_fit)

    @classmethod
    def get_curve_radii_in_pixels(cls, ploty, left_fit, right_fit):
        ''' Convenience method for getting the curvature of the left and right
            lane lines in pixels.
        '''

        # Define y-value where we want radius of curvature
        # In this case, the maximum y-value, corresponding to the bottom of the image
        y_eval = np.max(ploty)

        left_curverad = cls.get_curve_radius(y_eval, left_fit)
        right_curverad = cls.get_curve_radius(y_eval, right_fit)

        return left_curverad, right_curverad

    @classmethod
    def get_curve_radii_in_meters(cls, ploty, leftx, rightx):
        ''' Convenience method for getting the curvature of the left and right
            lane lines in meters.
        '''
        left_curverad = cls.get_curve_radius_in_meters(ploty, leftx)
        right_curverad = cls.get_curve_radius_in_meters(ploty, rightx)

        return left_curverad, right_curverad

    @staticmethod
    def eval_poly_at(at, poly_coefficients):
        ''' Creates the polynomial defined by the coefficients, then evaluates it at the specified value(s).
            If 'at' is a scalar, returns a scalar. If it is an array, performs it for all values and returns
            an array of the same dimensions.
        '''
        poly = np.poly1d(poly_coefficients)
        return poly(at)

    @classmethod
    def get_lane_center_in_pixels(cls, ploty, left_fit, right_fit):
        ''' Find the center pixel value between the right and left lines at the bottom of the image.
        '''
        # Grab the y point at the bottom of the image
        y_eval = np.max(ploty)

        # Evaluate the x points at that y-point
        left_x = cls.eval_poly_at(y_eval, left_fit)
        right_x = cls.eval_poly_at(y_eval, right_fit)

        return ((right_x + left_x) // 2)

    @classmethod
    def get_lane_offset_in_meters(cls, img_width, lane_center):
        ''' Converts the pixel offset to meters '''
        return cls.convert_x_pixels_to_meters(img_width//2 - lane_center)
