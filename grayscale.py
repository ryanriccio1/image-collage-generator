import image
import pixel_transform


def convert_pixel_to_gray(pixel):
    tot_intensity = pixel.getRed() + pixel.getGreen() + pixel.getBlue()
    avg_intensity = tot_intensity // 3
    bst_intensity = min(avg_intensity, 255)
    pixel = image.Pixel(bst_intensity, bst_intensity, bst_intensity)
    return pixel


def apply_grayscale(img):
    return pixel_transform.transform(img, convert_pixel_to_gray)
