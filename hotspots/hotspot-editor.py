import cv2
import argparse
import csv
import numpy as np

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

def _draw_hotspots():
    for i, data in enumerate(hot_spots):
        cv2.circle(video_frame, (data[0], data[1]), data[2], (255, 0, 255), 1, lineType=cv2.LINE_AA)


def draw_circle(event, x,y, flags, params):
    global video_frame
    if video_frame is not None:
        existing_hot_spot_index = _is_point_in_circle(x, y)
        if existing_hot_spot_index is not None:
            del hot_spots[existing_hot_spot_index]
        else:
            hot_spots.append(
                [x,y,radius]
            )

        video_frame = video_frame_redraw_backup.copy()
        _draw_hotspots()

def handle_mouse_events(event, x, y, flags, params):
    global video_frame, video_frame_redraw_backup

    if event != 0:
        print(event)

    if event == cv2.EVENT_LBUTTONDOWN:
        draw_circle(event, x, y, flags, params)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if video_frame is None:
            video_frame = frame.copy()
            video_frame_redraw_backup = video_frame
            _draw_hotspots()

        else:
            video_frame = None



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, required=False, default=50,
                    help="Optional [50]: Radius size")
    ap.add_argument("--filename", required=False, default="hotspots.csv", help="Optional[hotspots.csv] Filename to save hotspot data")
    ap.add_argument("--read-file", action='store_true', help="read the filename for initial hotspots")

    args = vars(ap.parse_args())

    radius = args['radius']
    filename = args['filename']
    read_file = args['read_file']

    frame_shape = None
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, handle_mouse_events)

    cap = cv2.VideoCapture(0)

    save_hotspots = False

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if frame_shape is None:
            frame_shape = frame.shape

        if video_frame is not None:
            cv2.imshow(window_name, video_frame)
        else:
            cv2.imshow(window_name, frame)

        if read_file:
            read_file = False
            # read in the hotspot data
            with open(filename, "r") as f:
                csv_reader = csv.reader(f, delimiter=',')
                for row in csv_reader:
                    print(f'\t{row}')
                    row = list(np.float_(row))
                    hot_spots.append([int(row[0]*frame_shape[1]), int(row[1]*frame_shape[0]), int(row[2]*(frame_shape[0]*frame_shape[1]))])

        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('s'):
            save_hotspots = True
            break


    cap.release()
    cv2.destroyAllWindows()

    if save_hotspots:
        with open(filename, "w") as f:
            hotsport_writer = csv.writer(f, delimiter=',')
            for i, data in enumerate(hot_spots):

                norm_x = data[0] / frame_shape[1]
                norm_y = data[1] / frame_shape[0]
                norm_radius = data[2] / (frame_shape[0]*frame_shape[1])
                hotsport_writer.writerow([norm_x, norm_y, norm_radius])
