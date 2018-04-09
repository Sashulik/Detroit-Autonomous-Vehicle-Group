from moviepy.editor import VideoFileClip
import distutils.dir_util

class VidFrames():

    @staticmethod
    def frange(start, stop, step):
        ''' Generator: Converts start, stop, and step parameters to a time value. '''
        _idx = start
        while _idx < stop:
            yield _idx
            _idx += step

    @classmethod
    def extract_frames(cls, name, start_time=0.0, interval=0.1, max_images=25):
        ''' Generator: Extracts frames from a video clip and returns them one at a time. '''
        if (name == ""):
            return
        clip = VideoFileClip(name + '.mpg')
        for _clip_idx in cls.frange(start_time, min([clip.end, start_time + max_images*interval]), interval):
            yield clip.to_ImageClip(_clip_idx).img

    @staticmethod
    def save_frames_to_dir(name, t_start=0, t_end=None, fps=24):
        ''' Extracts frames from a video clip and saves them to the filesystem. '''
        if (name == ""):
            return
        clip = VideoFileClip(name + '.mpg').subclip(t_start, t_end)
        distutils.dir_util.mkpath('{}/'.format(name))
        return clip.write_images_sequence("{}/frame%03d.jpg".format(name), fps=fps)
