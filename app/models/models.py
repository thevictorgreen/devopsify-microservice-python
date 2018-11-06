class TaskModel:
    'Base Class for all Tasks'

    def __init__(self, id, title, description, done):
        self.id = id
        self.title = title
        self.description = description
        self.done = done

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'done': self.done}
