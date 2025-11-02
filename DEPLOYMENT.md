# Portfolio Deployment Guide: Production vs Development Modes

This guide walks you through deploying your portfolio with nginx routing, static ngrok URL, and proper environment configuration.

## Architecture Overview

```
GitHub Pages (Static Site)
         ↓
Static ngrok URL: https://valid-goblin-full.ngrok-free.app
         ↓
    Nginx (Port 8080) - CORS Handler
    ├── /lighting/* → Flask App (Port 5001) - Lighting Control
    └── /connect4/* → Flask App (Port 5002) - Connect4 Game
```

## Development vs Production Mode

### Development Mode Behavior
- **CORS Handling**: Flask apps handle CORS directly using Flask-CORS
- **Allowed Origins**: `localhost:3000`, `127.0.0.1:3000`, `https://halyconer.github.io`
- **Debug Mode**: Enabled with detailed error messages
- **Direct Access**: No nginx proxy needed - access Flask apps directly
- **Environment**: `DEVELOPMENT_MODE=true`, `FLASK_ENV=development`

### Production Mode Behavior  
- **CORS Handling**: nginx handles ALL CORS headers (Flask CORS disabled)
- **Allowed Origins**: Only `https://halyconer.github.io`
- **Reverse Proxy**: nginx routes requests to appropriate Flask apps
- **Environment**: `DEVELOPMENT_MODE=false`, `FLASK_ENV=production`
- **Security**: Origin validation and request filtering enabled

## File Structure & Usage

```
├── index.html              # Main portfolio with API calls
├── nginx.conf              # Production nginx configuration
├── backend/                # Lighting Control API
│   ├── app.py              # ✅ PRODUCTION Flask server (port 5001)
│   ├── app_new.py          # ❌ NOT USED (development artifact)
│   ├── requirements.txt    # Python dependencies
│   └── generate_stats.py   # Analytics generation
└── connectX/               # Connect4 Game API
    ├── app.py              # ✅ PRODUCTION Flask server (port 5002)
    ├── Connect4.py         # Game logic
    ├── minimax.py          # AI algorithm with alpha-beta pruning
    └── scoring.py          # Game evaluation functions
```

## Environment Configuration

### Required Environment Variables

**Backend (Lighting API):**
```bash
FLASK_ENV=production|development
DEVELOPMENT_MODE=true|false  
BULB_IP=192.168.1.210        # Yeelight bulb IP address
ALLOWED_ORIGIN=https://halyconer.github.io  # Production origin
```

**Key Behavior Differences:**
- `DEVELOPMENT_MODE=true`: Enables Flask CORS, allows localhost origins
- `DEVELOPMENT_MODE=false`: Disables Flask CORS, relies on nginx for CORS  
- `FLASK_ENV=development`: Enables debug mode with detailed error messages

## Local Development Setup

### Quick Development Start
```bash
# Clone repository
git clone https://github.com/Halyconer/Welcome-to-my-Portfolio.git
cd Welcome-to-my-Portfolio

# Start Lighting API (Terminal 1)
cd backend
pip install -r requirements.txt
export DEVELOPMENT_MODE=true
export FLASK_ENV=development
python app.py  # Runs on http://localhost:5001

# Start Connect4 API (Terminal 2)
cd connectX
poetry install  # or pip install -r requirements.txt
python app.py   # Runs on http://localhost:5002

# Open portfolio in browser (Terminal 3)
open index.html  # or start local web server
```

**Development Testing:**
- Lighting API: `http://localhost:5001/dev/status`
- Connect4 API: `http://localhost:5002/game_state`
- Frontend: Open `index.html` directly in browser

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

## API Endpoints

### Lighting API (`/lighting/`)
- `POST /lighting/set_brightness` - Set light brightness (1-100%)
  ```json
  {"brightness": 75}
  ```
- `GET /lighting/stats.json` - Usage statistics and analytics
- `GET /lighting/spotify_stats.json` - Music preferences data  
- `GET /lighting/dev/status` - Development endpoint (dev mode only)

### Connect4 API (`/connect4/`)  
- `POST /connect4/play` - Start new game
  ```json
  {"board": [[0,0,0,0,0,0,0],...], "turn": 0, "valid_cols": [0,1,2,3,4,5,6]}
  ```
- `POST /connect4/move` - Make a move (player + AI response)
  ```json
  {"column": 3}
  ```
- `GET /connect4/game_state` - Current game state

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

### CORS Issues (Most Common)

**Problem:** `Access-Control-Allow-Origin header contains multiple values`
```
Access-Control-Allow-Origin: https://halyconer.github.io, *
```

**Root Cause:** Both Flask and nginx are setting CORS headers, causing duplicates.

**Solution:**
1. **Check Flask apps have CORS disabled in production:**
   ```bash
   # In app.py files, ensure this logic exists:
   if DEVELOPMENT_MODE:
       CORS(app)  # Only enabled in development
   else:
       # CORS disabled - nginx handles it
   ```

