import logging
from PIL import Image

import settings


class Resize(object):
    """ Resize processor. Requires needed size
    """
    def __init__(self, size):
        self.__size = size

    def do(self, image):
        (width, height) = image.size

        if width > self.__size:
            logging.info("Image will be resized to {size}".format(
                size=self.__size
            ))

            coef = width / self.__size
            width = self.__size
            height = int(height / coef)

            image.thumbnail(
                (width, height),
                getattr(Image, settings.RESAMPLE, Image.ANTIALIAS)
            )
        else:
            logging.info("Image to small and will not be processed")

        return image