#!/bin/bash
# Run this ONCE on a fresh DigitalOcean Ubuntu droplet as root

set -e

# 1. Install Docker
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin git

# 2. Clone the repo
mkdir -p /opt/tam-api
git clone https://github.com/Waleedoff/tam-api.git /opt/tam-api
cd /opt/tam-api

# 3. Copy and fill the env file
cp .env.prod.example .env.prod
echo ">>> Edit /opt/tam-api/.env.prod with your real values, then re-run step 4"

# 4. Start services (run manually after editing .env.prod)
# docker compose -f docker-compose.prod.yml up -d

# 5. Get SSL certificate (replace yourdomain.com)
# docker compose -f docker-compose.prod.yml run --rm certbot certonly \
#   --webroot --webroot-path /var/www/certbot \
#   -d yourdomain.com --email you@email.com --agree-tos --no-eff-email

echo ">>> Done. Edit .env.prod, update nginx/nginx.conf with your domain, then start."
