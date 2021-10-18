'''

This script will allow one to draw rectangles on an image and upon mouse release it will print the 
upper left corner (x,y) and the lower right corner (x,y) values along with the scaled values.

usage: python rect-hotspot.py --image-path ../images/8x8matrix_expansion.png --width 600 --read-file --show-hotspots

'''
import argparse
import imutils
import cv2
import csv
import numpy as np

WINDOW_NAME = "Image"

collected_hotspots = []
image = None

# variables
ix = -1
iy = -1
drawing = False


def draw_reactangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, image
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            image2 = read_image()
            print(image2.shape)
            cv2.rectangle(image2, pt1=(ix, iy), pt2=(x, y), color=(0, 255, 255), thickness=3)
            image = image2

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(image, pt1=(ix, iy), pt2=(x, y), color=(0, 255, 255), thickness=3)
        print(ix, iy, x, y)
        collected_hotspots.append((ix, iy, x, y))
        image = read_image()


def mouse_events(event, x, y,
                flags, param):

    draw_reactangle_with_drag(event, x, y, flags, param)

    if show_hotspots:
        show_collected_hotspots()

    cv2.imshow(WINDOW_NAME, image)

def show_collected_hotspots():
    for points in collected_hotspots:
        ix = int(points[0])
        iy = int(points[1])
        x = int(points[2])
        y = int(points[3])

        cv2.rectangle(image, pt1=(ix, iy), pt2=(x, y), color=(255, 0, 0), thickness=3)


def read_image():
    if mask_transparent:
        _image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        print(_image.shape)
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


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--image-path", type=str, required=True, help="Path to the image to load")
    ap.add_argument("--width", type=int, required=False, default=None, help="Resize image to specified width")
    ap.add_argument("--height", type=int, required=False, default=None, help="Resize image to specified height")
    
    ap.add_argument("--filename", required=False, default="rect-hotspots.csv",
                    help="Optional[rect-hotspots.csv] Filename to save hotspot data")
    ap.add_argument("--read-file", action='store_true', help="read the filename for initial hotspots")
    ap.add_argument("--mask-transparent", action='store_true', help="If the image has a transparent background, map the transparent background to white")
    ap.add_argument("--show-hotspots", action='store_true', help="If present, then always show collected hotspots on the image")

    args = vars(ap.parse_args())

    image_path = args['image_path']
    width = args['width']
    height = args['height']
    filename = args['filename']
    read_file = args['read_file']
    mask_transparent = args['mask_transparent']
    show_hotspots = args['show_hotspots']
    
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_NAME, mouse_events)

    image = read_image()

    if read_file:
        # read in the hotspot data
        with open(filename, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                # print(f'\t{row}')
                row = list(np.float_(row))
                ix = int(row[0] * image.shape[1])
                iy = int(row[1] * image.shape[0])
                x = int(row[2] * image.shape[1])
                y = int(row[3] * image.shape[0])

                collected_hotspots.append((ix,iy,x,y))
                print(collected_hotspots)

    if show_hotspots:
        show_collected_hotspots()

    cv2.imshow(WINDOW_NAME, image)

    cv2.waitKey(0)

    with open(filename, "w") as f:
        hotsport_writer = csv.writer(f, delimiter=',')
        for i, data in enumerate(collected_hotspots):
            norm_ix = data[0] / image.shape[1]
            norm_iy = data[1] / image.shape[0]
            norm_x = data[2] / image.shape[1]
            norm_y = data[3] / image.shape[0]
            hotsport_writer.writerow([norm_ix, norm_iy, norm_x, norm_y])


    cv2.destroyAllWindows()

    
