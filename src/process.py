import logging
from StringIO import StringIO
import re

from processors.crop import Crop
from processors.resize import Resize
from utils import get_image


def process(host, path, callback):
    __regexp_list = [
        r'^/(resize)/(\d+)x(-|\d+)',
        r'^/(crop)(?:/(\d+)x(-|\d+))'
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

                if width in ('-', ''):
                    width = 0

                height = mathced.group(3)

                if height in ('-', ''):
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
                    logging.info("Add crop processor width size {width}x{height}".format(
                        width=width,
                        height=height
                    ))

                    workers.append(Crop(width, height))

                cont = True
                break

    image = get_image(host + path)
    source_image_type = image.format.lower()

    for worker in workers:
        image = worker.do(image)

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