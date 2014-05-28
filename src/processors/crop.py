import logging

from base import Processor
from resize import Resize


class Crop(Processor):
    def do(self, image):
        width, height = image.size

        side = min(width, height)

        logging.info("Image will be croped to region with side {side}".format(
            side=side
        ))

        image = image.crop((0, 0, side, side))
        image.load()

        if self._width > 0 or self._height > 0:
            image = Resize(self._width, self._height).do(image)

        return image