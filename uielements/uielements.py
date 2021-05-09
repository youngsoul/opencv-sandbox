import cv2
from abc import ABC, abstractmethod
from enum import Enum

class Shape(ABC):
    class Meta:
        class State(Enum):
            INACTIVE = 0
            ENTER = 1
            EXIT = 2

    def __init__(self, anchor_x, anchor_y, label):
        """

        :param anchor_x: anchor x-point for shape.  Could be upper left or center
        :type anchor_x:
        :param anchor_y: anchor y-point for shape.  Could be upper left or center
        :type anchor_y:
        """
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.label = label
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.state = Shape.Meta.State.INACTIVE

    # https://gist.github.com/xcsrz/8938a5d4a47976c745407fe2788c813a
    def _center_text(self, text):
        # get boundary of this text
        textsize = cv2.getTextSize(text, self.font, 1, 2)[0]
        # get coords based on boundary
        textX = self.anchor_x - (textsize[0] // 2)
        textY = self.anchor_y + (textsize[1] // 2)

        return textX, textY

    @abstractmethod
    def is_point_inside(self, x, y):
        pass

    @abstractmethod
    def process_point(self, x, y, image):
        pass

    @abstractmethod
    def on_enter(self, x, y, image):
        pass

    @abstractmethod
    def on_exit(self, x, y, image):
        pass

    @abstractmethod
    def draw(self, image):
        pass


class CircleButton(Shape):

    def __init__(self, x, y, radius, label, outline_color):
        super().__init__(x, y, label)
        self.radius = radius
        self.outline_color = outline_color

    def draw(self, image):
        if self.state == Shape.Meta.State.INACTIVE:
            cv2.circle(image, (self.anchor_x, self.anchor_y), self.radius, self.outline_color, 2, lineType=cv2.LINE_AA)
            # cv2.circle(image, (self.anchor_x, self.anchor_y), int(self.radius*0.8), self.outline_color, -1)

            textX, textY = self._center_text(self.label)
            # add text centered on image
            cv2.putText(image, self.label, (textX, textY + self.radius + 15), self.font, 1, (255, 255, 255), 2)
        else:
            cv2.circle(image, (self.anchor_x, self.anchor_y), self.radius, (0, 0, 255), 2, lineType=cv2.LINE_AA)
            cv2.circle(image, (self.anchor_x, self.anchor_y), int(self.radius*0.4), self.outline_color, -1)
            textX, textY = self._center_text(self.label)
            # add text centered on image
            cv2.putText(image, self.label, (textX, textY + self.radius + 15), self.font, 1, (255, 255, 255), 2)


    def on_enter(self, x, y, image):
        self.draw(image)

    def on_exit(self, x, y, image):
        self.draw(image)

    def process_point(self, x, y, image):
        in_circle = self.is_point_inside(x,y)
        if self.state is Shape.Meta.State.INACTIVE:
            if in_circle == True:
                self.state = Shape.Meta.State.ENTER
                self.on_enter(x, y, image)
        elif self.state == Shape.Meta.State.ENTER:
            if not in_circle:
                self.state = Shape.Meta.State.EXIT
                self.on_exit(x, y, image)
                self.state = Shape.Meta.State.INACTIVE
                self.draw(image)

    def is_point_inside(self, x, y):
        in_circle = (x - self.anchor_x) ** 2 + (y - self.anchor_y) ** 2 < self.radius ** 2
        return in_circle

class DisplayValueLabel(Shape):
    def __init__(self, x, y, width, height, label, bkgnd_color=(245, 117, 16), value_color=(255,255,255), label_value_space=10):
        super().__init__(x, y, label)
        self.width = width
        self.height = height
        self.bkgnd_color = bkgnd_color
        # textsize = tuple = (x,y)
        self.textsize = cv2.getTextSize(self.label, self.font, 1, 2)[0]
        self.value = None
        self.value_color = value_color
        self.label_x = self.anchor_x+10
        self.label_y = self.anchor_y+25
        self.value_x = self.anchor_x + self.textsize[0] + label_value_space
        self.value_y = self.anchor_y+25

    def set_value(self, val):
        self.value = val

    def draw(self, image):
        cv2.rectangle(image, (self.anchor_x, self.anchor_y), (self.anchor_x+self.width, self.anchor_y+self.height), self.bkgnd_color, -1)

        # Display Class
        cv2.putText(image, self.label
                    , (self.label_x, self.label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, f"{self.value}"
                    , (self.value_x, self.value_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    def on_enter(self, x, y, image):
        pass

    def on_exit(self, x, y, image):
        pass

    def process_point(self, x, y, image):
        pass

    def is_point_inside(self, x, y):
        return False
