import os

SECRET_KEY = 'e341e6698cb20dd889d040a9be7d5fc129cb06255f349bd6ea3f901afe8d61b4'

# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2059_test:12345678@std-mysql.ist.mospolytech.ru/std_2059_test'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password123@mysql_db/app'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
