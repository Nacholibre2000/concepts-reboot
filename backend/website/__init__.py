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
    cors_origin = os.getenv('CORS_ORIGIN')
    CORS(app, resources={r"/*": {"origins": cors_origin}})

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from .views.curriculum_data import curriculum_data
    from .views.node_data import node_data

    app.register_blueprint(curriculum_data, url_prefix='/api')
    app.register_blueprint(node_data, url_prefix='/api')

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
