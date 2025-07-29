from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from config import Config
from repositories.database import db
import  psycopg2
from models.employee import Employee
from flask_migrate import Migrate
from controllers.excel_controller import excel_bp
from controllers.pdf_controller import pdf_bp

class AppFactory:
    def __init__(self):
        self.app=Flask(__name__)
        self.configure_app()
        self.configure_extensions()
        self.register_routes()

    def configure_app(self):
        self.app.config.from_object(Config)

    def configure_extensions(self):
        db.init_app(self.app)
        Migrate(self.app, db)

    def register_routes(self):
        self.app.register_blueprint(excel_bp)
        self.app.register_blueprint(pdf_bp)

    def create_app(self):
          return self.app

app=AppFactory().create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
