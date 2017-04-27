#!flask/bin/python
from app import app
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 3500), app)
http_server.serve_forever()
app.run(debug=True)
