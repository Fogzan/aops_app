from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import LoginManager, login_user, logout_user, current_user
from app import db
from models import Users
from functools import wraps
from models import *

bp = Blueprint('auth', __name__)

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)

def load_user(user_id):
    user = db.session.execute(db.select(Users).filter_by(id=user_id)).scalar()
    return user

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('loginInput')
        password = request.form.get('passwordInput')
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            user = db.session.execute(db.select(Users).filter_by(login=login)).scalar()
            if user and user.check_password(password):
                login_user(user, remember=remember_me)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('login.html', action='login')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))

@bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        login = request.form.get('loginInput')
        password = request.form.get('passwordInput')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        if not(login and password and last_name and first_name and middle_name):
            flash('Введите все поля', 'danger')
            return render_template('login.html', action='create')

        try:
            new_user = Users(
            last_name = last_name,
            first_name = first_name,
            middle_name = middle_name,
            login = login,
            password_hash = generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно создан.', 'success')
            return redirect(url_for('index'))
        except:
            flash('Произошла ошибка', 'danger')
            return render_template('login.html', action='create')
    return render_template('login.html', action='create')