import numpy as np
import matplotlib.pyplot as plt

def show_gauss_plot(width=111):
    mu, sigma = 0, 0.2
    bins = np.linspace(-0.6, 0.6, width)
    gauss = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2))
    norm_gauss = gauss / np.max(gauss)

    plt.plot(norm_gauss, linewidth=2, color='r')
    plt.show()
    
# UNCOMMENT TO RUN
show_gauss_plot()
