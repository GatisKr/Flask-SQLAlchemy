# app.py functions
from Database import db, User  # db - import the SQLAlchemy database instance
from flask import render_template, request, redirect


def ur_edit_fn(id_fn):
    user = db.session.get(User, id_fn)
    print("id_edit_fn(): User ID", id_fn, "edit form invoked")
    return render_template("user_edit.html", user=user, popup_message="Delete user?", popup_action="/user_edit", popup_id=user.id)


def ur_delete_fn(id_fn):
    user = db.session.get(User, id_fn)

    try:
        db.session.delete(user)
        db.session.commit()
        print("ur_delete_fn(): Successfully deleted User", id_fn)
        return redirect("/")

    except:
        return "User not found"


def ur_submit_fn(id_fn):
    user = db.session.get(User, id_fn)
    user.name = request.form["name"]
    user.password = request.form["password"]
    user.age = request.form["age"]
    user.isAdmin = bool(request.form.get("isAdmin", False))

    try:
        db.session.commit()  # save changes to database
        print(f"ur_submit_fn(): Successfully submitted User {id_fn} data")
        return redirect("/")

    except:
        return "Error changing User data"
