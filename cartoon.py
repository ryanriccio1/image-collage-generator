import numpy as np
import cv2
import image


def edge_mask(img, line_size, blur_value):
    # convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # use median blur is good enough and fast enough
    img = cv2.medianBlur(img, blur_value)

    # the threshold value is the mean of a neighborhood area (line_size). values past this generate threshold are
    # give a value of 255. it is cv2 neighbor aware edge detection
    edges = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges


def color_quantization(img, k):
    # https://www.programcreek.com/python/?code=PacktPublishing%2FMastering-OpenCV-4-with-Python%2FMastering-OpenCV-4-with-Python-master%2FChapter10%2F01-chapter-content%2Fk_means_color_quantization.py
    # get the image as a np array of pixels (shape = [num_pixels, 3])
    data = np.float32(img).reshape((-1, 3))

    # stop the algorithm when we hit accuracy epsilon (0.001) or when we hit
    # 20 iterations, whichever comes first
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    # Implementing K-Means
    # pick k-amount of random values. Calculate the distance each pixel value is from the value. Continue to
    # adjust the random values to get closer and closer to the center of the pixel values in a given 'bin' until
    # we have reached a set accuracy, or too many iterations, whichever comes first.
    # this will give us a compactness value which is the sum of the distance from the center all the pixel values
    # are, a label which is each pixel's assignment to a center value, and a list of center pixel values of len=k
    compactness, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # convert to int
    center = np.uint8(center)

    # for each pixel, use the label to get the center value
    result = center[label.flatten()]

    # convert to image shape rather than 1d array
    result = result.reshape(img.shape)
    return result


def apply_cartoon(img, line_size=7, blur_value=5, k=12, d=9):
    img_list = []
    # convert the image to a numpy array of pixel values
    for row in img.to_list():
        pixels = []
        for pixel in row:
            pixels.append(list(pixel.getColorTuple()))
        img_list.append(pixels)
    img = np.array(img_list)
    img = np.uint8(img)

    # cv2 uses BGR while the image library uses RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    edges = edge_mask(img, line_size, blur_value)
    color_changes = color_quantization(img, k)

    # bilateral filtering is almost a dual pass of gaussian blur
    # it uses one gaussian to act as a mask, and another gaussian to make sure that only pixels with similar
    # intensities are considered. Then it performs a blur on only the similar pixels, and keeps the edge
    # since the edge will have a different pixel intensity
    blurred = cv2.bilateralFilter(color_changes, d=d, sigmaColor=200, sigmaSpace=200)

    # use bitwise and to apply the mask
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    new_img = image.EmptyImage(img.shape[1], img.shape[0])
    # iterate through the pixels
    for row in range(cartoon.shape[0]):
        for col in range(cartoon.shape[1]):
            # get the pixel value from the cartoon image
            pixel = image.Pixel(int(cartoon[row, col][2]), int(cartoon[row, col][1]), int(cartoon[row, col][0]))
            # apply convolution, sum values, and set pixel
            new_img.setPixel(col, row, pixel)

    return new_img
