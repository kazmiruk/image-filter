import logging
from logging.config import dictConfig

from exception import Http404, Http502
from process import process
import settings

dictConfig(settings.LOGGING)


def application(environ, start_response):
    """application which realize wsgi interface
    """
    host = "{schema}://{host}".format(schema=environ['wsgi.url_scheme'], host=environ['HTTP_HOST'])
    path = environ['PATH_INFO']

    logging.info("Query obtained with path {path}".format(path=environ['PATH_INFO']))

    try:
        return process(host, path, start_response)
    except Http404:
        start_response('404 Not Found', [])
        return []
    except Http502:
        start_response('502 Bad gateway', [])
        return []
    except Exception, e:
        logging.error(e, exc_info=True)
        raise e


def WSGIHandler():
    """WSGI wrapper for server
    """
    return application