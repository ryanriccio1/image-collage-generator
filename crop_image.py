import image


def crop(img, new_x, new_y):
    new_img = image.EmptyImage(new_x, new_y)
    for row in range(new_y):
        for col in range(new_x):
            new_img.setPixel(col, row, img.getPixel(col, row))

    return new_img
