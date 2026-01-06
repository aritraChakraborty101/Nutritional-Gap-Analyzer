from flask_login import login_required
from controllers import login, logout, index

def register_routes(app, login_manager):
    # Auth Routes
    app.route('/login', methods=['GET', 'POST'])(login)
    app.route('/logout')(login_required(logout))
    
    # App Routes
    app.route('/')(login_required(index))
