import numpy as np
import image
import grayscale
import convolution
import gaussian_blur


def _edge_detect(img):
    # edge detection kernels
    x_kernel = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])

    y_kernel = np.array([[1, 2, 1],
                         [0, 0, 0],
                         [-1, -2, -1]])

    # apply the kernel and convert image back to list of pixels
    x_pixels = convolution.convolve(img, x_kernel).to_list()
    y_pixels = convolution.convolve(img, y_kernel).to_list()

    # convert grayscale image to array of pixel intensities (RGB should all be equal)
    x_intensity = []
    y_intensity = []

    for row in range(len(x_pixels)):
        x_intensity.append([])
        for pixel in x_pixels[row]:
            x_intensity[row].append(pixel.getRed())
    for row in range(len(y_pixels)):
        y_intensity.append([])
        for pixel in y_pixels[row]:
            y_intensity[row].append(pixel.getRed())

    # perform distance formula calculation to sum masks
    summed_masks = np.hypot(x_intensity, y_intensity)

    # generate new image from summed masks
    img = image.EmptyImage(img.getWidth(), img.getHeight())
    for row, row_values in enumerate(summed_masks):
        for col, pixel_value in enumerate(row_values):
            # use .ceil so that values >0 & <1 will have an intensity of 1
            pixel_value = max(min(int(np.ceil(pixel_value)), 255), 0)

            # apply pixel value to RGB
            img.setPixel(col, row, image.Pixel(pixel_value, pixel_value, pixel_value))

    return img


def apply_edge_detect(img, gaussian_distance=3, gaussian_amount=1.4):
    img = gaussian_blur.apply_blur(img, gaussian_distance, gaussian_amount)
    img = grayscale.apply_grayscale(img)
    img = _edge_detect(img)
    return img

