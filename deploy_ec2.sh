#!/usr/bin/env bash
# =============================================================================
# CloudifyOps BFSI Intelligence Platform - EC2 Deployment Script
# Architecture: t3.medium (Ubuntu 22.04 LTS), Zero NAT Gateway ($0/mo), HTTPS Let's Encrypt
# =============================================================================

set -e

echo "================================================================="
echo " Starting CloudifyOps BFSI Setup on Amazon EC2 (t3.medium)"
echo "================================================================="

# 1. Update system packages
echo "[*] Updating Ubuntu packages..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release certbot python3-certbot-nginx

# 2. Install Docker & Docker Compose if not present
if ! command -v docker &> /dev/null; then
    echo "[*] Installing Docker Engine..."
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
fi

echo "[+] Docker version: $(docker --version)"

# 3. Discover EC2 Elastic IP and setup sslip.io wildcard domain
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com || curl -s https://api.ipify.org)
DASHED_IP=$(echo $PUBLIC_IP | tr '.' '-')
DEFAULT_DOMAIN="${DASHED_IP}.sslip.io"

echo "[*] Detected EC2 Public IP: ${PUBLIC_IP}"
echo "[*] Wildcard Zero-Approval HTTPS Domain: https://${DEFAULT_DOMAIN}"

# 4. Create .env file if missing
if [ ! -f .env ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
    sed -i "s/54-210-45-89.sslip.io/${DEFAULT_DOMAIN}/g" .env
fi

# 5. Launch Docker Compose Stack (PostgreSQL 15 + FastAPI Backend + Nginx)
echo "[*] Building and launching Docker Compose containers..."
sudo docker compose down || true
sudo docker compose up --build -d

# 6. Verify health
echo "[*] Awaiting services health check..."
sleep 8
sudo docker compose ps

echo "================================================================="
echo " [SUCCESS] CloudifyOps BFSI Contact Center is LIVE!"
echo " Web UI (Local/HTTP): http://${PUBLIC_IP}"
echo " For Free WebRTC HTTPS Microphone SSL:"
echo " Run: sudo certbot certonly --standalone -d ${DEFAULT_DOMAIN}"
echo "================================================================="

