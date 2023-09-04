from Database import db  # Import the SQLAlchemy database instance
from flask import Flask, render_template, request, redirect

app = Flask(__name__)  # Create a Flask application instance. This means that the main Flask launch file is app.py.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'  # Configure the database URI for SQLAlchemy to connect to
db.init_app(app)  # Initialize database with the app


@app.route("/")  # Route for the home page
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/post_add", methods=['POST', 'GET'])  # Route for creating new post
def post_add():
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
        return render_template("post_add.html")


@app.route('/post_all')  # Define a route for displaying posts
def post_all():  # Query all posts from the database using the Post model
    from Database import Post
    posts = Post.query.all()  # Retrieve all Post records from the database

    # Later add here post delete function

    return render_template('post_all.html',
                           posts=posts)  # Render the 'post_all.html' template and pass the retrieved posts to it


@app.route("/message_add", methods=['POST', 'GET'])
def message_add():
    fn = "message_add:"

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
        return render_template("message_add.html")


@app.route('/message_all')  # Define a route for displaying posts
def message_all():  # Query all posts from the database using the Post model
    from Database import Message
    messages = Message.query.all()  # Retrieve all Message records from the database

    # Later add here post delete function

    return render_template('message_all.html', messages=messages)


@app.route("/user_add", methods=['POST', 'GET'])
def add_user():
    fn = "/user_add:"
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


@app.route("/user_all", methods=['POST', 'GET'])
def user_all():
    from Database import User
    fn = "/user_all:"
    n = 1
    print(n, fn, "Started /user_all")

    users = User.query.all()

    n += 1
    print(n, fn, "Variable users:")

    for i in users:
        print(i, end=" ")
    print()

    if request.method == 'POST':
        user_id_to_edit = request.form.get('edit_current_user')  # Get the ID of the user to

        n += 1
        print(n, fn, "user_id_to_edit =", user_id_to_edit)

        if user_id_to_edit:
            n += 1
            print(n, fn, "Triggered EDIT_USER command")

            user = User.query.get(user_id_to_edit)

            n += 1
            print(n, fn, "User variable:", user)

            if user:
                # Pass the user data to the edit_user.html template
                return render_template("user_edit.html", user=user)
            else:
                return "User not found"

        else:
            return "No user_id_to_edit"

    else:
        return render_template("user_all.html", allUsers=users)


@app.route("/user_edit", methods=['POST', 'GET'])
def user_edit():
    print("Invoked user_edit form")

    from function import submit_data
    submit_data()

    return redirect("/")


if __name__ == '__main__':  # Run the Flask app if this script is executed directly
    app.run(debug=True)     # All the root paths should be above

