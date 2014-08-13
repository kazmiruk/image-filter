import logging

from base import Processor


class Cut(Processor):
    def do(self, image):
        width, height = image.size

        if self._width > 0:
            width = min(self._width, width)

        if self._height > 0:
            height = min(self._height, height)

        logging.info("Image will be cut to region {width}x{height}".format(
            width=width,
            height=height
        ))

        image = image.crop((0, 0, width, height))
        image.load()

        return image