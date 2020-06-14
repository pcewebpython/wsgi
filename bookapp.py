import re
import traceback
from bookdb import BookDB

DB = BookDB()


def book(book_id):
    body = """<h1>{title}</h1>
    <table>
        <tr><th align='left'>Author:</th><td>{author}</td></tr>
        <tr><th align='left'>Publisher:</th><td>{publisher}</td></tr>
        <tr><th align='left'>ISBN:</th><td>{isbn}</td></tr>
    </table>
    <a href="/">Back to the list</a>
    """
    the_book = DB.title_info(book_id)
    if the_book is None:
        raise NameError
    return body.format(**the_book)


def books():
    all_books = DB.titles()
    body = ['<h1>My Bookself</h1>', '<ul>']
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append('</ul>')
    return '\n'.join(body)

def book_router(path):
    functions = {
        '': books,
        'book': book
    }
    # strip the last '/', then split the path into words by
    # "/"
    # so localhost:8080/ should be []
    # localhost:8080/book/id1/ should be [book] [id1]
    # localhost:8080/book/id2/ should be [book] [id2]
    path = path.strip('/').split('/')
    func_name = path[0]
    func_args = path[1:]
    try:
        func = functions[func_name]
    except KeyError:
        raise NameError
    finally:
        return func, func_args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = book_router(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = '404 Not Found'
        body = '<h1> 404 Not Found </h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1> Internal Server Error </h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-len', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
