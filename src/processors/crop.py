import logging


class Crop(object):
    """ Crop processor. Make square region from image
    """
    def do(self, image):
        width, height = image.size

        side = min(width, height)

        logging.info("Image will be croped to region with side {side}".format(
            side=side
        ))

        image = image.crop((0, 0, side, side))
        image.load()

        return image