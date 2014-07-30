import logging
from StringIO import StringIO
import re

from processors.crop import Crop
from processors.resize import Resize
from processors.maxsz import Maxsz
from utils import get_image


def process(host, path, callback):
    __regexp_list = [
        r'^/(resize)/(\d+)x(-|\d+)',
        r'^/(crop)(?:/(\d+)x(-|\d+))?',
        r'^/(maxsz)/(\d+)x(\d+)'
    ]

    workers = []
    cont = True

    while cont:
        cont = False

        for pattern in __regexp_list:
            mathced = re.match(pattern, path, re.IGNORECASE)

            if mathced is not None:
                path = re.sub(pattern, '', path, re.IGNORECASE)

                key = mathced.group(1)

                width = mathced.group(2)

                if width is None or width in ('-', ''):
                    width = 0

                height = mathced.group(3)

                if height is None or height in ('-', ''):
                    height = 0

                width = int(width)
                height = int(height)

                if key == 'resize':
                    logging.info("Add resize processor with size {width}x{height}".format(
                        width=width,
                        height=height
                    ))

                    workers.append(Resize(width, height))
                elif key == 'crop':
                    logging.info("Add crop processor with size {width}x{height}".format(
                        width=width,
                        height=height
                    ))

                    workers.append(Crop(width, height))
                elif key == 'maxsz':
                    logging.info("Add maxsz processor with size {width}x{height}".format(
                        width=width,
                        height=height
                    ))

                    workers.append(Maxsz(width, height))

                cont = True
                break

    image = get_image(host + path)
    source_image_type = image.format.upper()

    for worker in workers:
        #extract palette from Image
        pl = image.getpalette()

        image = worker.do(image)

        if pl is not None:
            #if image has palette then restore it
            image.putpalette(pl)

    source_file = StringIO()
    image.save(source_file, source_image_type)
    data = source_file.getvalue()
    data_len = len(data)

    logging.info('Image was successful processed with type {type} and len {data_len}'.format(
        type=source_image_type,
        data_len=data_len
    ))

    callback('200 OK', [
        ('Content-type', 'image/{type}'.format(type=source_image_type)),
        ('Content-length', str(data_len))
    ])
    return [data]