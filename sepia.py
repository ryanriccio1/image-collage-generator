import image
import pixel_transform


def convert_pixel_to_sepia(pixel):
    r = int(min((pixel.getRed() * 0.393 + pixel.getGreen() * 0.769 + pixel.getBlue() * 0.189), 255))
    g = int(min((pixel.getRed() * 0.349 + pixel.getGreen() * 0.686 + pixel.getBlue() * 0.168), 255))
    b = int(min((pixel.getRed() * 0.272 + pixel.getGreen() * 0.534 + pixel.getBlue() * 0.131), 255))

    pixel = image.Pixel(r, g, b)
    return pixel


def apply_sepia(img):
    return pixel_transform.transform(img, convert_pixel_to_sepia)