2. **Verify nginx.conf has no duplicate location blocks:**
   ```bash
   # Check for duplicate /connect4/ blocks
   grep -n "location /connect4/" /etc/nginx/nginx.conf
   # Should only show ONE result
   ```

3. **Restart services after fixing:**
   ```bash
   sudo systemctl restart nginx
   sudo systemctl restart lighting-api connect4-api
   ```

### Production Deployment Fixes

**Fix Applied:** 
- `backend/app.py`: CORS disabled in production mode
- `connectX/app.py`: CORS disabled in production mode  
- `nginx.conf`: Single CORS configuration, no duplicates
- Origin restricted to `https://halyconer.github.io` only

### Check Service Status
```bash
sudo systemctl status lighting-api
sudo systemctl status connect4-api
sudo systemctl status nginx
```

### Check if Flask Apps Are Running
```bash
# Check for running Python/Flask processes
ps aux | grep -E "(python|flask)" | grep -v grep

# Check if ports are listening
sudo netstat -tlnp | grep -E ":500[12]"
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

1. **502 Bad Gateway - Flask apps not running** (Most Common)
   
   **Symptoms:** `ps aux | grep python` shows no Flask apps
   
   **Solutions:**
   ```bash
   # Option 1: Restart systemd services
   sudo systemctl restart lighting-api connect4-api
   
   # Option 2: Manual start for debugging
   cd /home/pi/portfolio/backend
   source venv/bin/activate
   python app.py &
   
   cd /home/pi/portfolio/connectX
   source .venv/bin/activate
   python app.py &
   
   # Option 3: Re-run setup script
   cd /home/pi/portfolio
   ./setup.sh
   ```

2. **Services exist but won't start**
   ```bash
   # Check service files exist
   ls -la /etc/systemd/system/*-api.service
   
   # Reload systemd and try again
   sudo systemctl daemon-reload
   sudo systemctl enable lighting-api connect4-api
   sudo systemctl start lighting-api connect4-api
   ```

3. **CORS Errors**: Check nginx CORS headers in config

4. **ngrok Browser Warning**: Ensure `ngrok-skip-browser-warning` header is set

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

## Quick Diagnostic Commands

If something isn't working, run these commands to diagnose:

```bash
# 1. Check if Flask apps are running
ps aux | grep -E "(python|flask)" | grep -v grep

# 2. Check if ports are listening
sudo netstat -tlnp | grep -E ":500[12]|:8080"

# 3. Check service status
sudo systemctl status lighting-api connect4-api nginx

# 4. Test local endpoints
curl http://localhost:5001/health 2>/dev/null && echo "✅ Lighting API OK" || echo "❌ Lighting API DOWN"
curl http://localhost:5002/game_state 2>/dev/null && echo "✅ Connect4 API OK" || echo "❌ Connect4 API DOWN"
curl http://localhost:8080/health 2>/dev/null && echo "✅ Nginx OK" || echo "❌ Nginx DOWN"
```

**Expected output when everything works:**
- 2-3 Python processes running
- Ports 5001, 5002, 8080 listening
- All services "active (running)"
- All curl tests return "OK"

## Production Monitoring & Maintenance

### Start Production Services
```bash
# Set production environment
export FLASK_ENV=production
export DEVELOPMENT_MODE=false
export ALLOWED_ORIGIN=https://halyconer.github.io

# Start lighting API (background)
cd ~/portfolio/backend && python app.py &

# Start Connect4 API (background)  
cd ~/portfolio/connectX && python app.py &

# Start nginx
sudo systemctl start nginx

# Setup ngrok tunnel
ngrok http --domain=valid-goblin-full.ngrok-free.app 8080
```

### Monitor Services
```bash
# Check Flask processes
ps aux | grep python | grep -v grep

# Check nginx status
sudo systemctl status nginx

# View nginx access logs
sudo tail -f /var/log/nginx/access.log

# View nginx error logs  
sudo tail -f /var/log/nginx/error.log

# Check Flask app logs (if using systemd services)
sudo journalctl -u lighting-api -f
sudo journalctl -u connect4-api -f

# Monitor SQLite database (lighting interactions)
sqlite3 ~/portfolio/backend/calls.db "SELECT * FROM calls ORDER BY timestamp DESC LIMIT 10;"
```

### Health Checks
```bash
# Test all endpoints
curl -s https://valid-goblin-full.ngrok-free.app/health
curl -s https://valid-goblin-full.ngrok-free.app/lighting/stats.json  
curl -s https://valid-goblin-full.ngrok-free.app/connect4/game_state

# Test CORS headers
curl -H "Origin: https://halyconer.github.io" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://valid-goblin-full.ngrok-free.app/lighting/set_brightness
```
