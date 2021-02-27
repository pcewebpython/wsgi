import re

from bookdb import BookDB

DB = BookDB()

def resolve_path(path):
    funcs = {
        '': books,
        'book': book,
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def book(book_id):
    entry = DB.title_info(book_id)
    if not entry:
        raise NameError
    page = """
<h1>{title}</h1>
<table>
    <tr><th>Author</th><td>{author}</td></tr>
    <tr><th>Publisher</th><td>{publisher}</td></tr>
    <tr><th>ISBN</th><td>{isbn}</td></tr>
</table>
<a href="/">Back to the list</a>
"""

    return page.format(**entry)


def books():
    book_list = DB.titles()
    body = ["<h1>Book Index</h1>"]
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in book_list:
        body.append(item_template.format(**book))
    return '\n'.join(body)


def application(environ, start_response):
    # status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path=environ.get('PATH_INFO',None)
        if not path:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except:
        status = "500 Internal Server Error"
        body = "<h1>Vague Server Error</h1"
    finally:
        headers.append(("Content-Length", str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
