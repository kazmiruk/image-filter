import logging
from StringIO import StringIO
import re

from processors.crop import Crop
from processors.resize import Resize
from processors.maxsz import Maxsz
from processors.cut import Cut
from utils import get_image, get_extension, get_file


__regexp_list = {
    r'^/(resize)/(\d+)x(-|\d+)': Resize,
    r'^/(crop)(?:/(\d+)x(-|\d+))?': Crop,
    r'^/(maxsz)/(\d+)x(\d+)': Maxsz,
    r'^/(cut)/(-|\d+)x(-|\d+)': Cut
}


def _build_workers(path):
    """ Process path, build workers and remove placeholders from path
    """
    workers = []
    cont = True

    while cont:
        cont = False

        for pattern in __regexp_list:
            mathced = re.match(pattern, path, re.IGNORECASE)

            if mathced is not None:
                path = re.sub(pattern, '', path, re.IGNORECASE)

                width = mathced.group(2)

                if width is None or width in ('-', ''):
                    width = 0

                height = mathced.group(3)

                if height is None or height in ('-', ''):
                    height = 0

                workers.append(__regexp_list[pattern](int(width), int(height)))

                cont = True
                break

    return path, workers


def process(host, path, callback):
    path, workers = _build_workers(path)

    source_file = get_file(host + path)

    if get_extension(path) == 'svg':
        # http://redmine.pearbox.net/issues/1605
        source_image_type = 'svg+xml'
    else:
        image = get_image(source_file)
        exif = image.info.get('exif', b'')
        source_image_type = image.format.upper()

        for worker in workers:
            #extract palette from Image
            pl = image.getpalette()

            image = worker.do(image)

            if pl is not None:
                #if image has palette then restore it
                image.putpalette(pl)

        source_file = StringIO()
        image.save(source_file, source_image_type, exif=exif)

    data = source_file.getvalue()
    data_len = len(data)

    logging.info('Image was successful processed with type {type} and len {data_len}'.format(
        type=source_image_type, data_len=data_len))

    callback('200 OK', [('Content-type', 'image/{type}'.format(type=source_image_type)),
                        ('Content-length', str(data_len))])

    return [data]