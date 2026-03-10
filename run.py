from flask import Flask
from flask_cors import CORS
from app.models.user_model import User
from app.models.resume_model import ResumeAnalysis
from app.config import Config
from app.extensions import db, jwt

from app.routes.auth_routes import auth_bp
from app.routes.resume_routes import resume_bp


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)

    return app


app = create_app()

with app.app_context():
    try:
        db.engine.connect()
        print("Database connected successfully")
        print("Before Creating tables....")
        db.create_all()
        print("After creating tables...")
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    app.run(debug=True)
