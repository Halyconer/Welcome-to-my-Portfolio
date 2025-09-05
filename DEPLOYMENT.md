# Portfolio Deployment Guide: Static Ngrok URL

This guide walks you through deploying your portfolio with nginx routing and a **static ngrok URL**.

## Architecture Overview

```
GitHub Pages (Static Site)
         ↓
Static ngrok URL: https://valid-goblin-full.ngrok-free.app
         ↓
    Nginx (Port 8080)
    ├── /lighting/* → Flask App (Port 5001)
    └── /connect4/* → Flask App (Port 5002)
```

## Prerequisites

- Raspberry Pi with internet connection
- ngrok account with **static domain** configured
- Both Flask apps working locally

## Step-by-Step Deployment

### 1. On Your Development Machine

✅ **Already Done:**
- Updated HTML to use static ngrok URL: `https://valid-goblin-full.ngrok-free.app`
- Created nginx configuration for path-based routing
- Created setup script for automated deployment

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

#### D. Start ngrok with Static Domain
```bash
# In a separate terminal - use your static domain
ngrok http --domain=valid-goblin-full.ngrok-free.app 8080
```

**Note:** Your static domain `valid-goblin-full.ngrok-free.app` is already configured in all frontend code, so no URL updates are needed!

### 3. Deploy to GitHub Pages

Since your frontend is already configured with the static ngrok URL, simply:
```bash
git add .
git commit -m "Deploy with static ngrok configuration"
git push origin main
```

Your GitHub Pages site will automatically use the correct API endpoints.

## Testing Your Setup

### Test nginx routing:
```bash
# Health check
curl https://valid-goblin-full.ngrok-free.app/health

# Test lighting API
curl -X POST https://valid-goblin-full.ngrok-free.app/lighting/set_brightness \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{"brightness": 50}'

# Test Connect4 API
curl https://valid-goblin-full.ngrok-free.app/connect4/game_state \
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

- ✅ **Static ngrok URL** - No need to update frontend code when restarting
- ✅ **Single ngrok tunnel** (fits free tier)
- ✅ **Centralized routing** via nginx
- ✅ **Automatic service restart** via systemd
- ✅ **Production-ready** with proper logging
- ✅ **Easy to maintain** - deploy once, works forever

## URL Structure

Your APIs are available at these **static endpoints**:
- Lighting: `https://valid-goblin-full.ngrok-free.app/lighting/set_brightness`
- Lighting Stats: `https://valid-goblin-full.ngrok-free.app/lighting/stats.json`
- Lighting Spotify: `https://valid-goblin-full.ngrok-free.app/lighting/spotify_stats.json`
- Connect4 Game: `https://valid-goblin-full.ngrok-free.app/connect4/play`
- Connect4 Move: `https://valid-goblin-full.ngrok-free.app/connect4/move`
- Connect4 State: `https://valid-goblin-full.ngrok-free.app/connect4/game_state`

## Quick Start Command

Once everything is set up, start your entire system with:
```bash
# Start ngrok with your static domain
ngrok http --domain=valid-goblin-full.ngrok-free.app 8080
```

That's it! Your portfolio will be live and accessible from anywhere. 🚀
