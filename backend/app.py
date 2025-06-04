from flask import Flask, request, jsonify
from flask_cors import CORS
from yeelight import Bulb
# import time
# from collections import defaultdict

# Configuration
BULB_IP = "192.168.1.210"
# API_KEY = "your-secret-key"  # Commented out for testing
ALLOWED_ORIGINS = [
    "https://halyconer.github.io",
    "https://halyconer.github.io/Welcome-to-my-Portfolio",
    "https://halyconer.github.io/Welcome-to-my-Portfolio/"
]

app = Flask(__name__)
# Allow all origins for testing - REMOVE IN PRODUCTION
CORS(app)

# Rate limiting disabled for testing
# request_times = defaultdict(list)
# RATE_LIMIT = 5
# RATE_WINDOW = 60

def get_bulb():
    try:
        bulb = Bulb(BULB_IP, auto_on=True)
        # Test connection
        bulb.get_properties()
        return bulb
    except Exception as e:
        print(f"Bulb connection failed: {e}")
        return None

# Rate limiting function commented out
# def is_rate_limited(client_ip):
#     now = time.time()
#     request_times[client_ip] = [
#         req_time for req_time in request_times[client_ip] 
#         if now - req_time < RATE_WINDOW
#     ]
#     
#     if len(request_times[client_ip]) >= RATE_LIMIT:
#         return True
#     
#     request_times[client_ip].append(now)
#     return False

# Security checks commented out for testing
# @app.before_request
# def check_auth():
#     if request.endpoint != 'set_brightness':
#         return
#     
#     # Check rate limiting
#     client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
#     if is_rate_limited(client_ip):
#         return jsonify({"error": "Rate limit exceeded. Please wait a moment."}), 429
#     
#     # Check API key
#     api_key = request.headers.get('X-API-Key') or request.headers.get('q7x!K3L9fN*zaP2vR1yW0hT8mB5sG4c')
#     if api_key != API_KEY:
#         return jsonify({"error": "Unauthorized"}), 401

@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    data = request.get_json(silent=True) or request.form.to_dict()
    value = data.get('brightness')
    
    if value is None:
        return jsonify({"error": "No brightness provided"}), 400

    try:
        br = int(value)
    except ValueError:
        return jsonify({"error": "Brightness must be an integer"}), 400

    if not 1 <= br <= 100:
        return jsonify({"error": "Brightness must be between 1 and 100"}), 400

    bulb = get_bulb()
    if bulb is None:
        return jsonify({"error": "Smart bulb is currently offline. Please try again later."}), 503

    try:
        bulb.set_brightness(br)
        print(f"Brightness set to {br}%")  # Debug logging
        
        return jsonify({
            "status": "success", 
            "brightness_set": br
        }), 200
        
    except Exception as e:
        print(f"Bulb control error: {e}")
        return jsonify({"error": f"Failed to control the bulb: {str(e)}"}), 500

@app.route('/health')
def health():
    bulb = get_bulb()
    return jsonify({
        "status": "online",
        "bulb_reachable": bulb is not None
    })

@app.route('/')
def home():
    return "Yeelight Controller is running (NO SECURITY - TESTING ONLY). Visit /health for status."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Debug enabled for testing