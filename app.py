from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from config import Config
from controllers.send_excel_manager_controller import send_excel_bp
from repositories.database import db
import  psycopg2
from models.employee import Employee
from flask_migrate import Migrate
from controllers.generate_excel_controller import excel_bp
from controllers.generate_pdf_controller import pdf_bp
from controllers.send_pdf_employees_controller import send_pdf_bp
import flask_monitoringdashboard as dashboard

class AppFactory:
    def __init__(self):
        self.app=Flask(__name__)
        self.configure_app()
        self.configure_extensions()
        self.register_routes()
        self.configure_dashboard()

    def configure_app(self):
        self.app.config.from_object(Config)

    def configure_extensions(self):
        db.init_app(self.app)
        Migrate(self.app, db)
    def configure_dashboard(self):
        dashboard.config.init_from(file='config.cfg')
        dashboard.bind(self.app)
    def register_routes(self):
        self.app.register_blueprint(excel_bp)
        self.app.register_blueprint(pdf_bp)
        self.app.register_blueprint(send_pdf_bp)
        self.app.register_blueprint(send_excel_bp)

    def create_app(self):
          return self.app

app=AppFactory().create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
