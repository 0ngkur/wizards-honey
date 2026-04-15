import os
from flask import Flask, jsonify, Response
from services.guard import Guard
from services.generator import DataGenerator

# Mode Config: 'STANDARD' or 'PROXY'
HONEY_MODE = os.getenv('HONEY_MODE', 'STANDARD').upper()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Import mode-specific routes
if HONEY_MODE == 'PROXY':
    from modes.proxy.routes import proxy_bp
    app.register_blueprint(proxy_bp)
    SERVER_IDENTITY = '9router/0.3.89'
else:
    from modes.standard.routes import standard_bp
    app.register_blueprint(standard_bp)
    SERVER_IDENTITY = 'Apache/2.4.41 (Ubuntu)'

@app.after_request
def add_custom_headers(response):
    response.headers['Server'] = SERVER_IDENTITY
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.before_request
def monitor_requests():
    """Universal threat monitor."""
    Guard.analyze_request()

@app.route('/.env')
def exposed_env():
    """Universal bait for all modes."""
    Guard.log_incident('CRITICAL', 'Direct access to .env file')
    return Response(DataGenerator.get_fake_env(), mimetype='text/plain')

@app.route('/api/v1/health')
def health_check():
    return jsonify({"status": "ok", "mode": HONEY_MODE})

if __name__ == '__main__':
    print(f"[*] Wizard's Honey starting in {HONEY_MODE} mode...")
    app.run(host='0.0.0.0', port=5000, debug=True)
