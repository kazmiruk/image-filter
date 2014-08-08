import logging
from PIL import Image
from StringIO import StringIO
import urllib

from exception import Http404, Http502


def get_image(url):
    """ downloading image by url and creating PIL object
    """
    logging.info("Downloading img {url}".format(
        url=url
    ))

    content_response = urllib.urlopen(url)

    status_code = content_response.getcode()

    if 400 <= status_code < 500:
        raise Http404()
    elif 500 <= status_code:
        raise Http502()

    content = content_response.read()
    f = StringIO(content)

    return Image.open(f)