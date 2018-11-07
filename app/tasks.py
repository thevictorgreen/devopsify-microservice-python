# tasks.py
from flask import Flask, Response, jsonify, request, make_response, url_for
from flask_restful import Api, Resource, abort, reqparse
import os
from models.models import TaskModel
import logging


# Populate tasks with dummy data
tasks = []
tasks.append(TaskModel(1,'Learn Python','Great Programming Language',False).to_dict())
tasks.append(TaskModel(2,'Build App','Time to create that product',False).to_dict())
tasks.append(TaskModel(3,'Get Paid','Monetize your skillset',False).to_dict())

# Setup parser for posted data
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')

# Grab a reference to the app logger
logger = logging.getLogger("app-logger")


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('task', id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


class TaskList(Resource):

    def get(self):
        logger.info("tasks-produced", extra={'tags': ['role:web', 'env:prod']})
        return jsonify({'tasks': [make_public_task(task) for task in tasks]})

    def post(self):
        args = parser.parse_args(strict=True)
        task = TaskModel(tasks[-1]['id'] + 1,args['title'],args['description'],False).to_dict()
        tasks.append(task)
        logger.info("new-task", extra={'tags': ['role:web', 'env:prod']})
        return jsonify({'task':task})


class Task(Resource):
    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            logger.error("task-not-found", extra={'tags': ['role:web', 'env:prod']})
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            logger.info("task-retrieved", extra={'tags': ['role:web', 'env:prod']})
            return jsonify({'task': task[0]})

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            logger.error("task-not-found", extra={'tags': ['role:web', 'env:prod']})
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            tasks.remove(task[0])
            logger.info("tasks-removed", extra={'tags': ['role:web', 'env:prod']})
            return jsonify({'result': True})

    def put(self, id):
        args = parser.parse_args(strict=True)
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            logger.error("task-not-found", extra={'tags': ['role:web', 'env:prod']})
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            task[0]["title"] = args['title']
            task[0]["description"] = args['description']
            logger.info("tasks-updated", extra={'tags': ['role:web', 'env:prod']})
            return jsonify({'task': task[0]})
