import logging
import os
from flask import Flask
from flask import Blueprint
from flask import request
from .view import auth
from .view import seller
from .view import buyer
from .model.store import init_database

bp_shutdown = Blueprint("shutdown", __name__)


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        return False
    func()
    return True


@bp_shutdown.route("/shutdown")
def be_shutdown():
    ok = shutdown_server()
    if ok:
        return "Server shutting down..."
    return "Shutdown not supported in this server context"


def be_run():
    this_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(this_path)
    log_file = os.path.join(parent_path, "app.log")
    init_database('mongodb://localhost:27017', 'bookstoredb')

    logging.basicConfig(filename=log_file, level=logging.ERROR)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    app = Flask(__name__)
    app.register_blueprint(bp_shutdown)
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(seller.bp_seller)
    app.register_blueprint(buyer.bp_buyer)
    app.run(threaded=False, use_reloader=False)

if __name__ == "__main__":
    be_run()