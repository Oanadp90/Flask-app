from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from .models import Todo
from . import db

my_view = Blueprint("my_view", __name__)

reviews = []

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    print(todo_list)
    message = request.args.get('message', None)
    return render_template("index.html", todo_list=todo_list, message=message)

@my_view.route("/page2")
def page2():
    return render_template("page2.html")
    # return"<h1>Here you will find pictures for each task.</h1>"

@my_view.route('/page3')
def page3():
    return render_template('page3.html', reviews=reviews)

@my_view.route('/submit_review', methods=['POST'])
def submit_review():
    rating = request.form['rating']
    text = request.form['review']
    reviews.append({'rating': rating, 'text': text})
    return redirect(url_for('my_view.page3'))


@my_view.route("/add", methods=["GET","POST"])
def add():
    try:
        task = request.form.get("task")
        if Todo.query.filter_by(task=task).first() is not None:
            return redirect(url_for("my_view.home", message="Task already exists"))
        else:
            new_todo = Todo(task=task)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("my_view.home", message="Task added successfully"))
    except:
        return redirect(url_for("my_view.home", message="There was an error adding your task. Please try again"))


@my_view.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        todo.complete = not todo.complete  # Toggle the completion status
        db.session.commit()
    return redirect(url_for("my_view.home"))


@my_view.route("/delete/<todo_id>", methods=["POST", "GET"])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home", message="Task deleted successfully"))