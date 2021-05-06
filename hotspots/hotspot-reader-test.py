import cv2
import numpy as np
import argparse
import csv
import imutils

window_name = 'HotSpotEditor'
radius = None
video_frame_redraw_backup = None
video_frame = None
frame = None


hot_spots = []

def _is_point_in_circle(x,y):
    for i, data in enumerate(hot_spots):
        in_circle = (x-data[0])**2 + (y-data[1])**2 < data[2]**2
        if in_circle:
            return i
    else:
        return None


def draw_circles():
    global video_frame
    if video_frame is not None:
        for i,data in enumerate(hot_spots):
            x = int(data[0]*video_frame.shape[1])
            y = int(data[1]*video_frame.shape[0])
            radius = int(data[2]*(video_frame.shape[0]*video_frame.shape[1]))
            cv2.circle(video_frame, (x,y), radius, (255, 0, 255), 1, lineType=cv2.LINE_AA)



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, required=False, default=None,
                    help="Optional [None]: Resize VideoCapture image to specified width ")
    ap.add_argument("--filename", required=False, default="hotspots.csv", help="Optional[hotspots.csv] Filename to save hotspot data")
    args = vars(ap.parse_args())

    width = args['width']
    filename = args['filename']

    # read in the hotspot data
    with open(filename, "r") as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            print(f'\t{row}')
            row = list(np.float_(row))
            hot_spots.append(row)

    cv2.namedWindow(window_name)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if width is not None:
            video_frame = imutils.resize(frame, width=width)
        else:
            video_frame = frame

        draw_circles()
        cv2.imshow(window_name, video_frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
