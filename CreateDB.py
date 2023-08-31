from app import app, db  # This file is used to set up and initialize a Flask application with a SQLAlchemy database.

app.app_context().push()  # This line is creating an application context for Flask app and pushing it onto the context stack. An application context is necessary to properly handle database interactions within a Flask application. It ensures that the necessary resources and configurations are set up for the app to work correctly.

db.create_all()  # This line is invoking the create_all() method on db instance. The create_all() method is provided by SQLAlchemy and is used to create the database tables based on the models you've defined. It scans your models and generates the necessary SQL statements to create the corresponding tables in the database.

# This file renew database tables. Run on adding new database
