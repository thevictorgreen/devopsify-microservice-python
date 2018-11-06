from flask import Flask, Response, jsonify, request
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS
import pytest
from tasks import *


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    api = Api(app)

    @app.route('/ping')
    def ping():
        return jsonify(ping='pong')

    @app.route("/healthz",methods=["GET"])
    def healthz():
        return jsonify({"status":"SUCCESS"})

    api.add_resource(TaskList,"/tasks")
    api.add_resource(Task,"/tasks/<int:id>")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run("0.0.0.0",port=5000, debug=True)
