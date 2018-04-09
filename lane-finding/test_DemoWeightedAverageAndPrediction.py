import numpy as np
import cv2
import matplotlib.pyplot as plt

from davg.lanefinding.Prediction import Prediction

def plot_line(img, x, y, color=(255,255,0), thickness=2):
    ''' Takes an image and two arrays of x and y points similar to matplotlib
        and writes the lines onto the image. If the points are floats, they
        are rounded and converted to ints to satisfy opencv.
    '''
    points = np.rint(np.vstack([x,y]).T).astype(int)
    #print(points)
    cv2.polylines(img, [points], False, color, thickness)

def demonstrate_weighted_average_and_prediction():

    # Create a blank array to be used as an image
    test_img = np.zeros((128, 128, 3), dtype='uint8')

    # Define common y-points
    y = np.array([0,31,63,95,127])

    # Define an array of x-point arrays
    #recent_x = np.array([[40,40,40,40,40]])
    #recent_x = np.array([[40,40,40,40,40], [30,35,37,39,40]])
    #recent_x = np.array([[40,40,40,40,40], [30,35,37,39,40], [20,30,35,38,40], [10,25,32,37,40]])
    #recent_x = np.array([[40,40,40,40,40], [30,35,37,39,40], [20,30,35,38,40], [10,25,32,37,40], [20,30,35,38,40]])
    recent_x = np.array([[40,40,40,40,40], [30,35,37,39,40], [20,30,35,38,40], [10,25,32,37,40], [0,20,29,36,40]])
    print ("recent_x", recent_x)

    # Calculate the softmax weighted averages for the x-points
    averages = Prediction.find_weighted_averages(recent_x, window=3)
    print("weighted averages", averages)

    # Calculate the differences between the each consecutive set of x-points
    recent_xdiff = np.diff(recent_x, axis=0)
    print ("recent_xdiff", recent_xdiff)

    if len(recent_xdiff) != 0:
        # Calculate the non-weighted average of the differences for a baseline
        recent_xdiff_avg = np.average(recent_xdiff, axis=0)
        print ("recent_xdiff_avg", recent_xdiff_avg)

        # Calculate the softmax weighted averages for the differences in the x-points
        xdiff_weighted_averages = Prediction.find_weighted_averages(recent_xdiff, window=2)
        print("xdiff_weighted_averages[-1]:", xdiff_weighted_averages[-1])

    # Predict the next line location by applying the last weighted diff to the last x-points
    #predicted_x = np.add(xdiff_weighted_averages[-1], recent_x[-1])
    predicted_x = Prediction.predict_next_values(recent_x, window=2)
    print("predicted:", predicted_x)

    # Plot the various lines
    for i in range(len(recent_x)):
        # Plot a red line for the weighted moving averages
        plot_line(test_img, averages[i], y, thickness=1, color=(200,0,0))

        # Plot a yellow line for the current points
        plot_line(test_img, recent_x[i], y, thickness=1)

    # Plot a green line for the predicted next line based on weighted averages of the diffs
    plot_line(test_img, predicted_x, y, thickness=1, color=(0,200,0))

    plt.imshow(test_img)
    plt.show()

# UNCOMMENT TO RUN
demonstrate_weighted_average_and_prediction()
