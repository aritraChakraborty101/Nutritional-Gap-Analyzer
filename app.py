from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
# New imports
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-to-something-secret' # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Where to redirect if user isn't logged in

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # Optional: Link todo to specific user
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Auth Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
            
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- App Routes ---

# 1. Protect the main route
@app.route('/')
@login_required 
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# 2. HTMX Error Handling
# If a user's session expires and they click a button, Flask normally redirects to /login.
# HTMX will try to put the /login HTML inside the button's target (ugly).
# This function forces HTMX to do a full browser redirect instead.
@login_manager.unauthorized_handler
def unauthorized():
    if request.headers.get('HX-Request'):
        response = Response()
        response.headers['HX-Redirect'] = url_for('login')
        return response
    return redirect(url_for('login'))

# ... Add your add_todo and delete_todo routes here (add @login_required to them too!)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)