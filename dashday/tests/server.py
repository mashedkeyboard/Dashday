# Tests the TurboGears2 server
from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server
import urllib.request
import threading
import time

class RootController(TGController):
    @expose()
    def index(self):
        return 'Hello World'

def testWebServer():
    print("Hosting server")

    config = AppConfig(minimal=True, root_controller=RootController())

    application = config.make_wsgi_app()

    httpd = make_server('', 62433, application)

    thr = threading.Thread(target=httpd.serve_forever)
    thr.start()

    print("Running test")
    page = urllib.request.urlopen('http://127.0.0.1:62433/')
    if page.read().decode() != "Hello World":
        raise RuntimeError("Server did not correctly host 'Hello World' page.")
    httpd.shutdown()