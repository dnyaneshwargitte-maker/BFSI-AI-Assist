#!/bin/bash
# =============================================================================
# CloudifyOps BFSI Intelligence Platform - EC2 Bootstrap User Data Script
# Automatically provisions Docker, Docker Compose, PostgreSQL 15, FastAPI & Nginx
# =============================================================================

set -e

# Log all output to /var/log/user_data.log
exec > >(tee /var/log/user_data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "================================================================="
echo " Starting BFSI AI Assist EC2 Cloud-Init Provisioning..."
echo "================================================================="

# 1. Update system packages
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release git jq

# 2. Install Docker Engine & Docker Compose Plugin
if ! command -v docker &> /dev/null; then
    echo "[*] Installing Docker Engine..."
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ubuntu
fi

echo "[+] Docker installed successfully: $(docker --version)"

# 3. Create Application Root
APP_DIR="/opt/bfsi-ai-assist"
mkdir -p "$APP_DIR"
chown -R ubuntu:ubuntu "$APP_DIR"

# 4. Create .env configuration
cat << 'EOF' > "$APP_DIR/.env"
POSTGRES_USER=${postgres_user}
POSTGRES_PASSWORD=${postgres_password}
POSTGRES_DB=${postgres_db}
DB_HOST=postgres
DB_PORT=5432
AWS_DEFAULT_REGION=${aws_region}
EOF

chown ubuntu:ubuntu "$APP_DIR/.env"
chmod 600 "$APP_DIR/.env"

echo "================================================================="
echo " [SUCCESS] EC2 Docker Engine is ready at $APP_DIR"
echo " Deploy codebase using git clone or SCP and run: docker compose up -d"
echo "================================================================="

