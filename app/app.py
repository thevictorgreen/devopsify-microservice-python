# app.py
from flask import Flask, Response, jsonify, request
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS
import pytest
import datetime, logging, sys, json_logging
from tasks import *
from helpers.middleware import setup_metrics
import prometheus_client


CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


def create_app():
    app = Flask(__name__)
    setup_metrics(app)

    json_logging.ENABLE_JSON_LOGGING = True
    json_logging.init(framework_name='flask')
    json_logging.init_request_instrument(app)
    logger = logging.getLogger("app-logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    api = Api(app)

    @app.route('/ping')
    def ping():
        logger.info("pinged", extra={'tags': ['role:web', 'env:prod']})
        return jsonify(ping='pong')

    @app.route("/healthz",methods=["GET"])
    def healthz():
        logger.info("health-checked", extra={'tags': ['role:web', 'env:prod']})
        return jsonify({"status":"SUCCESS"})

    @app.route('/metrics')
    def metrics():
        return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    api.add_resource(TaskList,"/tasks")
    api.add_resource(Task,"/tasks/<int:id>")

    return app


if __name__ == "__main__":
    app = create_app()
    # Local Development
    # To Serve With Flask
    # python app.py
    #app.run("0.0.0.0",port=5000, debug=True)
    # Production
    # To Serve With Gunicorn WSGI
    # gunicorn -w 4 --bind 0.0.0.0 --access-logfile - wsgi:application
    app.run("0.0.0.0", debug=False)
