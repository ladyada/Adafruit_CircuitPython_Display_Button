# The MIT License (MIT)
#
# Copyright (c) 2019 Limor Fried for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_display_button`
================================================================================

UI Buttons for displayio


* Author(s): Limor Fried

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio
from adafruit_display_text.text_area import TextArea
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Display_Button.git"


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
        self._selected = False
        self.group = displayio.Group()

        self.fill_color = fill_color
        self.outline_color = outline_color
        self.label_color = label_color
        # Selecting inverts the button colors!
        self.selected_fill = selected_fill
        self.selected_outline = selected_outline
        self.selected_label = selected_label

        if self.selected_fill is None and fill_color is not None:
            self.selected_fill = (~fill_color) & 0xFFFFFF
        if self.selected_outline is None and outline_color is not None:
            self.selected_outline = (~outline_color) & 0xFFFFFF

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

            if self.selected_label is None and label_color is not None:
                self.selected_label = (~label_color) & 0xFFFFFF
            #print(dims)

        """
        #else: # ok just a bounding box
            #self.bodyshape = displayio.Shape(width, height)
            #self.group.append(self.bodyshape)
        """

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if value != self._selected:
            self._selected = value
        if self._selected:
            self.body.fill = self.selected_fill
            self.body.outline = self.selected_outline
            self.label.color = self.selected_label
        else:
            self.body.fill = self.fill_color
            self.body.outline = self.outline_color
            self.label.color = self.label_color

    def contains(self, point):
        return (self.x <= point[0] <= self.x+self.width) and (self.y <= point[1] <= self.y+self.height)
