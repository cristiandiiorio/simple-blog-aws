python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

for db:

sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql

-- NOTE: If you have an existing 'photoblog' database from the old version,
-- you should drop it before creating the new one to apply schema changes.
-- DROP DATABASE photoblog;

CREATE USER testuser WITH PASSWORD 'testpass';
CREATE DATABASE photoblog OWNER testuser;
GRANT ALL PRIVILEGES ON DATABASE photoblog TO testuser;

export DATABASE_URL="postgresql://testuser:testpass@localhost:5432/photoblog"
export SECRET_KEY="a-much-more-secret-key-that-you-generate"
export ADMIN_USERNAME="your_admin_username"

export ADMIN_PASSWORD=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('password'))")

export DATABASE_URL="postgresql://testuser:testpass@localhost:5432/photoblog"

gunicorn --workers 3 --bind 0.0.0.0:5000 "app:create_app()"





source venv/bin/activate && \
export DATABASE_URL="postgresql://testuser:testpass@localhost:5432/photoblog" && \
export SECRET_KEY="a-very-long-and-random-secret-key" && \
export ADMIN_USERNAME="admin" && \
export ADMIN_PASSWORD=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('password'))") && \
gunicorn --workers 3 --bind 0.0.0.0:5000 "app:create_app()"
