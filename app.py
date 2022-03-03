from flask import Flask, jsonify
from models import todos
from flask import make_response, abort
from flask import request
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

todos_db = r'C:\Users\korek\Desktop\X\Edukacja\Python\Module 10\TODO\todos.sqbpro'

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1(todos_db):
    conn = todos.create_connection(todos_db)
    dane = todos.get_all(conn, 'tasks')
    return dane

@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return todo

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

#???????
@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todos.create(todo)
    return todo

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return todos

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        'done': data.get('done', todo['done'])
    }
    todos.update(todo_id, todo)
    return todo

if __name__ == "__main__":
    app.run(debug=True)