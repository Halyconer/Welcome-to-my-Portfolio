from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv() 

# Configuration from environment variables
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true'
BULB_IP = os.getenv('BULB_IP', '192.168.1.210')
ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', 'https://halyconer.github.io/Welcome-to-my-Portfolio/')

# Print configuration on startup
print(f"Flask Environment: {FLASK_ENV}")
print(f"Development Mode: {DEVELOPMENT_MODE}")
print(f"Allowed Origin: {ALLOWED_ORIGIN}")
print(f"Bulb IP: {BULB_IP}")

app = Flask(__name__)

# Configure CORS based on environment
if DEVELOPMENT_MODE:
    # In development mode, allow CORS from any origin
    CORS(app)
    print("CORS enabled for all origins (Development Mode)")
else:
    # In production mode, only allow CORS from your GitHub Pages domain
    CORS(app, resources={r"/set_brightness": {"origins": ALLOWED_ORIGIN}})
    print(f"CORS restricted to: {ALLOWED_ORIGIN}")

def get_bulb():
    try:
        from yeelight import Bulb  # Import here to avoid issues if library isn't installed
        return Bulb(BULB_IP, auto_on=True)
    except Exception:
        return None

@app.before_request
@cross_origin()
def check_auth():
    if request.endpoint != 'set_brightness':
         return  

    # Skip authentication checks in development mode
    if DEVELOPMENT_MODE:
        print("Development mode: Skipping origin/referer checks")
        return

    origin = request.headers.get("Origin")
    referer = request.headers.get("Referer")
    
    # origin and referrer are always automatically attached by browsers when making CORS requests
    # this should block against curl or postman in production mode
    if origin != ALLOWED_ORIGIN and (referer is None or not referer.startswith(ALLOWED_ORIGIN)):
        print(f"Request blocked - Origin: {origin}, Referer: {referer}")
        return jsonify({"error": "Request origin not allowed"}), 403

# SQL database setup
def log_call(brightness, status):
    conn = sqlite3.connect('calls.db') # Will be located on the pi

    # Define the table (if it doesn't exist)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            brightness INTEGER,
            status INTEGER
        )
    ''')
    conn.execute('INSERT INTO calls (brightness, status) VALUES (?, ?)', (brightness, status)) # Note that the tuple will replace the ? placeholders
    conn.commit()
    conn.close() # Release the file lock

# Endpoint to set brightness and log the call to the database
@app.route('/set_brightness', methods=['POST']) # Remember that with app.route, /set_brightness is the endpoint, not /set_brightness/
def set_brightness():
    data = request.get_json(silent=True) or request.form.to_dict() # Returns None if the request body is empty or not JSON
    value = data.get('brightness')
    
    if value is None:
        log_call(None, 400)  # Log the failure
        return jsonify({"error": "No brightness provided - Please let me know how you did that."}), 400

    try:
        br = int(value)
    except ValueError:
        log_call(None, 400)  # Log the failure
        return jsonify({"error": "Brightness must be an integer"}), 400

    if not 1 <= br <= 100:
        log_call(br, 400)  # Log the failure
        return jsonify({"error": "How the hell did you ask for something below 1 or above 100?"}), 400

    bulb = get_bulb()
    if bulb is None:
        log_call(br, 500)  # Log the failure
        return jsonify({"error": "Either my Bulb is dead or you have a bad connection."}), 500

    try:
        bulb.set_brightness(br)
        log_call(br, 200)  # Log the success
        return jsonify({"status": "success", "brightness_set": br}), 200
    except Exception as e:
        log_call(br, 500)  # Log the failure
        return jsonify({"error": f"For Adrian: {e}"}), 500

# Endpoint to serve the stats.json file
@app.route('/stats.json')
def serve_stats():
    try:
        return send_file('stats.json', mimetype='application/json')
    except FileNotFoundError:
        # Return empty stats if file doesn't exist yet
        return jsonify({
            "last_updated": datetime.now().isoformat(),
            "collection_period": "24_hours",
            "update_frequency": "daily", 
            "total_calls_all_time": 0,
            "avg_brightness_all_time": 0
        })

# Endpoint to serve the spotify stats file
@app.route('/spotify_stats.json')
def serve_spotify_stats():
    try:
        return send_file('spotify_top_artists.json', mimetype='application/json')
    except FileNotFoundError:
        # Return empty stats if file doesn't exist yet
        return jsonify({
            "last_updated_utc": datetime.utcnow().isoformat(),
            "artists": []
        })

# Development mode endpoint for testing
@app.route('/dev/status')
def dev_status():
    """Development endpoint to check current configuration"""
    if not DEVELOPMENT_MODE:
        return jsonify({"error": "This endpoint is only available in development mode"}), 404
    
    return jsonify({
        "flask_env": FLASK_ENV,
        "development_mode": DEVELOPMENT_MODE,
        "allowed_origin": ALLOWED_ORIGIN,
        "bulb_ip": BULB_IP,
        "request_origin": request.headers.get("Origin"),
        "request_referer": request.headers.get("Referer"),
        "user_agent": request.headers.get("User-Agent")
    })

if __name__ == '__main__': # Only to be run when this file is executed directly on the Pi
    debug_mode = DEVELOPMENT_MODE or FLASK_ENV == 'development'
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)
