import numpy as np
from moviepy.editor import VideoFileClip
from davg.lanefinding.Pipeline import Pipeline

left_line = None
right_line = None
pipeline = Pipeline()
ploty = np.linspace(0, 971, 972)

def lane_line_diag(img):
    global left_line, right_line, pipeline, ploty
    screen, left_line, right_line = pipeline.visualize_lane_using_basicScreen(img, ploty, left_line, right_line)
    return screen

def writeout_lane_finding_video_with_basicScreen(src, dst, start=0, end=0):
    clip = VideoFileClip(src).subclip(start, end)
    diag_clip = clip.fl_image( lane_line_diag )
    diag_clip.write_videofile(dst)

# UNCOMMENT TO RUN
writeout_lane_finding_video_with_basicScreen('video/stream1.mpg', 'video/stream1_basic-20180304.mp4', start=0, end=None)
