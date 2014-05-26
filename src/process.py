import logging
from StringIO import StringIO
import re

from processors.crop import Crop
from processors.resize import Resize
from utils import get_full_url, get_image


def process(path, callback):
    __regexp_list = [
        r'^/(resize)/(\d+?)x-',
        r'^/(crop)'
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

                if key == 'resize':
                    size = int(mathced.group(2))

                    logging.info("Add resize processor with size {size}".format(
                        size=size
                    ))

                    workers.append(Resize(size))
                elif key == 'crop':
                    logging.info("Add crop processor")

                    workers.append(Crop())

                cont = True
                break

    image = get_image(get_full_url(path))
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