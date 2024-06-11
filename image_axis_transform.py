import image


def vertical_flip(img):
    height = img.getHeight()
    width = img.getWidth()
    last = width - 1

    flipped_image = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            pixel = img.getPixel(last - x, y)
            flipped_image.setPixel(x, y, pixel)
    return flipped_image


def horizontal_flip(img):
    height = img.getHeight()
    width = img.getWidth()
    last = height - 1

    flipped_image = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            pixel = img.getPixel(x, last - y)
            flipped_image.setPixel(x, y, pixel)
    return flipped_image


def vertical_mirror(img):
    height = img.getHeight()
    width = img.getWidth()
    distance = width // 2
    last = width - 1

    mirrored_image = image.EmptyImage(width, height)
    for x in range(distance):
        for y in range(height):
            pixel = img.getPixel(x, y)
            mirrored_image.setPixel(x, y, pixel)

    for x in range(distance, width):
        for y in range(height):
            pixel = img.getPixel(last - x, y)
            mirrored_image.setPixel(x, y, pixel)

    return mirrored_image


def horizontal_mirror(img):
    height = img.getHeight()
    width = img.getWidth()
    distance = height // 2
    last = height - 1

    mirrored_image = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(distance):
            pixel = img.getPixel(x, y)
            mirrored_image.setPixel(x, y, pixel)

    for x in range(width):
        for y in range(distance, height):
            pixel = img.getPixel(x, last - y)
            mirrored_image.setPixel(x, y, pixel)

    return mirrored_image
