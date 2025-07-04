# init_db.py
import os
from urllib.parse import urlparse, urlunparse
from sqlalchemy import create_engine, text
from app import create_app
from models import db

# 1) Grab your full DATABASE_URL from env, parse it
raw_url = os.environ["DATABASE_URL"]
parsed = urlparse(raw_url)
dbname   = parsed.path.lstrip("/")              # e.g. "photoblog"

# 2) Build a URL that points *to* the default 'postgres' database
admin_path   = "/postgres"
admin_parsed = parsed._replace(path=admin_path)
admin_url    = urlunparse(admin_parsed)

# 3) Connect to 'postgres' and CREATE DATABASE if needed
print(f"Ensuring database '{dbname}' exists…")
admin_engine = create_engine(admin_url)
with admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
    try:
        conn.execute(text(f"CREATE DATABASE {dbname}"))
        print(f"✔ Database '{dbname}' created")
    except Exception as e:
        # typically "already exists", which is fine
        print(f"⚠ Could not create database: {e}")

# 4) Now boot your Flask app and create the tables
print("Creating tables in the application DB…")
app = create_app()
with app.app_context():
    db.create_all()
print("🎉 Tables created successfully.")
