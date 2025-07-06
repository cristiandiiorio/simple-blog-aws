import os

class Config:
    # Database and upload settings
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "uploads")
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # Admin credentials from environment variables
    # You will need to generate a password hash and set these
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    S3_BUCKET = os.environ.get("S3_BUCKET")

