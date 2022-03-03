import json
import sqlite3
from sqlite3 import Error

class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = []

    def all(self):
        return self.todos

    def get(self, id):
        todo = [todo for todo in self.all() if todo['id'] == id]
        if todo:
            return todo[0]
        return []

    def create(self, data):
        self.todos.append(data)
        self.save_all()

    def delete(self, id):
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        todo = self.get(id)
        if todo:
            index = self.todos.index(todo)
            self.todos[index] = data
            self.save_all()
            return True
        return False

class TodosSQL:

    def __init__(self):
        """
            -- zadanie table
        CREATE TABLE IF NOT EXISTS tasks (
            id integer PRIMARY KEY,
            title VARCHAR(250) NOT NULL,
            description TEXT,
            done VARCHAR(15) NOT NULL,
        );  
        """ 

    def create_connection(self, todos_db):
        conn = None
        try:
            conn = sqlite3.connect(todos_db)
            return conn
        except Error as e:
            print(e)

        return conn

    def execute_sql(self, conn, sql):
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def get(conn, status):
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

        rows = cur.fetchall()
        return rows

    def get_all(conn, table):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows

    def create(conn, todo):
        sql = '''INSERT INTO tasks(title, description, done)
                    VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, todo)
        conn.commit()
        return cur.lastrowid

    def delete(conn, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Deleted")

    def update(conn, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
                    SET {parameters}
                    WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

todos = TodosSQL()