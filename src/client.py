from bottle import get, run, static_file, route


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')

@get('/')
def index():
    return static_file('index.html', root="static/")


run(host='localhost', port=5000)
