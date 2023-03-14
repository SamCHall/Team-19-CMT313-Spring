import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dotenv import DotEnv
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment
from flask_compress import Compress


# Initialisation and configuration:
# Flask app
app = Flask(__name__)
env = DotEnv(app)
if not bool(os.environ.get('DELOYMENT')):
    app.config['SECRET_KEY'] = 'development'
else:
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
cookie_security = True
app.config['SESSION_COOKIE_SECURE'] = cookie_security
app.config['REMEMBER_COOKIE_SECURE'] = cookie_security
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Database connection
if not bool(os.environ.get('DELOYMENT')):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aat.db')
db = SQLAlchemy(app)

# Form protection
csrf = CSRFProtect(app)

# Assets
from .assets import bundles
assets = Environment(app)
assets.register(bundles)

# Compression
Compress(app)

# Routes
from .main import routes

# Create database
from . import models
with app.app_context():
    db.create_all()
    # Comment/uncomment the below line to enable/disable test content generation for the database.
    # from . import create_db_test_data
