from moviepy.editor import VideoFileClip
from davg.lanefinding.Pipeline import Pipeline

left_line = None
right_line = None
pipeline = Pipeline()

def lane_line_diag(img):
    global left_line, right_line, pipeline
    screen, left_line, right_line = pipeline.visualize_lanes_using_diagnostic_screen(img, left_line, right_line)
    return screen

def writeout_lane_finding_video_with_diag_screen(src, dst, start=0, end=0):
    clip = VideoFileClip(src).subclip(start, end)
    diag_clip = clip.fl_image( lane_line_diag )
    diag_clip.write_videofile(dst)

# UNCOMMENT TO RUN
writeout_lane_finding_video_with_diag_screen('video/stream1.mpg', 'video/stream1_test-20180304.mp4', start=0, end=None)
