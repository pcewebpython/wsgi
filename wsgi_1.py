#!/usr/bin/env python
from datetime import datetime

default = "No Value Set"

body = """<html>
<head>
<title>Lab 3 - WSGI experiments</title>
</head>
<body>
<p>Hey there, this page has been generated by {software}, running at {path}</p>
<p>Today is {month} {date}, {year}.</p>
<p>This page was requested by IP Address {client_ip}</p>
</body>
</html>"""


def application(environ, start_response):
    import pprint
    pprint.pprint(environ)

    response_body = body.format(
        software=environ.get('SERVER_SOFTWARE', default),
        path=environ.get("SERVER_PATH", default),
        month=datetime.today().strftime("%B"),
        date=datetime.today().strftime("%#d"),
        year=datetime.today().strftime("%Y"),
        client_ip=environ.get("REMOTE_ADDR", default)
    )
    status = '200 OK'

    response_headers = [('Content-Type', 'text/html'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
