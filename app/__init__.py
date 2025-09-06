# This script runs automatically when our `app` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask, g
from app import db
from datetime import datetime
from app.src.model.auth import load_logged_in_user, is_admin, is_editor

app = Flask(__name__, static_folder='static') # Place new Bootstrap files in /static

# Set the "secret key" that our app will use to sign session cookies. This can
# be anything.
# 
# Anyone with access to this key can pretend to be signed in as any user. In a
# real-world project, you wouldn't store this key in your source code. To learn
# about how to manage "secrets" like this in production code, check out
# https://blog.gitguardian.com/how-to-handle-secrets-in-python/
#
# For the purpose of your assignments, you DON'T need to use any of those more
# advanced and secure methods: it's fine to store your secret key in your
# source code like we do here.
app.secret_key = 'Example Secret Key (CHANGE THIS TO YOUR OWN SECRET KEY!)'

# Set up database connection.
from app import connect
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)


@app.before_request
def before_request():
    load_logged_in_user()

@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'current_user': getattr(g, "user", None),
        'can_edit': is_editor(),
        'can_delete': is_admin(),
        'is_admin': is_admin(),
        'is_editor': is_editor()
    }

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.context_processor
def inject_datetime():
    return {"datetime": datetime}


# Include all modules that define our Flask route-handling functions.
from app.src.route import centrelist
from app.src.route import centredetails
from app.src.route import centrecreate
from app.src.route import citysummary
from app.src.route import auth
from app.src.route import staff_admin
