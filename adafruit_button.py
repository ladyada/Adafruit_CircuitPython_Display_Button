import displayio
from adafruit_display_text.text_area import TextArea
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect

class Button():
    RECT = const(0)
    ROUNDRECT = const(1)
    SHADOWRECT = const(2)
    SHADOWROUNDRECT = const(3)
    def __init__(self, *, x, y, width, height, style=RECT,
                 fill_color=0xFFFFFF, outline_color=0x0,
                 label=None, label_font=None, label_color=0x0,
                 selected_fill=None, selected_outline=None,
                 selected_label=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._font = label_font

        self.group = displayio.Group()

        if outline_color or fill_color:
            self.body = self.shadow = None
            if style == RECT:
                self.body = Rect(x, y, width, height,
                                 fill=fill_color, outline=outline_color)
            elif style == ROUNDRECT:
                self.body = RoundRect(x, y, width, height, r=10,
                                      fill=fill_color, outline=outline_color)
            elif style == SHADOWRECT:
                self.shadow = Rect(x+2, y+2, width-2, height-2,
                                   fill=outline_color)
                self.body = Rect(x, y, width-2, height-2,
                                 fill=fill_color, outline=outline_color)
            elif style == SHADOWROUNDRECT:
                self.shadow = RoundRect(x+2, y+2, width-2, height-2, r=10,
                                   fill=outline_color)
                self.body = RoundRect(x, y, width-2, height-2, r=10,
                                 fill=fill_color, outline=outline_color)
            if self.shadow:
                self.group.append(self.shadow)
            self.group.append(self.body)

        if label:   # button with text label
            if not label_font:
                raise RuntimeError("Please provide label font")
            dims = label_font.text_bounding_box(label)
            if dims[2] >= width or dims[3] >= height:
                raise RuntimeError("Button not large enough for label")
            self.label = TextArea(label_font, text=label)
            self.label.x = x + (width - dims[2])//2
            self.label.y = y + (height - dims[3])
            self.label.color = label_color
            self.group.append(self.label)
            print(dims)

        """
        #else: # ok just a bounding box
            #self.bodyshape = displayio.Shape(width, height)
            #self.group.append(self.bodyshape)
        """

    @property
    def select(self):
        return self._selected

    @select.setter
    def select(self, value):
        self._selected = not self._selected

    def contains(self, point):
        return (self.x <= point[0] <= self.x+self.width) and (self.y <= point[1] <= self.y+self.height)
