import numpy as np
import image


def get_new_image_size(num_pixels, kernel_size):
    new_pixels = 0

    # this allows for the image to be size - kernel_size + 1
    # even if the image is divisible by kernel_size
    for current_pixel in range(num_pixels):
        if current_pixel + kernel_size <= num_pixels:
            new_pixels += 1

    return new_pixels


def _sum_convolved(convolved_image, kernel_size):
    red = 0
    green = 0
    blue = 0
    # add up all the RGB values in an array (size=kernel_size, kernel_size)
    for current_row in range(kernel_size):
        for current_pixel in range(kernel_size):
            red += convolved_image[current_row, current_pixel][0]
            green += convolved_image[current_row, current_pixel][1]
            blue += convolved_image[current_row, current_pixel][2]

    # make sure we are within limits, clip out of bound values
    red = max(min(int(red), 255), 0)
    green = max(min(int(green), 255), 0)
    blue = max(min(int(blue), 255), 0)

    return image.Pixel(red, green, blue)


def convolve(img, kernel):
    # get a list of all the pixel objects in the image
    orig_img_pixels = np.array(img.to_list())

    kernel_size = kernel.shape[0]
    # get the size of the pixels we have
    width = get_new_image_size(orig_img_pixels.shape[1], kernel_size)
    height = get_new_image_size(orig_img_pixels.shape[0], kernel_size)

    # empty image
    convolved_image = image.EmptyImage(width, height)

    # iterate through the pixels
    for row in range(height):
        for col in range(width):
            # select the pixels that we will multiply by our kernel
            mask = orig_img_pixels[row:row + kernel_size, col:col + kernel_size]

            # apply convolution, sum values, and set pixel
            convolved_image.setPixel(col, row, _sum_convolved(np.multiply(mask, kernel), kernel_size))
    return convolved_image


def __mul__(self, other):
    # image.Pixel does not have a method to support multiplying the entire pixel by a value
    # this is the implementation to multiple a pixel by a value
    return self.get_red() * other, self.get_green() * other, self.get_blue() * other


# dynamically apply these overloaded functions to the library
setattr(image.Pixel, '__mul__', __mul__)
