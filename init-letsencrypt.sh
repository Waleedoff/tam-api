#!/bin/bash
set -e

DOMAIN="ruyahub.club"
EMAIL="waled988@hotmail.com"
COMPOSE_FILE="docker-compose.prod.yml"
NGINX_CONF="nginx/nginx.conf"

echo "==> Switching to HTTP-only nginx config for initial cert issuance..."
cp "$NGINX_CONF" "${NGINX_CONF}.bak"
cp nginx/nginx-init.conf "$NGINX_CONF"

restore_config() {
    if [ -f "${NGINX_CONF}.bak" ]; then
        cp "${NGINX_CONF}.bak" "$NGINX_CONF"
        rm -f "${NGINX_CONF}.bak"
    fi
}
trap 'echo "Error — restoring nginx config"; restore_config' ERR

echo "==> Starting nginx (HTTP only)..."
docker compose -f "$COMPOSE_FILE" up -d nginx
sleep 3

echo "==> Requesting certificate from Let's Encrypt..."
docker compose -f "$COMPOSE_FILE" run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN"

echo "==> Restoring full SSL nginx config..."
restore_config
trap - ERR

echo "==> Reloading nginx with SSL..."
docker compose -f "$COMPOSE_FILE" exec nginx nginx -s reload

echo "==> Starting remaining services..."
docker compose -f "$COMPOSE_FILE" up -d

echo ""
echo "Done! ruyahub.club is now serving HTTPS."
echo "To renew: docker compose -f docker-compose.prod.yml run --rm certbot renew && docker compose -f docker-compose.prod.yml exec nginx nginx -s reload"
