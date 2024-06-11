import image_axis_transform
import sepia
import grayscale
import negative
import edge_detect
import emboss
import gaussian_blur
import scale_image
import crop_image
import image
import tkinter as tk


def draw(img, src_window, pos_x, pos_y):
    # use index to place rather than pixel values
    img.setPosition(img.getWidth() * pos_x + 5 * (pos_x + 1), img.getHeight() * pos_y + 5 * (pos_y + 1))
    img.draw(src_window)


def save_to_disk(img_1, img_2, img_3, img_4, img_5, img_6, img_7, img_8, img_9, output_file):
    img_width = img_1.getWidth()
    img_height = img_1.getHeight()

    master_img = image.EmptyImage(img_width * 3, img_height * 3)

    for row in range(img_height):
        for col in range(img_width):
            pixel_00 = img_1.getPixel(col, row)
            pixel_10 = img_2.getPixel(col, row)
            pixel_20 = img_3.getPixel(col, row)
            pixel_01 = img_4.getPixel(col, row)
            pixel_11 = img_5.getPixel(col, row)
            pixel_21 = img_6.getPixel(col, row)
            pixel_02 = img_7.getPixel(col, row)
            pixel_12 = img_8.getPixel(col, row)
            pixel_22 = img_9.getPixel(col, row)

            master_img.setPixel(col, row, pixel_00)
            master_img.setPixel(col + img_width, row, pixel_10)
            master_img.setPixel(col + img_width * 2, row, pixel_20)

            master_img.setPixel(col, row + img_height, pixel_01)
            master_img.setPixel(col + img_width, row + img_height, pixel_11)
            master_img.setPixel(col + img_width * 2, row + img_height, pixel_21)

            master_img.setPixel(col, row + img_height * 2, pixel_02)
            master_img.setPixel(col + img_width, row + img_height * 2, pixel_12)
            master_img.setPixel(col + img_width * 2, row + img_height * 2, pixel_22)
    master_img.save(output_file)


def main(src_img, input_size, kernel_size, output_file=None):
    # open image and set size for input to filters
    main_img = image.FileImage(src_img)
    new_height = int(main_img.getHeight() * (input_size / main_img.getWidth()))
    main_img = scale_image.scale_to_size(main_img, input_size, new_height)

    # get the size of the screen
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # get the amount we have to scale the images before we write to screen
    width_factor = (screen_width - 200) / (main_img.getWidth() + 5) / 3
    height_factor = (screen_height - 200) / (main_img.getHeight() + 5) / 3
    scale_factor = 0

    # scale with best fit
    if main_img.getHeight() * width_factor < screen_height - 200:
        scale_factor = height_factor
    elif main_img.getWidth() * height_factor < screen_width - 200:
        scale_factor = width_factor

    # show the window with the best fit
    window = image.ImageWin(int(main_img.getWidth() * scale_factor * 3 + 5),
                            int(main_img.getHeight() * scale_factor * 3 + 5), "Collage")
    window.configure(background="black")

    # all images take in the scaled input, then their output is scaled again to fit the screen
    # this allows us to speed up processing time by selecting a different input size than the output size
    # main image
    main_img_scaled = scale_image.scale_by_factor(main_img, scale_factor, scale_factor)
    draw(main_img_scaled, window, 1, 1)

    # flipped image
    horizontal_flip_img = image_axis_transform.vertical_flip(main_img)
    hfi_scaled = scale_image.scale_by_factor(horizontal_flip_img, scale_factor, scale_factor)
    draw(hfi_scaled, window, 0, 0)

    # sepia image
    sepia_img = sepia.apply_sepia(main_img)
    si_scaled = scale_image.scale_by_factor(sepia_img, scale_factor, scale_factor)
    draw(si_scaled, window, 1, 0)

    # mirrored image
    horizontal_mirror_img = image_axis_transform.vertical_mirror(main_img)
    hmi_scaled = scale_image.scale_by_factor(horizontal_mirror_img, scale_factor, scale_factor)
    draw(hmi_scaled, window, 2, 0)

    # grayscale image
    grayscale_img = grayscale.apply_grayscale(main_img)
    gi_scaled = scale_image.scale_by_factor(grayscale_img, scale_factor, scale_factor)
    draw(gi_scaled, window, 0, 1)

    # negative image
    negative_img = negative.apply_negative(main_img)
    ni_scaled = scale_image.scale_by_factor(negative_img, scale_factor, scale_factor)
    draw(ni_scaled, window, 2, 1)

    # edge-detect image
    edge_img = edge_detect.apply_edge_detect(main_img, kernel_size)
    # crop and scale to remove edges from convolution
    edge_img = crop_image.crop(edge_img, edge_img.getWidth() - kernel_size, edge_img.getHeight() - kernel_size)
    edge_img = scale_image.scale_to_size(edge_img, main_img.getWidth(), main_img.getHeight())
    ei_scaled = scale_image.scale_by_factor(edge_img, scale_factor, scale_factor)
    draw(ei_scaled, window, 0, 2)

    # embossed image
    emboss_img = emboss.apply_emboss(main_img)
    # crop and scale to remove edges from convolution
    emboss_img = crop_image.crop(emboss_img, emboss_img.getWidth() - 3, emboss_img.getHeight() - 3)
    emboss_img = scale_image.scale_to_size(emboss_img, main_img.getWidth(), main_img.getHeight())
    embi_scaled = scale_image.scale_by_factor(emboss_img, scale_factor, scale_factor)
    draw(embi_scaled, window, 1, 2)

    # gaussian blur image
    # this has only been shown during the butterfly image, but something about the nearest neighbor scaling twice
    # mixed with the gaussian blur sometimes creates very faint lines in the image if the input size is just right
    blur_img = gaussian_blur.apply_blur(main_img, kernel_size)
    # crop and scale to remove edges from convolution
    blur_img = crop_image.crop(blur_img, blur_img.getWidth() - kernel_size, blur_img.getHeight() - kernel_size)
    blur_img = scale_image.scale_to_size(blur_img, main_img.getWidth(), main_img.getHeight())
    bi_scaled = scale_image.scale_by_factor(blur_img, scale_factor, scale_factor)
    draw(bi_scaled, window, 2, 2)

    # save to file
    if output_file:
        save_to_disk(horizontal_flip_img, sepia_img, horizontal_mirror_img,
                     grayscale_img, main_img, negative_img, edge_img,
                     emboss_img, blur_img, output_file)

    # wait for exit
    window.exitonclick()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Image Collage Generator")
    parser.add_argument('-k', "--kernel-size", default=5, type=int,
                        help="kernel size to use for gaussian blur and edge detect.")
    parser.add_argument('-i', "--input-size", default=300, type=int,
                        help="size to scale images to before processing (width)")
    parser.add_argument('-o', "--output-file", type=str, help="file to write collage to")
    parser.add_argument('input', type=str, help="file to process")

    args = parser.parse_args()
    main(args.input, args.input_size, args.kernel_size, args.output_file)
