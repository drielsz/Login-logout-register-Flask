from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user
from app import app, login_manager, db
from app.models import User
import asyncio
from sqlalchemy.exc import IntegrityError

loop = asyncio.get_event_loop()

@app.route('/')    
def home():
    return jsonify(message="Hello World :)")

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        # if name and email and pwd:
        user = User(name, email, pwd)
        db.session.add(user)
        db.session.commit()

        # return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



app.run(debug=True)