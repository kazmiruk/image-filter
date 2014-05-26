from hashlib import sha256
import logging
from PIL import Image
from StringIO import StringIO
import urllib

import settings


def get_full_url(url):
    """ return absolute url by relative url
    """
    if not hasattr(settings, 'CFS') or\
            'DOMAIN_MASK' not in settings.CFS or\
            'MAX_DOMAINS' not in settings.CFS:
        raise AttributeError()

    domain_mask = settings.CFS['DOMAIN_MASK']
    max_domains = settings.CFS['MAX_DOMAINS']

    domain_id = int(
        '0x' + sha256(url).hexdigest(),
        0
    ) % max_domains + 1

    return domain_mask.format(domain_id) + url


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