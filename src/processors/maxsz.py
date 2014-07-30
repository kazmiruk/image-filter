import logging
from PIL import Image

import settings
from base import Processor


class Maxsz(Processor):
    def do(self, image):
        if self._width == 0 or self._height == 0:
            return image

        (width, height) = image.size

        coef = max([
            width * 1.0 / self._width,
            height * 1.0 / self._height
        ])

        if coef > 1.0:
            self._width = int(width / coef)
            self._height = int(height / coef)

            logging.info("Image will be resized to {width}x{height} to fit pointed size".format(
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