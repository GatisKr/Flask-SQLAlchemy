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

    # add here post delete function

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

    return render_template('message_all.html', messages=messages)


@app.route("/message_edit", methods=["POST"])
def message_edit():
    from Database import Message
    id_edit = request.form.get("edit_current_message")
    id_submit = request.form.get("submit_data")
    id_delete = request.form.get("delete_data")
    print(f"id_edit: {id_edit}; id_submit: {id_submit}; id_delete: {id_delete}")

    if id_edit:
        message = db.session.get(Message, id_edit)

    elif id_submit:
        message = db.session.get(Message, id_submit)
        message.title = request.form["title"]
        message.messageText = request.form["messageText"]
        message.priority = request.form["priority"]

        try:
            db.session.commit()
            print("id_submit: Successfully submitted Message changes")
            return redirect("/")

        except:
            return "Error submitting message data"

    elif id_delete:
        message = db.session.get(Message, id_delete)

        try:
            db.session.delete(message)
            db.session.commit()
            print("Successfully deleted Message")
            return redirect("/")

        except:
            return "Error deleting message"

    else:
        return "No message ID to edit"

    return render_template("message_edit.html", message=message, popup_message="Delete message?", popup_action="/message_edit", popup_id=message.id)


@app.route("/user_add", methods=['POST', 'GET'])
def user_add():
    fn = "/user_add:"
    if request.method == 'POST':
        isAdmin = False

        if "isAdmin" in request.form:
            isAdmin = True

        name = request.form["name"]
        password = request.form["password"]
        age = request.form["age"]
        print(fn, "User variables:", name, password, age, isAdmin)

        from Database import User

        try:
            user = User(name=name, password=password, age=int(age), isAdmin=isAdmin)
            db.session.add(user)
            db.session.commit()  # save changes to database
            print(fn, "Successfully added new User")
            return redirect("/")

        except:
            return "Error adding user to database"

    else:
        return render_template("user_add.html")


@app.route("/user_all", methods=['GET'])
def user_all():
    from Database import User
    users = User.query.all()
    print("/user_all: Fetched User data")
    return render_template("user_all.html", allUsers=users)


@app.route("/user_edit", methods=['POST'])
def user_edit():
    id_edit = request.form.get('edit_current_user')
    id_delete = request.form.get('delete_data')
    id_submit = request.form.get('submit_data')
    print(f"id_edit: {id_edit}; id_delete: {id_delete}; id_submit: {id_submit}")

    if id_edit:
        from function import ur_edit_fn
        id_fn = id_edit
        return ur_edit_fn(id_fn)

    elif id_delete:
        from function import ur_delete_fn
        id_fn = id_delete
        return ur_delete_fn(id_fn)

    elif id_submit:
        from function import ur_submit_fn
        id_fn = id_submit
        return ur_submit_fn(id_fn)

    else:
        return "No user_id_to_edit"


if __name__ == '__main__':  # Run the Flask app if this script is executed directly
    app.run(debug=True)     # All the root paths should be above
