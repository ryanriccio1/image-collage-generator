import image


def invert_pixel(pixel):
    r, g, b = pixel.getColorTuple()
    r = 255 - r
    g = 255 - g
    b = 255 - b
    pixel = image.Pixel(r, g, b)
    return pixel


def apply_negative(img):
    width = img.getWidth()
    height = img.getHeight()

    negative = image.EmptyImage(width, height)
    for row in range(height):
        for col in range(width):
            pixel = invert_pixel(img.getPixel(col, row))
            negative.setPixel(col, row, pixel)
    return negative
