import numpy as np
from davg.lanefinding.Prediction import Prediction

class Line():
    def __init__(self):

        # was the line detected in the last iteration?
        self.detected = False

        # x-values for detected line pixels
        self.detected_pixelsx = None

        # y-values for detected line pixels
        self.detected_pixelsy = None

        # polynomial coefficients for the fit to the detected pixels
        self.detected_fit = [np.array([False])]

        # x-values resulting from evaluating detected_fit at the y-values
        self.detected_fitx = None

        # polynomial coefficients for the fit that was actually used
        # This may be the same as detected_fit, or a predicted value based on
        # the differences in the recent history
        self.used_fit = [np.array([False])]

        # x-values resulting from evaluating used_fit at the y-values
        self.used_fitx = None

        # Depth of the history to keep
        self.history_depth = 5

        # x-values of the last history_depth fits of the line
        self.recent_fitxs = []

        # Polynomial coefficients for the polynomial fit to the best_fitx
        self.best_fit = [np.array([False])]

        # Weighted average of x-values from recent_fitxs values
        self.best_fitx = None

        # Image showing detected line pixels decayed over last history_depth iterations
        #self.history_heatmap = None

        #radius of curvature of the best_fit line in pixels
        self.radius_of_curvature_px = None

        #radius of curvature of the best_fit line in meters
        self.radius_of_curvature_m = None

    def predict_next_fitx(self):
        #return self.recent_fitxs[-1]
        return Prediction.predict_next_values(self.recent_fitxs, window=self.history_depth)
