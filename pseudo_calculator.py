"""
This pseudo calculator should support the following operations:

  * Positive
  * Negative

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/positive/5' then the response
body in my browser should be `true`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/positive/5  => 'true'
  http://localhost:8080/positive/0  => 'false'
  http://localhost:8080/positive/-5 => 'false'
  http://localhost:8080/negative/0  => 'false'
  http://localhost:8080/negative/-2 => 'true'
```
"""


def content_positive(typ):
    """ test positive """
    try:
        float(typ)
        if int(typ) > 0:
            page = """
            <h1>True</h1>
            <hr>
            <p>Number {} is positive</p> 
            """
        else:
            page = """
            <h1>False</h1>
            <hr>
            <p>Number {} is <b><em>not</em></b> positive</p> 
            """
        return page.format(typ)
    except ValueError:
        page = """
            <p><b>Number required at path's end</b></p> 
            """
        return page

def content_negative(typ):
    """ test negative """
    try:
        float(typ)
        if int(typ) < 0:
            page = """
            <h1>True</h1>
            <hr>
            <p>Number {} is negative</p> 
            """
        else:
            page = """
            <h1>False</h1>
            <hr>
            <p>Number {} is <b><em>not</em></b> negative</p>
            """
        return page.format(typ)
    except ValueError:
        page = """
            <p><b>Number required at path's end</b></p>
            """
        return page

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments, based on the path.
    """
    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = some_func
    # args = ['25', '32']

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    funcs = {
        "positive": content_positive,
        "negative": content_negative
        }

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    """ app """
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
    return [body.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    SRV = make_server('localhost', 8080, application)
    SRV.serve_forever()
