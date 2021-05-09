from uielements.uielements import CircleButton, DisplayValueLabel
import numpy as np
import cv2
import time


def handle_mouse_events(event, x, y, flags, params):
    circle_btn.process_point(x, y, img)
    circle_btn2.process_point(x, y, img)
    circle_btn3.process_point(x, y, img)


cv2.namedWindow("image")
cv2.setMouseCallback("image", handle_mouse_events)

if __name__ == '__main__':

    # create blank image - y, x
    # 600 - rows (y)
    # 1000 - columns (x)
    img = np.zeros((600, 1000, 3), np.uint8)

    circle_btn = CircleButton(500, 300, 50, "Btn1", (255, 0, 255))
    circle_btn.draw(img)

    circle_btn2 = CircleButton(100, 100, 50, "Btn2", (255, 0, 255))
    circle_btn2.draw(img)

    circle_btn3 = CircleButton(800, 400, 50, "Btn3", (255, 0, 255))
    circle_btn3.draw(img)

    l1 = DisplayValueLabel(3,3,140,40,"Test")
    l1.set_value(99)
    l1.draw(img)
    while True:

        # display image
        cv2.imshow('image', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
