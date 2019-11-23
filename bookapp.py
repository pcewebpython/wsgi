import re

from bookdb import BookDB

DB = BookDB()

base_url = 'localhost'
port = 8080

url = f"http://{base_url}:{port}"

def book(book_id):
    book_info = DB.title_info(book_id)
    if book_info is None:
        raise NameError
    response = f"""<html>
                    <h1>{book_info.get('title')}</h1>
                    <body><p><b>Author:</b> {book_info.get('author')}</p>
                    <p><b>Publisher:</b> {book_info.get('publisher')}</p>
                    <p><b>ISBN:</b> {book_info.get('isbn')}</p>
                    <p><a href="{url}">Back to List</a></p>
    """

    response += "</body></html>"

    return response


def books():
    response = """<h1>The Great Libary of Nemo</h1>
                  <ul>"""
    for title in DB.titles():
        response += f"""<li><a href="/books/{title['id']}">{title.get('title')}</a></li>"""

    response += "</ul>"
    
    return response

def resolve_path(path):
    funcs = {
        '': books,
        'books': books,
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

def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    try:
        if environ.get('PATH_INFO') == '/':
            response_body = books()
        
        elif environ.get('PATH_INFO') == '/books':
            response_body = books()
        
        elif environ.get('PATH_INFO').startswith('/books/id'):
            input_book_id = environ.get('PATH_INFO').split('/')[2]
            response_body = book(input_book_id)
        else:

            response_body = f"""<html>
                                {environ}
                                </html>
                                """ 
    except NameError:
        response_body = books()
    


    return [response_body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
