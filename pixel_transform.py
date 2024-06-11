import image


def transform(img, pixel_filter):
    width = img.getWidth()
    height = img.getHeight()
    modified_image = image.EmptyImage(width, height)

    for row in range(height):
        for col in range(width):
            pixel = img.getPixel(col, row)
            pixel = pixel_filter(pixel)
            modified_image.setPixel(col, row, pixel)

    modified_image.setPosition(width + 1, 0)
    return modified_image
