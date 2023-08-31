# This file contains functions for app.py
from Database import db  # Import the SQLAlchemy database instance
from flask import render_template, request, redirect


def submit_data():
    from Database import User

    if request.method == 'POST':
        id_to_delete = request.form.get('delete_data')  # Get user ID to delete
        id_to_submit = request.form.get('submit_data')  # Get user ID to submit

        if id_to_delete:
            user = User.query.get(id_to_delete)

            try:
                db.session.delete(user)
                db.session.commit()
                return redirect("/")

            except:
                return "User not found"

        elif id_to_submit:
            user = User.query.get(id_to_submit)

            user.name = request.form["name"]
            user.password = request.form["password"]
            user.age = request.form["age"]
            user.isAdmin = bool(request.form.get("isAdmin", False))

            try:
                db.session.commit()  # save changes to database
                return redirect("/")

            except:
                return "Error while changing user data"

        else:
            return "No ID input"

    else:
        user = User.query.all()
        return render_template("user_edit.html", user=user)
