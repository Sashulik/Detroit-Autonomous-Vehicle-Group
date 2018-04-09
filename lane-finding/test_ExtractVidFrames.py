import matplotlib.pyplot as plt

from davg.lanefinding.VidFrames import VidFrames

def demonstrate_extracting_video_frames():
    vf = VidFrames()
    for img in vf.extract_frames('video/stream1', 0.0, 0.1, 3):
        plt.figure()
        plt.imshow(img)
        plt.show()

demonstrate_extracting_video_frames()
