from datetime import datetime
import hug

from todos import ToDo, session


@hug.get()
@hug.cli()
@hug.local()
def all():
    """Get all items on the to do list"""
    todos = session.query(ToDo).all()
    return {'To Dos': [todo.as_dict() for todo in todos]}


@hug.get()
@hug.cli()
@hug.local()
def all_by_category(category: hug.types.text):
    """Get all items in a category on a to do list"""
    todos = session.query(ToDo).filter_by(category=category).all()
    return {'To Dos': [todo.as_dict() for todo in todos]}


@hug.get()
@hug.cli()
@hug.local()
def all_by_assignee(assignee: hug.types.text):
    """Get all items on a to do list assigned to the given person"""
    todos = session.query(ToDo).filter_by(assignee=assignee).all()
    return {'To Dos': [todo.as_dict() for todo in todos]}


@hug.get()
@hug.cli()
@hug.local()
def by_id(id: hug.types.number):
    """Get the todo item by ID"""
    todo = session.query(ToDo).get(id)
    return {'To Do': todo.as_dict()}


@hug.get()
@hug.cli()
@hug.local()
def add(todo: hug.types.text, assignee: hug.types.text=None, category: hug.types.text=None):
    """Add an item to the to do list"""
    todo_db = ToDo(assignee=assignee,  todo=todo, category=category)
    session.add(todo_db)
    session.commit()
    return {'id': todo_db.id}


@hug.get()
@hug.cli()
@hug.local()
def delete(id: hug.types.number):
    """Delete the todo item by ID"""
    todo = session.query(ToDo).get(id)
    session.delete(todo)
    session.commit()
    if not session.query(ToDo).get(id):
        result = 'Success'
    else:
        result = 'Failure'
    return {'result': result}


@hug.get()
@hug.cli()
@hug.local()
def update(id: hug.types.number, todo: hug.types.text=None, assignee: hug.types.text=None, category:hug.types.text=None):
    """Delete the todo item by ID"""
    todo_db = session.query(ToDo).get(id)
    old_todo_db = todo_db.as_dict()
    if todo:
        todo_db.todo = todo
    if assignee:
        todo_db.assignee = assignee
    if category:
        todo_db.category = category
    todo_db.updated = datetime.utcnow()
    if not todo_db.as_dict() == old_todo_db:
        session.commit()
        return {'result': 'Success'}
    return {'result': 'No change'}


if __name__ == '__main__':
    all.interface.cli()
    all_by_category.interface.cli()
    by_id.interface.cli()
    add.interface.cli()
    delete.interface.cli()
    update.interface.cli()