import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

db = SQLAlchemy(app)

class books(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer())
    borrowed = db.Column(db.Boolean()) 
    by_whom = db.Column(db.String(100))
    when = db.Column(db.Integer())

    def __init__(self, id, title, year, borrowed, by_whom, when):
        id = id
        title = title
        year = year
        borrowed = borrowed 
        by_whom = by_whom
        when = when

@app.route('/', methods=["GET", "POST"])
def home():
    if request.form:
        try:
            book = books(request.form['title'], request.form['year'], request.form['borrowed'], request.form['by_whom'], request.form['when'])
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    return render_template("home.html", books=books.query.all())

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        newyear = request.form.get("newyear")
        newborrowed = request.form.get("newborrowed")
        newby_whom = request.form.get("newby_whom")
        newwhen = request.form.get("newwhen")
        oldtitle = request.form.get("oldtitle")
        book = books.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        book.year = newyear
        book.borrowed = newborrowed
        book.by_whom = newby_whom
        book.when = newwhen
        
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = books.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)