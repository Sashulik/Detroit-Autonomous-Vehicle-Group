import glob
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from davg.lanefinding.Pipeline import Pipeline

def demonstrate_diag_screen_with_single_image(fname):

    pipeline = Pipeline()

    img = mpimg.imread(fname)
    screen, left_line, right_line = pipeline.visualize_lanes_using_diagnostic_screen(img)

    print("left_line.best_fit", left_line.best_fit)
    print("right_line.best_fit", right_line.best_fit)

    plt.figure(figsize=(10,6))
    plt.imshow(screen)
    plt.show()

test_images = glob.glob('test_images_s1_1296x972/*.jpg')
demonstrate_diag_screen_with_single_image(test_images[0])
