from flask import Flask, Response, jsonify, request
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS
from tasks import *


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


api.add_resource(TaskList,"/tasks")
api.add_resource(Task,"/tasks/<int:id>")


@app.route("/healthz",methods=["GET"])
def healthz():
    return jsonify({"status":"SUCCESS"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
