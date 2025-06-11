from flask import Flask, request, jsonify
from flask_cors import CORS
from yeelight import Bulb

# Configuration
BULB_IP = "192.168.1.210"         # your bulb’s IP
API_KEY = "your-secret-key"       # keep this truly secret!
ALLOWED_ORIGIN = "https://halyconer.github.io/Welcome-to-my-Portfolio/"

app = Flask(__name__)

# Only allow CORS from your GitHub Pages domain on the /set_brightness route:
# CORS(app, resources={r"/set_brightness": {"origins": ALLOWED_ORIGIN}})
CORS(app)

def get_bulb():
    try:
        return Bulb(BULB_IP, auto_on=True)
    except Exception:
        return None

# @app.before_request
# def check_auth():
#     if request.endpoint != 'set_brightness':
#         return  
#     if request.headers.get(
#         'q7x!K3L9fN*zaP2vR1yW0hT8mB5sG4c'
#     ) != API_KEY:
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
		return jsonify({"error": "Bulb unreachable"}), 500

	try:
		bulb.set_brightness(br)
	except Exception as e:
		return jsonify({"error": f"Failed to set brightness: {e}"}), 500

	return jsonify({"status": "success", "brightness_set": br}), 200

@app.route('/')
def home():
	return "Yeelight Brightness Controller is running."

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=False)
