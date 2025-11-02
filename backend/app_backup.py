from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
import sqlite3
from dotenv import load_dotenv
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv() 

# Configuration
BULB_IP = "192.168.1.210"         # your bulb’s IP
ALLOWED_ORIGIN = "https://halyconer.github.io/Welcome-to-my-Portfolio/"

app = Flask(__name__)

# Only allow CORS from your GitHub Pages domain on the /set_brightness route:
CORS(app, resources={r"/set_brightness": {"origins": ALLOWED_ORIGIN}})

def get_bulb():
    try:
        return Bulb(BULB_IP, auto_on=True)
    except Exception:
        return None

@app.before_request
@cross_origin()
def check_auth():
    if request.endpoint != 'set_brightness':
         return  

    origin = request.headers.get("Origin")
    referer = request.headers.get("Referer")
    
    # origin and referrer are always automatically attached by browsers when making CO requests so this should block agains curl or postman
    if origin != ALLOWED_ORIGIN  and (referer is None or not referer.startswith(ALLOWED_ORIGIN)):
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
        return jsonify({"How the hell did you ask for something below 1 or above 100?"}), 400

    bulb = get_bulb()
    if bulb is None:
        log_call(br, 500)  # Log the failure
        return jsonify({"Either my Bulb is dead or you have a bad connection."}), 500

    try:
        bulb.set_brightness(br)
        log_call(br, 200)  # Log the success
        return jsonify({"status": "success", "brightness_set": br}), 200
    except Exception as e:
        log_call(br, 500)  # Log the failure
        return jsonify({"error for some reason": f"For Adrian: {e}"}), 500

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

if __name__ == '__main__': # Only to be run when this file is executed directly on the Pi
	app.run(host='0.0.0.0', port=5001, debug=False)




