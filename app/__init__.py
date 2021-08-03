import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv ("DATABASE_URL")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import index, search, match
    app.register_blueprint(index.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(match.bp)    

    return app

if __name__  == "__main__":
    app = create_app()
    app.run(debug=True)