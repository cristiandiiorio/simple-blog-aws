import os
import boto3
from botocore.exceptions import NoCredentialsError
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)

from config import Config
from models import db, Post, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.getenv("SECRET_KEY", "a-very-secret-key-that-you-should-change")

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    s3 = boto3.client("s3")
    S3_BUCKET = app.config["S3_BUCKET"]


    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    def allowed_file(filename):
        return (
            "." in filename and
            filename.rsplit(".", 1)[1].lower()
            in app.config["ALLOWED_EXTENSIONS"]
        )

    # --- Public Routes ---
    @app.route("/")
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", posts=posts)

    # --- Authentication Routes ---
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('create_post'))

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            admin_user = app.config["ADMIN_USERNAME"]
            admin_pass_hash = app.config["ADMIN_PASSWORD"]

            if not admin_pass_hash:
                flash("Error: The ADMIN_PASSWORD is not configured on the server.")
                return redirect(url_for('login'))

            if username == admin_user and check_password_hash(admin_pass_hash, password):
                user = User(id=admin_user)
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for("create_post"))
            else:
                flash("Invalid username or password.")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "success")
        return redirect(url_for("index"))

    # --- Admin/Protected Routes ---
    @app.route("/create", methods=["GET", "POST"])
    @login_required
    def create_post():
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            body = request.form.get("body", "").strip()
            file = request.files.get("image")

            if not title or not body:
                flash("Title and body are required.")
                return redirect(request.url)

            image_url = None
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    try:
                        s3.upload_fileobj(
                            file,
                            S3_BUCKET,
                            filename,
                            ExtraArgs={
                                "ContentType": file.content_type
                            }
                        )
                        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
                    except NoCredentialsError:
                        flash("AWS credentials not available.")
                        return redirect(request.url)
                    except Exception as e:
                        flash(f"An error occurred: {e}")
                        return redirect(request.url)

                else:
                    flash("Invalid file type")
                    return redirect(request.url)

            post = Post(title=title, body=body, image_url=image_url)
            db.session.add(post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("index"))
        return render_template("create_post.html")

    return app