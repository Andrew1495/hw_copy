from crypt import methods
from flask import Flask, redirect , render_template , Blueprint, request
from repositories import task_repository
from repositories import user_repository
from models.task import Task


tasks_blueprint = Blueprint("tasks", __name__)

@tasks_blueprint.route("/tasks")
def tasks():
    #  get the tasks from the database
    tasks = task_repository.select_all()
    # pass tasks to template
    return render_template("tasks/index.html", all_tasks=tasks)


# NEW
# GET /tasks/new
@tasks_blueprint.route("/tasks/new")
def new():
    users = user_repository.select_all()
    return render_template("tasks/new.html", all_users=users)

# CREATE
# POST /tasks

@tasks_blueprint.route("/tasks", methods=["POST"])
def create():
    description = request.form['description']
    user_id     = request.form['user_id']
    duration    = request.form['duration']
    completed   = request.form['completed']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed)
    task_repository.save(task)
    return redirect("/tasks")

# SHOW
# GET/tasks/<id>
@tasks_blueprint.route("/tasks/<id>")
def show(id):
    task = task_repository.select(id)
    return render_template("tasks/show.html", task=task)


# EDIT
# GET /tasks/<id>/edit

@tasks_blueprint.route("/tasks/<id>/edit" )
def edit(id):
    task = task_repository.select(id)
    user = user_repository.select_all()
    return render_template("/tasks/edit.html", task=task, all_users=user)

# UPDATE
# PUT /tasks/<id>
@tasks_blueprint.route("/tasks/<id>", methods=['POST'])
def update(id):
    description = request.form['description']
    user_id     = request.form['user_id']
    duration    = request.form['duration']
    completed   = request.form['completed']
    user = user_repository.select(user_id)
    task = Task(description, user, duration, completed, id) 
    task_repository.update(task)
    return redirect(f"/tasks/{id}")

# DELETE    
# POST /tasks/<id>/delete

@tasks_blueprint.route("/tasks/<id>/delete", methods=["POST"])
def delete(id):
    task_repository.delete(id)
    return redirect("/tasks")




# MARK INCOMPLETE

@tasks_blueprint.route("/tasks/<id>/mark-incomplete", methods=["POST"])
def mark_incomplete(id):
    task = task_repository.select(id)
    task.mark_incomplete()
    task_repository.update(task)
    return redirect("/tasks")


@tasks_blueprint.route("/tasks/<id>/complete", methods=["POST"])
def complete(id):
    task = task_repository.select(id)
    task.mark_complete()
    task_repository.update(task)
    return redirect("/tasks")
