import logging
from PIL import Image
from StringIO import StringIO
import urllib

from exception import Http404, Http502


def get_file(url):
    """ downloading file by url and creating IO object
    """
    logging.info("Downloading file {url}".format(
        url=url
    ))

    content_response = urllib.urlopen(url)

    status_code = content_response.getcode()

    if 400 <= status_code < 500:
        raise Http404()
    elif 500 <= status_code:
        raise Http502()

    content = content_response.read()

    return StringIO(content)


def get_image(file):
    """ creates PIL object
    """
    return Image.open(file)


def get_extension(path):
    return path.split('.')[-1].lower() if '.' in path else ''