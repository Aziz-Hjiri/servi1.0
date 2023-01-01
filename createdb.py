from app import  app
from database import db


# Create a Flask application context
with app.app_context():
    db.create_all()