from flask import Flask, render_template, request, flash, send_from_directory
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import *

# Создание БД
create_models(app)

# Blueprint
from auth import bp as auth_bp, init_login_manager
app.register_blueprint(auth_bp)
init_login_manager(app)
# --------------


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
        )

def create_user():
    new_user = Users(
        last_name = "Фамилия",
        first_name = "Имя",
        middle_name = "Отчество",
        login = "moder",
        password_hash = generate_password_hash("Qwerty"),
        role_id = 2
    )
    db.session.add(new_user)
    db.session.commit()

    # 1. Админы:
    # Логин: fogzan Пароль: qwerty
    # Логин: psiho Пароль: Qwerty
    # 2. Модератор:
    # Логин: moder Пароль: Qwerty
    # 3. Пользователь:
    # Логин: user Пароль: Qwerty
