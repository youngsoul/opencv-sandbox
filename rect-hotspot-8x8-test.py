from uielements.uielements import SolidColorRect
import csv
import numpy as np
import argparse
import cv2
import imutils


def read_normalized_rects_from_file(filename):
    rects = []

    with open(filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            row = list(np.float_(row))
            rects.append((row[0], row[1], row[2], row[3]))
    return rects


def denormalize_rectangles(rect_list, image_width, image_height):
    denorm_rects = []
    for rect in rect_list:
        x1 = rect[0] * image_width
        y1 = rect[1] * image_height
        x2 = rect[2] * image_width
        y2 = rect[3] * image_height
        denorm_rects.append((int(x1), int(y1), int(x2), int(y2)))

    return denorm_rects


def create_solidcolor_rects(rect_list):
    solid_rects = []
    for rect in rect_list:
        solid_rects.append(SolidColorRect(rect, color=(240, 32, 255)))

    return solid_rects

solid_rects_to_show = []

def mouse_events(event, x, y,
                 flags, param):
    global image

    if event == cv2.EVENT_LBUTTONDOWN:
        for i, solid_rect in enumerate(solid_rects):
            if solid_rect.is_point_inside(x, y):
                solid_rects_to_show.append(solid_rect)

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, solid_rect in enumerate(solid_rects_to_show):
            if solid_rect.is_point_inside(x, y):
                del solid_rects_to_show[i]

    image = copy_of_image.copy()
    for solid_rect in solid_rects_to_show:
        solid_rect.draw(image)

    cv2.imshow(WINDOW_NAME, image)


def read_image(image_path, width, height):
    if mask_transparent:
        _image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        # make mask of where the transparent bits are
        trans_mask = _image[:, :, 3] == 0

        # replace areas of transparency with white and not transparent
        _image[trans_mask] = [255, 255, 255, 255]
        # new image without alpha channel...
        # new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    else:
        _image = cv2.imread(image_path)
    _image = imutils.resize(_image, width, height)
    return _image


WINDOW_NAME = '8x8 Matrix'

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-path", type=str, required=True, help="Path to the image to load")
    ap.add_argument("--width", type=int, required=False, default=None, help="Resize image to specified width")
    ap.add_argument("--height", type=int, required=False, default=None, help="Resize image to specified height")

    ap.add_argument("--filename", required=False, default="None",
                    help="Optional. Filename to save hotspot data if provided")
    ap.add_argument("--mask-transparent", action='store_true',
                    help="If the image has a transparent background, map the transparent background to white")

    args = vars(ap.parse_args())

    image_path = args['image_path']
    width = args['width']
    height = args['height']
    filename = args['filename']
    mask_transparent = args['mask_transparent']

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_NAME, mouse_events)

    image = read_image(image_path, width, height)
    copy_of_image = image.copy()

    solid_rects = create_solidcolor_rects(denormalize_rectangles(read_normalized_rects_from_file(filename), image.shape[1], image.shape[0]))

    cv2.imshow(WINDOW_NAME, image)

    cv2.waitKey(0)
