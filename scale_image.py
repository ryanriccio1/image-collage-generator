import image
from math import floor


def get_nearest_pixel_by_factor(original_image, width_factor, height_factor, new_x, new_y):
    col_nearest = min(int(round(new_x / width_factor)), original_image.getWidth() - 1)
    row_nearest = min(int(round(new_y / height_factor)), original_image.getHeight() - 1)

    return original_image.getPixel(col_nearest, row_nearest)


def get_nearest_pixel_by_location(img, scale_factor_x, scale_factor_y, x, y):
    x_nearest = int(floor(x / scale_factor_x))
    y_nearest = int(floor(y / scale_factor_y))
    return img.getPixel(x_nearest, y_nearest)


def scale_by_factor(img, width_factor, height_factor):
    width = img.getWidth()
    height = img.getHeight()

    scaled_image = image.EmptyImage(int(width * width_factor), int(height * height_factor))
    for row in range(scaled_image.getHeight()):
        for col in range(scaled_image.getWidth()):
            pixel = get_nearest_pixel_by_factor(img, width_factor, height_factor, col, row)
            scaled_image.setPixel(col, row, pixel)

    return scaled_image


def scale_to_size(img, width, height):
    old_width = img.getWidth()
    old_height = img.getHeight()

    scaled_image = image.EmptyImage(width, height)

    scale_factor_x = width / old_width
    scale_factor_y = height / old_height

    for row in range(scaled_image.getHeight()):
        for col in range(scaled_image.getWidth()):
            pixel = get_nearest_pixel_by_location(img, scale_factor_x, scale_factor_y, col, row)
            scaled_image.setPixel(col, row, pixel)

    return scaled_image
