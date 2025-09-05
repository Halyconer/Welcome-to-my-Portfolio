# Portfolio Deployment Guide: Nginx + Single ngrok

This guide walks you through deploying your portfolio with nginx routing and a single ngrok tunnel.

## Architecture Overview

```
GitHub Pages (Static Site)
         ↓
    Single ngrok URL
         ↓
    Nginx (Port 8080)
    ├── /lighting/* → Flask App (Port 5001)
    └── /connect4/* → Flask App (Port 5002)
```

## Prerequisites

- Raspberry Pi with internet connection
- ngrok account and auth token
- Both Flask apps working locally

## Step-by-Step Deployment

### 1. On Your Development Machine

✅ **Already Done:**
- Updated HTML to use path-based routing
- Created nginx configuration
- Created setup script

### 2. On Your Raspberry Pi

#### A. Transfer Files
```bash
# Transfer your project to the Pi
scp -r /path/to/your/portfolio pi@your-pi-ip:/home/pi/portfolio
```

#### B. Install Python Dependencies
```bash
cd /home/pi/portfolio

# Install backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install Connect4 dependencies
cd connectX
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask-cors numpy pandas scipy
cd ..
```

#### C. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

#### D. Start ngrok
```bash
# In a separate terminal
ngrok http 8080
```

Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`)

### 3. Update Your Frontend

Update the `API_BASE_URL` in your HTML:
```javascript
const API_BASE_URL = 'https://your-actual-ngrok-url.ngrok-free.app'
```

### 4. Deploy to GitHub Pages

Commit and push your changes to deploy to GitHub Pages.

## Testing Your Setup

### Test nginx routing:
```bash
# Health check
curl https://your-ngrok-url.ngrok-free.app/health

# Test lighting API
curl -X POST https://your-ngrok-url.ngrok-free.app/lighting/set_brightness \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{"brightness": 50}'

# Test Connect4 API
curl https://your-ngrok-url.ngrok-free.app/connect4/game_state \
  -H "ngrok-skip-browser-warning: true"
```

## Troubleshooting

### Check Service Status
```bash
sudo systemctl status lighting-api
sudo systemctl status connect4-api
sudo systemctl status nginx
```

### View Logs
```bash
# Flask app logs
sudo journalctl -u lighting-api -f
sudo journalctl -u connect4-api -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Common Issues

1. **502 Bad Gateway**: Flask apps not running
   ```bash
   sudo systemctl restart lighting-api connect4-api
   ```

2. **CORS Errors**: Check nginx CORS headers in config

3. **ngrok Browser Warning**: Ensure `ngrok-skip-browser-warning` header is set

## Benefits of This Setup

- ✅ **Single ngrok tunnel** (fits free tier)
- ✅ **Centralized routing** via nginx
- ✅ **Automatic service restart** via systemd
- ✅ **Production-ready** with proper logging
- ✅ **Easy to maintain** single configuration

## URL Structure

Your APIs will be available at:
- Lighting: `https://your-ngrok-url/lighting/set_brightness`
- Lighting Stats: `https://your-ngrok-url/lighting/stats.json`
- Lighting Spotify: `https://your-ngrok-url/lighting/spotify_stats.json`
- Connect4 Game: `https://your-ngrok-url/connect4/play`
- Connect4 Move: `https://your-ngrok-url/connect4/move`
- Connect4 State: `https://your-ngrok-url/connect4/game_state`
