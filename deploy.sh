#!/bin/bash

# ==============================================================================
# ThinkCE Master Production Deployment & Security Script
# ==============================================================================
# This script handles:
# 1. Code Updates (Git)
# 2. Dependency Management
# 3. Database Migrations
# 4. Static Asset Collection
# 5. Cloudflare Security Hardening (Origin Cloaking)
# 6. Gunicorn Systemd Service
# 7. Service Refresh
# ==============================================================================

set -e # Exit on error

echo "🚀 Starting Integrated Deployment & Security Sync..."

# --- Configuration ---
PROJECT_DIR="/var/www/thinkce"
CLOUDFLARE_CONF="/etc/nginx/cloudflare_ips.conf"
VENV_PATH="$PROJECT_DIR/venv"

# 1. Pull latest code
echo "📥 [1/6] Pulling latest changes from git..."
git pull origin main

# 2. Update Dependencies
echo "📦 [2/6] Updating python dependencies..."
if [ ! -d "$VENV_PATH" ]; then
    echo "🔨 Creating virtual environment at $VENV_PATH..."
    python3 -m venv "$VENV_PATH"
fi
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# 3. Database & Migrations
echo "🗄️ [3/6] Running database migrations..."
python manage.py migrate --noinput

# 4. Static Assets
echo "🎨 [4/6] Collecting static files..."
python manage.py collectstatic --noinput

# 5. Permissions Management
echo "🔐 [5/8] Setting production permissions..."
sudo chown -R www-data:www-data "$PROJECT_DIR/media"
sudo chown -R www-data:www-data "$PROJECT_DIR/static"
sudo chown www-data:www-data "$PROJECT_DIR/db.sqlite3"
sudo chown www-data:www-data "$PROJECT_DIR"

sudo chmod -R 775 "$PROJECT_DIR/media"
sudo chmod -R 775 "$PROJECT_DIR/static"
sudo chmod 664 "$PROJECT_DIR/db.sqlite3"
sudo chmod 775 "$PROJECT_DIR"

# 6. SSL Directory & Certificate Setup
echo "🔑 [6/9] Checking SSL certificates..."
sudo mkdir -p /etc/ssl/thinkce

if [ ! -f "/etc/ssl/thinkce/cert.pem" ] || [ ! -f "/etc/ssl/thinkce/key.pem" ]; then
    echo "⚠️  SSL Certificates missing in /etc/ssl/thinkce/"
    
    echo "📝 Please paste your Cloudflare Origin Certificate (PEM) and press ENTER then Ctrl+D:"
    sudo bash -c 'cat > /etc/ssl/thinkce/cert.pem'
    
    echo "📝 Please paste your Cloudflare Private Key (PEM) and press ENTER then Ctrl+D:"
    sudo bash -c 'cat > /etc/ssl/thinkce/key.pem'
    
    sudo chmod 644 /etc/ssl/thinkce/*.pem
    echo "✅ SSL Certificates successfully installed."
else
    echo "✅ SSL Certificates already exist. Skipping input."
fi
sudo chmod 755 /etc/ssl/thinkce

# 7. Cloudflare Security (Origin Cloaking)
echo "🔒 [7/9] Hardening Cloudflare Security..."
echo "# Cloudflare IP Ranges (Auto-generated)" > temp_cf.conf
for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
    echo "set_real_ip_from $ip;" >> temp_cf.conf
    echo "allow $ip;" >> temp_cf.conf
done
for ip in $(curl -s https://www.cloudflare.com/ips-v6); do
    echo "set_real_ip_from $ip;" >> temp_cf.conf
    echo "allow $ip;" >> temp_cf.conf
done
echo "deny all;" >> temp_cf.conf

if [ -f "temp_cf.conf" ]; then
    sudo mv temp_cf.conf $CLOUDFLARE_CONF
    echo "✅ Cloudflare IP whitelist updated at $CLOUDFLARE_CONF"
fi

# 8. Nginx Configuration Setup (SSL Enabled)
echo "⚙️ [8/9] Updating Nginx configuration (HTTPS)..."
cat <<EOF > temp_nginx.conf
upstream thinkce_app {
    server unix:/run/thinkce/thinkce.sock;
}

server {
    listen 80;
    server_name thinkce.org www.thinkce.org;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name thinkce.org www.thinkce.org;

    ssl_certificate /etc/ssl/thinkce/cert.pem;
    ssl_certificate_key /etc/ssl/thinkce/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    include /etc/nginx/cloudflare_ips.conf;
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval';" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    location /static/ {
        alias /var/www/thinkce/static/;
    }

    location /media/ {
        alias /var/www/thinkce/media/;
    }

    location / {
        proxy_pass http://thinkce_app;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        real_ip_header CF-Connecting-IP;
    }
}
EOF

sudo mv temp_nginx.conf /etc/nginx/sites-available/thinkce
echo "✅ Nginx SSL config updated."

# 9. Gunicorn Systemd Service
echo "⚙️ [9/10] Configuring Gunicorn systemd service..."
sudo bash -c "cat <<EOF > /etc/systemd/system/thinkce.service
[Unit]
Description=Gunicorn instance to serve ThinkCE
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
RuntimeDirectory=thinkce
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$VENV_PATH/bin/gunicorn --workers 3 --bind unix:/run/thinkce/thinkce.sock thinkcesite.wsgi:application

[Install]
WantedBy=multi-user.target
EOF"

# 10. Service Refresh
echo "♻️ [10/10] Restarting Application Services..."
sudo systemctl daemon-reload
sudo systemctl enable thinkce.service
sudo systemctl restart thinkce.service
sudo nginx -t && sudo systemctl reload nginx

echo "✨ ThinkCE is now updated, secured (HTTPS), and configured!"

echo ""
echo "=============================================================================="
echo "🛡️  CLOUDFLARE & SSL SETUP WALKTHROUGH"
echo "=============================================================================="
cat <<EOF
To complete the security setup, please ensure the following:

1. SSL Certificates:
   - Generate an "Origin Certificate" in the Cloudflare Dashboard.
   - Save the certificate as: /etc/ssl/thinkce/cert.pem
   - Save the private key as: /etc/ssl/thinkce/key.pem
   - Ensure permissions: sudo chmod 644 /etc/ssl/thinkce/*.pem

2. SSL/TLS Configuration:
   - Set Mode to "Full (Strict)" in Cloudflare for end-to-end encryption.

3. DNS & Proxying:
   - Ensure all A/CNAME records for thinkce.org are "Proxied" (Orange Cloud).

4. Origin Cloaking (Active):
   - Direct access to your server IP on port 80/443 will be blocked for anyone
     not using Cloudflare IPs.

==============================================================================
EOF
