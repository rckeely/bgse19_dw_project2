from gevent.pywsgi import WSGIServer
from app import app

PORT = 5000

print("Running flask on : http://localhost:{}".format(PORT))

http_server = WSGIServer(('', PORT), app.server)
http_server.serve_forever()
