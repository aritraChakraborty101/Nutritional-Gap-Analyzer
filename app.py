from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes import register_routes
from controllers import unauthorized

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-to-something-secret' # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Where to redirect if user isn't logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HTMX Error Handling
# If a user's session expires and they click a button, Flask normally redirects to /login.
# HTMX will try to put the /login HTML inside the button's target (ugly).
# This function forces HTMX to do a full browser redirect instead.
@login_manager.unauthorized_handler
def handle_unauthorized():
    return unauthorized()

# Register all routes
register_routes(app, login_manager)

# ... Add your add_todo and delete_todo routes here (add @login_required to them too!)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)