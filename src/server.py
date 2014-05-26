""" Simple server for testing wsgi application
"""
import logging
from wsgiref import simple_server

import settings
from wsgi import application

server = simple_server.WSGIServer(
    (settings.SERVER_ADDRESS, settings.SERVER_PORT),
    simple_server.WSGIRequestHandler
)

logging.info("Test server starts on {host}:{port} with interval {interval}".format(
    host=settings.SERVER_ADDRESS,
    port=settings.SERVER_PORT,
    interval=settings.POLL_INTERVAL
))

server.set_app(application)
server.serve_forever(settings.POLL_INTERVAL)