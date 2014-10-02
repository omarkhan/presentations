# coding=utf-8

import time


def hello(environ, start_response):

    # Do some work...
    time.sleep(1)

    # Send the response
    response = u'สวัสดีครับ\n'.encode('utf-8')
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', len(response)),
    ]
    start_response(status, headers)
    return response
