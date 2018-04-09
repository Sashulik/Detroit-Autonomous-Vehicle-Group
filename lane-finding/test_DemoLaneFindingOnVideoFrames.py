from davg.lanefinding.VidFrames import VidFrames
from davg.lanefinding.Pipeline import Pipeline

def demonstrate_lane_finding_on_video_frames():

    left_line = None
    right_line = None

    pipeline = Pipeline()

    i_frame = 0
    for img in VidFrames.extract_frames('video/stream1', start_time=22.2, interval=1/24, max_images=15):

        print("frame:", i_frame)

        left_line, right_line = pipeline.visualize_lanes_using_matplotlib(img, left_line, right_line)

        i_frame += 1

# UNCOMMENT TO RUN
demonstrate_lane_finding_on_video_frames()
