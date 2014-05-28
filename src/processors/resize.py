import logging
from PIL import Image

import settings
from base import Processor


class Resize(Processor):
    def do(self, image):
        (width, height) = image.size

        if self._width > width:
            self._width = width

        if self._height > height:
            self._height = height

        if self._width > 0 and self._height == 0:
            coef = width * 1.0 / self._width
            self._height = int(height / coef)
        elif self._height > 0 and self._width == 0:
            coef = height * 1.0 / self._height
            self._width = int(width / coef)
        elif self._width == 0 and self._height == 0:
            return image

        if width >= self._width and height >= self._height:
            logging.info("Image will be resized to {width}x{height}".format(
                width=self._width,
                height=self._height
            ))

            image = image.resize(
                (self._width, self._height),
                getattr(Image, settings.RESAMPLE, Image.ANTIALIAS)
            )
        else:
            logging.info("Image to small and will not be processed")

        return image