import re
import traceback

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    page = """
<h1>{title}</h1>
<table>
    <tr><th>Author</th><td>{author}</td></tr>
    <tr><th>Publisher</th><td>{publisher}</td></tr>
    <tr><th>ISBN</th><td>{isbn}</td></tr>
</table>
<a href="/">Back to the list</a>
"""
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    return page.format(**book)

def books():
    book_list = DB.titles()
    body = ['<h1>My Bookshelf</h1>', '<ul>']
    title = '<li><a href="/book/{id}">{title}</a></li>'
    for book in book_list:
        body.append(title.format(**book))
    body.append('</ul>')
    return '\n'.join(body)

def resolve_path(path):
    funcs = {'': books, 'book': book}
    path = path.strip('/').split('/')
    args = path[1:]

    try:
        func = funcs[path[0]]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    # Try/except block to determine what the body and status will be
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
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
