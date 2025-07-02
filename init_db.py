# init_db.py
from app import create_app
from models import db

print("Connecting to the database and creating tables...")

# Create an application context to connect to the database
app = create_app()
with app.app_context():
    # This creates the tables based on your models.py
    db.create_all()

print("Database tables created successfully.")
