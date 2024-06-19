from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from .views.sidebar_data import sidebar_data
    from .views.dgraph_data import dgraph_data

    app.register_blueprint(sidebar_data, url_prefix='/')
    app.register_blueprint(dgraph_data, url_prefix='/')

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
