from flask import Flask, Response, jsonify, request, make_response, url_for
from flask_restful import Api, Resource, abort, reqparse
import os

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')



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
        return jsonify({'tasks': [make_public_task(task) for task in tasks]})

    def post(self):
        args = parser.parse_args(strict=True)
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return jsonify({'task':task})


class Task(Resource):
    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return jsonify({'task': task[0]})

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            tasks.remove(task[0])
            return jsonify({'result': True})

    def put(self, id):
        args = parser.parse_args(strict=True)
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            task[0]["title"] = args['title']
            task[0]["description"] = args['description']
            return jsonify({'task': task[0]})
