#!/bin/bash

# Portfolio Nginx + ngrok Setup Script
# Run this script on your Raspberry Pi

echo "🚀 Setting up Portfolio with Nginx + Single ngrok tunnel..."

# Check if running on Pi
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing nginx..."
    sudo apt update
    sudo apt install -y nginx
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok
    echo "🔑 Please run 'ngrok config add-authtoken YOUR_TOKEN' with your ngrok auth token"
fi

# Copy nginx config
echo "📝 Setting up nginx configuration..."
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    sudo systemctl restart nginx
    sudo systemctl enable nginx
else
    echo "❌ Nginx configuration error"
    exit 1
fi

# Create systemd services for Flask apps
echo "🔧 Creating systemd services..."

# Lighting API service
sudo tee /etc/systemd/system/lighting-api.service > /dev/null <<EOF
[Unit]
Description=Portfolio Lighting API
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=$PWD/backend
Environment=PATH=$PWD/backend/venv/bin
ExecStart=$PWD/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Connect4 API service
sudo tee /etc/systemd/system/connect4-api.service > /dev/null <<EOF
[Unit]
Description=Portfolio Connect4 API
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=$PWD/connectX
Environment=PATH=$PWD/connectX/.venv/bin
ExecStart=$PWD/connectX/.venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable lighting-api connect4-api
sudo systemctl start lighting-api connect4-api

echo "📊 Checking service status..."
sudo systemctl status lighting-api --no-pager
sudo systemctl status connect4-api --no-pager

echo "🌐 Starting ngrok tunnel on port 8080..."
echo "Run this command in a separate terminal:"
echo "ngrok http 8080"

echo ""
echo "✅ Setup complete!"
echo "📋 Next steps:"
echo "1. Run 'ngrok http 8080' in a separate terminal"
echo "2. Update the API_BASE_URL in your HTML with the ngrok URL"
echo "3. Deploy your HTML to GitHub Pages"
echo ""
echo "🔍 Check logs with:"
echo "   sudo journalctl -u lighting-api -f"
echo "   sudo journalctl -u connect4-api -f"
