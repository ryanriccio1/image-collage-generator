import convolution
import numpy as np
import image


def apply_emboss(img):
    kernel = np.array([[-1, -1, 0],
                       [-1,  0, 1],
                       [ 0,  1, 1]])
    embossed = convolution.convolve(img, kernel)
    multiplied_img = image.EmptyImage(embossed.getWidth(), embossed.getHeight())

    for row_i, row in enumerate(embossed.to_list()):
        for col_i, col in enumerate(row):
            pixel = image.Pixel(*(col + 128))
            multiplied_img.setPixel(col_i, row_i, pixel)

    return multiplied_img


def __add__(self, other):
    # image.Pixel does not have a method to support adding the entire pixel by a value
    # this is the implementation to add a pixel with a value
    return max(min(int(self.get_red() + other), 255), 0), \
           max(min(int(self.get_green() + other), 255), 0), \
           max(min(int(self.get_blue() + other), 255), 0)


# dynamically apply these overloaded functions to the library
setattr(image.Pixel, '__add__', __add__)
