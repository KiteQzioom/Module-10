from flask import Flask, jsonify
from models import todos
from flask import make_response, abort
from flask import request
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

todos_db = r'C:\Users\korek\Desktop\X\Edukacja\Python\Module 10\TODO\todos.db'

sql_create_projects_table = """
            -- zadanie table
        CREATE TABLE IF NOT EXISTS todos (
            id integer PRIMARY KEY,
            title VARCHAR(250) NOT NULL,
            description TEXT,
            done VARCHAR(15) NOT NULL,
        );  
        """ 

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    conn = todos.create_connection(todos_db)
    dane = todos.get_all(conn, 'todos')
    return str(dane)

@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get(todo_id):
    conn = todos.create_connection(todos_db)
    todo = todos.get(conn, todo_id)
    if not todo:
        abort(404)
    return str(todo)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    conn = todos.create_connection(todos_db)
    todo = todos.create(conn, 'todos')
    return str(todo)

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    conn = todos.create_connection(todos_db)
    todo = todos.update(conn, 'todos', todo_id)
    return str('deleted ' + todo)

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    conn = todos.create_connection(todos_db)
    todo = todos.update(conn, 'todos', todo_id)
    return str(todo)

if __name__ == "__main__":
    app.run(debug=True)