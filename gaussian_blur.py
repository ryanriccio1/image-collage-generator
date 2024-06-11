import numpy as np
import convolution


def generate_gaussian_kernel(size, sigma=1.0):
    # https://miro.medium.com/max640/1*YpLYVBomcYNNbwncG5iP9Q.webp
    # equation of gaussian kernel of size (2*size + 1) * (2*size + 1)
    size = int(size) // 2

    # make horizontal and vertical masks according to gaussian distribution
    x, y = np.mgrid[-size:size + 1, -size:size + 1]

    # part of the gaussian equation (basically just a scalar)
    normal = 1 / (2.0 * np.pi * sigma ** 2)

    # gaussian kernel formula
    kernel = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    return kernel


def apply_blur(img, blur_distance=5, sigma=1.4):
    gaussian_kernel = generate_gaussian_kernel(blur_distance, sigma)
    return convolution.convolve(img, gaussian_kernel)
