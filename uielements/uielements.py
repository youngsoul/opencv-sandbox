
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
            textX, textY = self._center_text(self.label)
            # add text centered on image
            cv2.putText(image, self.label, (textX, textY + self.radius + 15), self.font, 1, (255, 255, 255), 2)
        else:
            cv2.circle(image, (self.anchor_x, self.anchor_y), self.radius, (0, 0, 255), 2, lineType=cv2.LINE_AA)
            textX, textY = self._center_text(self.label)
            # add text centered on image
            cv2.putText(image, self.label, (textX, textY + self.radius + 15), self.font, 1, (255, 255, 255), 2)


    def on_enter(self, x, y, image):
        self.draw(image)

    def on_exit(self, x, y, image):
        self.draw(image)

    def process_point(self, x, y, image):
        in_circle = (x-self.anchor_x)**2 + (y-self.anchor_y)**2 < self.radius**2
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

