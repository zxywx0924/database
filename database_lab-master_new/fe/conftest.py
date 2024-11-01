import requests
import threading
from urllib.parse import urljoin
from be import serve
from fe import conf

thread: threading.Thread = None


def run_backend():
    # rewrite this if rewrite backend
    serve.be_run()


def pytest_configure(config):
    global thread
    print("frontend begin test")
    thread = threading.Thread(target=run_backend, daemon=True)  
    thread.start()

def pytest_unconfigure(config):
    url = urljoin(conf.URL, "shutdown")
    try:
        requests.get(url, timeout=3) 
    except Exception:
        pass
    if thread is not None:
        thread.join(timeout=5)  
    print("frontend end test")
