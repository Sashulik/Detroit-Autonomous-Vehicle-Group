import numpy as np
import cv2

class DiagnosticScreen:

    @staticmethod
    def normalized(img):
        return np.uint8(255*img/np.max(np.absolute(img)))

    @classmethod
    def to_RGB(cls, img):
        if img.ndim == 2:
            img_normalized = cls.normalized(img)
            return np.dstack((img_normalized, img_normalized, img_normalized))
        elif img.ndim == 3:
            return img
        else:
            return None

    @classmethod
    def update_diagScreen_cell(cls, diagScreen, img, w, h, r, c, text=None, color=(255,0,0), thickness=2):
        rgb = cls.to_RGB(img)
        if text is not None:
            fontFace = cv2.FONT_HERSHEY_COMPLEX
            fontScale = 2
            offset = 20
            textSize, _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
            cv2.putText(rgb, text, (offset, textSize[1] + offset), fontFace, fontScale, color, thickness)
        diagScreen[r*h:(r+1)*h, c*w:(c+1)*w] = cv2.resize(rgb, (w, h), interpolation=cv2.INTER_AREA)
        return diagScreen

    @classmethod
    def compose_filter_diagScreen(cls, diag1=None, diag2=None, diag3=None,
                                  diag4=None, diag5=None, diag6=None,
                                  diag7=None, diag8=None, diag9=None,
                                  diag10=None, diag11=None, diag12=None,
                                  diag13=None, diag14=None, diag15=None,
                                  title1=None, title2=None, title3=None,
                                  title4=None, title5=None, title6=None,
                                  title7=None, title8=None, title9=None,
                                  title10=None, title11=None, title12=None,
                                  title13=None, title14=None, title15=None):

        width = 320
        height = 240

        rows = 5
        cols = 3

        # Initialize the output image.
        diagScreen = np.zeros((height * rows, width * cols, 3), dtype=np.uint8)

        # top row
        if diag1 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag1, width, height, r=0, c=0, text=title1)
        if diag2 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag2, width, height, r=0, c=1, text=title2)
        if diag3 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag3, width, height, r=0, c=2, text=title3)

        if diag4 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag4, width, height, r=1, c=0, text=title4)
        if diag5 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag5, width, height, r=1, c=1, text=title5)
        if diag6 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag6, width, height, r=1, c=2, text=title6)

        if diag7 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag7, width, height, r=2, c=0, text=title7)
        if diag8 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag8, width, height, r=2, c=1, text=title8)
        if diag9 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag9, width, height, r=2, c=2, text=title9)

        if diag10 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag10, width, height, r=3, c=0, text=title10)
        if diag11 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag11, width, height, r=3, c=1, text=title11)
        if diag12 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag12, width, height, r=3, c=2, text=title12)

        # bottom row
        if diag13 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag13, width, height, r=4, c=0, text=title13)
        if diag14 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag14, width, height, r=4, c=1, text=title14)
        if diag15 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag15, width, height, r=4, c=2, text=title15)

        return diagScreen

    @classmethod
    def compose_2x3_screen(cls, diag1=None, diag2=None, diag3=None,
                           diag4=None, diag5=None, diag6=None,
                           title1=None, title2=None, title3=None,
                           title4=None, title5=None, title6=None,
                           color=(255,0,0), thickness=2):

        width = 320
        height = 240

        rows = 2
        cols = 3

        # Initialize the output image.
        diagScreen = np.zeros((height * rows, width * cols, 3), dtype=np.uint8)

        if diag1 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag1, width, height, r=0, c=0, text=title1, color=color, thickness=thickness)
        if diag2 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag2, width, height, r=0, c=1, text=title2, color=color, thickness=thickness)
        if diag3 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag3, width, height, r=0, c=2, text=title3, color=color, thickness=thickness)

        if diag4 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag4, width, height, r=1, c=0, text=title4, color=color, thickness=thickness)
        if diag5 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag5, width, height, r=1, c=1, text=title5, color=color, thickness=thickness)
        if diag6 is not None:
            diagScreen = cls.update_diagScreen_cell(diagScreen, diag6, width, height, r=1, c=2, text=title6, color=color, thickness=thickness)

        return diagScreen

    @classmethod
    def compose_diagScreen(cls, curverad=0, offset=0,
                       mainDiagScreen=None, diag1=None, diag2=None, diag3=None, diag4=None,
                       diag5=None, diag6=None, diag7=None, diag8=None, diag9=None):

        # Initialize the output image. Dimensions: 1080 H x 1920 W
        diagScreen = np.zeros((1080, 1920, 3), dtype=np.uint8)

        # Main screen (720x1280) in upper left
        if mainDiagScreen is not None:
            diagScreen[0:720, 0:1280] = cv2.resize(mainDiagScreen, (1280,720))

        # Four small (240x320) diagnostic screens in upper right
        if diag1 is not None:
            diagScreen[0:240, 1280:1600] = cv2.resize(cls.to_RGB(diag1), (320,240), interpolation=cv2.INTER_AREA)
        if diag2 is not None:
            diagScreen[0:240, 1600:1920] = cv2.resize(cls.to_RGB(diag2), (320,240), interpolation=cv2.INTER_AREA)
        if diag3 is not None:
            diagScreen[240:480, 1280:1600] = cv2.resize(cls.to_RGB(diag3), (320,240), interpolation=cv2.INTER_AREA)
        if diag4 is not None:
            diagScreen[240:480, 1600:1920] = cv2.resize(cls.to_RGB(diag4), (320,240), interpolation=cv2.INTER_AREA)*4

        # Gap of 120x320 on right side

        # One medium (480x640) diagnostic screen in lower right
        if diag7 is not None:
            diagScreen[600:1080, 1280:1920] = cv2.resize(cls.to_RGB(diag7), (640,480), interpolation=cv2.INTER_AREA)*4

        # Middle panel (120x1280) below main screen on left side

        # Use cv2 for drawing text in diagnostic pipeline.
        font = cv2.FONT_HERSHEY_COMPLEX
        middlepanel = np.zeros((120, 1280, 3), dtype=np.uint8)
        cv2.putText(middlepanel, 'Estimated lane curvature: {:5.3f} m'.format(curverad), (30, 60), font, 1, (255,0,0), 2)
        cv2.putText(middlepanel, 'Estimated offset from center of lane: {:.3f} m'.format(offset), (30, 90), font, 1, (255,0,0), 2)

        diagScreen[720:840, 0:1280] = middlepanel

        # Four small (240x320) diagnostic screens in lower left
        if diag5 is not None:
            diagScreen[840:1080, 0:320] = cv2.resize(cls.to_RGB(diag5), (320,240), interpolation=cv2.INTER_AREA)
        if diag6 is not None:
            diagScreen[840:1080, 320:640] = cv2.resize(cls.to_RGB(diag6), (320,240), interpolation=cv2.INTER_AREA)
        if diag8 is not None:
            diagScreen[840:1080, 640:960] = cv2.resize(cls.to_RGB(diag8), (320,240), interpolation=cv2.INTER_AREA)
        if diag9 is not None:
            diagScreen[840:1080, 960:1280] = cv2.resize(cls.to_RGB(diag9), (320,240), interpolation=cv2.INTER_AREA)

        return diagScreen

    @staticmethod
    def compose_basicScreen(img, curverad=0, offset=0):

        # Determine which side of center in English
        if (offset <= 0):
            side = 'left'
        else:
            side = 'right'

        # Make the offset a positive number now that we have the side
        offset = abs(offset)

        # Use cv2 for drawing text in diagnostic pipeline.
        font = cv2.FONT_HERSHEY_COMPLEX
        color = (255, 255, 255)
        cv2.putText(img, 'Radius of curvature: {}m'.format(int(curverad)), (30, 50), font, 1, color, 1)
        cv2.putText(img, 'Vehicle is {:.2f}m {} of center'.format(offset, side), (30, 90), font, 1, color, 1)

        return img
