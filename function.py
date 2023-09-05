# app.py functions
from Database import db, User  # db - import the SQLAlchemy database instance
from flask import render_template, request, redirect


def id_edit_fn(id_fn):
    user = db.session.get(User, id_fn)
    print("id_edit_fn(): User ID", id_fn, "edit form invoked")
    return render_template("user_edit.html", user=user)


def id_delete_fn(id_fn):
    user = db.session.get(User, id_fn)

    try:
        db.session.delete(user)
        db.session.commit()
        print("id_delete_fn(): Successfully deleted User ID", id_fn)
        return redirect("/")

    except:
        return "User not found"


def id_submit_fn(id_fn):
    user = db.session.get(User, id_fn)
    user.name = request.form["name"]
    user.password = request.form["password"]
    user.age = request.form["age"]
    user.isAdmin = bool(request.form.get("isAdmin", False))

    try:
        db.session.commit()  # save changes to database
        print("id_submit_fn(): Successfully submitted User ID", id_fn, "data")
        return redirect("/")

    except:
        return "Error while changing user data"
