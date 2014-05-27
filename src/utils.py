import logging
from PIL import Image
from StringIO import StringIO
import urllib


def get_image(url):
    """ downloading image by url and creating PIL object
    """
    logging.info("Downloading img {url}".format(
        url=url
    ))

    content_response = urllib.urlopen(url)
    content = content_response.read()
    f = StringIO(content)

    return Image.open(f)