import glob
import matplotlib.image as mpimg

import os.path

from davg.lanefinding.Pipeline import Pipeline

def demonstrate_lane_finding_on_test_images(data):

    pipeline = Pipeline()
    
    for idx in range(len(data)):

        # Read in a test image
        img = mpimg.imread(data[idx])

        # Process it
        left_line, right_line = pipeline.visualize_lanes_using_matplotlib(img)

# UNCOMMENT TO RUN
test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_lane_finding_on_test_images(test_images[0:2])
