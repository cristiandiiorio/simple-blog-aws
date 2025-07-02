# Simple blog for AWS

```bash
# 1. Create & activate venv
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip && pip install -r requirements.txt

# 3. Setup PostgreSQL (Debian/Ubuntu)
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql <<EOF
DROP DATABASE IF EXISTS photoblog;
CREATE USER testuser WITH PASSWORD 'testpass';
CREATE DATABASE photoblog OWNER testuser;
GRANT ALL PRIVILEGES ON DATABASE photoblog TO testuser;
EOF

# 4. Export env vars
export DATABASE_URL="postgresql://testuser:testpass@localhost:5432/photoblog"
export SECRET_KEY="a-very-long-and-random-secret-key"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('password'))")

# 5. Launch the app
gunicorn --workers 3 --bind 0.0.0.0:5000 "app:create_app()"
