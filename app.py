from Database import db  # Import the SQLAlchemy database instance
from flask import Flask, render_template, request, redirect

app = Flask(__name__)  # Create a Flask application instance. This means that the main Flask launch file is app.py.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'  # Configure the database URI for SQLAlchemy to connect to
db.init_app(app)  # Initialize database with the app


@app.route("/")  # Route for the home page
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/add_post", methods=['POST', 'GET'])  # Route for creating new post
def add_post():
    if request.method == 'POST':  # If the request method is POST (from submission)
        title = request.form['title']  # Get the title from the form
        text = request.form['text']  # Get the text from the form
        from Database import Post  # Import the Post model form the Database module
        post = Post(title=title, text=text)  # Create a new Post object

        try:  # Add the new post to the database session and commit the changes
            db.session.add(post)
            db.session.commit()
            return redirect("/")  # Redirect to the home page
        except:
            return "Error while adding data"

    else:  # If the request method is GET (loading the form)
        return render_template("add_post.html")


@app.route('/all_posts')  # Define a route for displaying posts
def all_posts():  # Query all posts from the database using the Post model
    from Database import Post
    posts = Post.query.all()  # Retrieve all Post records from the database

    # Later add here post delete function

    return render_template('all_posts.html',
                           posts=posts)  # Render the 'all_posts.html' template and pass the retrieved posts to it


@app.route("/add_message", methods=['POST', 'GET'])
def add_message():
    fn = "add_message:"

    if request.method == 'POST':
        title = request.form["title"]
        messageText = request.form["messageText"]
        priority = request.form["priority"]

        from Database import Message
        message = Message(title=title, messageText=messageText, priority=priority)

        try:
            db.session.add(message)
            db.session.commit()
            print(fn, "Successfully added Message title, text, priority", title, messageText, priority)
            return redirect("/")

        except:
            return "Error while adding message to database"

    else:
        return render_template("add_message.html")


@app.route('/all_messages')  # Define a route for displaying posts
def all_messages():  # Query all posts from the database using the Post model
    from Database import Message
    messages = Message.query.all()  # Retrieve all Message records from the database

    # Later add here post delete function

    return render_template('all_messages.html', messages=messages)


@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    fn = "add_user:"
    if request.method == 'POST':
        # add is Admin field
        isAdmin = False

        if "isAdmin" in request.form:
            isAdmin = True

        name = request.form["name"]
        password = request.form["password"]
        age = request.form["age"]
        print(fn, "User variables:", name, password, age, isAdmin)

        from Database import User
        user = User(name=name, password=password, age=int(age), isAdmin=isAdmin)

        try:
            db.session.add(user)
            db.session.commit()  # saglabājam imaiņas
            print(fn, "Successfully added new user")
            return redirect("/")
        except:
            return "Error while adding user to database"

    else:
        return render_template("user_add.html")


@app.route("/all_users", methods=['POST', 'GET'])
def all_users():
    from Database import User
    fn = "/all_users:"

    n = 0
    n = n + 1
    print(n, "Started /all_users")

    allUsers = User.query.all()

    n = n + 1
    print(n, "Variable allUsers:")

    for i in allUsers:
        print(i)

    if request.method == 'POST':
        user_id_to_edit = request.form.get('edit_current_user')  # Get the ID of the user to

        n = n + 1
        print(n, fn, "user_id_to_edit =", user_id_to_edit)

        if user_id_to_edit:
            n = n + 1
            print(n, fn, "Triggered EDIT_USER command")

            user = User.query.get(user_id_to_edit)

            n = n + 1
            print(n, fn, "User variable:", user)

            if user:
                # Pass the user data to the edit_user.html template
                return render_template("user_edit.html", user=user)
            else:
                return "User not found"

        else:
            return "No user_id_to_edit"

    else:
        return render_template("users_all.html", allUsers=allUsers)


@app.route("/edit_user", methods=['POST', 'GET'])
def edit_my_user():
    from Database import User
    fn = "/edit_user:"
    n = 1
    print(n, fn, "Edit user invoked")

    if request.method == 'POST':
        user_id_to_delete = request.form.get('delete_user')  # Get the ID of the user to delete
        user_id_to_submit = request.form.get('submit_user')  # Get ID of the user to submit

        n = n + 1
        print(n, fn, "user_id_to_delete =", user_id_to_delete)
        n = n + 1
        print(n, fn, "user_id_to_submit =", user_id_to_submit)

        if user_id_to_delete:
            n = n + 1
            print(n, fn, "Triggered DELETE_USER command")

            user = User.query.get(user_id_to_delete)

            n = n + 1
            print(n, fn, "User variable:", user)

            try:
                db.session.delete(user)
                db.session.commit()

                n = n + 1
                print(n, fn, "Successfully deleted user entry")

                return redirect("/")
            except:
                return "User not found"

        elif user_id_to_submit:
            n = n + 1
            print(n, fn, "Triggered SUBMIT_USER command")

            user = User.query.get(user_id_to_submit)

            n = n + 1
            print(n, fn, "User variable:", user)
            n = n + 1
            print(n, fn, "Request form:", request.form)

            user.name = request.form["name"]
            user.password = request.form["password"]
            user.age = request.form["age"]
            user.isAdmin = bool(request.form.get("isAdmin", False))

            n = n + 1
            print(n, fn, "User variables:", user.name, user.password, user.age, user.isAdmin)
            n = n + 1
            print(n, fn, "isAdmin type:", type(user.isAdmin))

            try:
                db.session.commit()  # save changes to database

                n = n + 1
                print(n, fn, "Successfully changed user data")

                return redirect("/")
            except:
                return "Error while changing user data"

        else:
            return "No ID input"

    else:
        user = User.query.all()
        return render_template("user_edit.html", user=user)


if __name__ == '__main__':  # Run the Flask app if this script is executed directly
    app.run(debug=True)     # Saknses ceļiem jābūt pirms šīs rindas

