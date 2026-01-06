from flask import render_template, request, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user
from models import User, Todo

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

def logout():
    logout_user()
    return redirect(url_for('login'))

def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

def unauthorized():
    if request.headers.get('HX-Request'):
        response = Response()
        response.headers['HX-Redirect'] = url_for('login')
        return response
    return redirect(url_for('login'))
