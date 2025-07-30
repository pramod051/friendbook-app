from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

from .forms import LoginForm, RegisterForm, PostForm
from .models import db, User, Post
from . import login_manager

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('main.profile'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if not existing:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
        flash('Username already exists')
    return render_template('register.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = PostForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join('app/static/uploads', filename)
            form.image.data.save(filepath)
            image_path = filename
        post = Post(content=form.content.data, image=image_path, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.profile'))
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', form=form, posts=posts)

@main.route('/')
def home():
    return redirect(url_for('main.login'))
