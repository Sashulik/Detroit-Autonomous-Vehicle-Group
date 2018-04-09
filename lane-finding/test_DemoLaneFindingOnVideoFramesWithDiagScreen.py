import glob
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from davg.lanefinding.Pipeline import Pipeline
from davg.lanefinding.VidFrames import VidFrames

def demonstrate_lane_finding_on_video_frames_with_diag_screen():

    left_line = None
    right_line = None

    pipeline = Pipeline()

    for img in VidFrames.extract_frames('video/stream1', start_time=22.2, interval=1/24, max_images=6):
        screen, left_line, right_line = pipeline.visualize_lanes_using_diagnostic_screen(img, left_line, right_line)

        print("left_line.best_fit", left_line.best_fit)
        print("right_line.best_fit", right_line.best_fit)

        plt.figure(figsize=(10,6))
        plt.imshow(screen)
        plt.show()

# UNCOMMENT TO RUN
demonstrate_lane_finding_on_video_frames_with_diag_screen()
