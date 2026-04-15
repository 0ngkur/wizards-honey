from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from services.guard import Guard
from services.generator import DataGenerator
import os

app = Flask(__name__)
app.secret_key = "".join([os.urandom(8).hex() for _ in range(3)])

# Middleware for security monitoring
@app.before_request
def monitor_requests():
    """Analyze every incoming request for malicious patterns."""
    is_threat = Guard.analyze_request()
    # We don't block the request; we want to see what they do.
    pass

@app.route('/')
def index():
    """Main landing page - bait for automated scanners."""
    return render_template('index.html')

@app.route('/.env')
def exposed_env():
    """Fake environment file containing bait credentials."""
    Guard.log_incident('CRITICAL', 'Direct access to .env file')
    return Response(DataGenerator.get_fake_env(), mimetype='text/plain')

@app.route('/admin/dashboard')
def dashboard():
    """The prize for the attacker - a vulnerable-looking admin panel."""
    stats = DataGenerator.get_server_stats()
    logs = DataGenerator.generate_logs(8)
    return render_template('dashboard.html', stats=stats, logs=logs)

@app.route('/api/v1/system/status')
def system_status():
    """Interactive API endpoint for the dashboard."""
    return jsonify(DataGenerator.get_server_stats())

@app.route('/admin/terminal')
def terminal():
    """Fake 0-day shell access."""
    Guard.log_incident('CRITICAL', 'Opened internal debug terminal')
    return render_template('terminal.html')

@app.route('/api/v1/terminal/execute', methods=['POST'])
def terminal_execute():
    """Simulates command execution in the fake shell."""
    command = request.json.get('command', '').strip()
    Guard.log_incident('CRITICAL', f'Executed command: {command}')
    
    # Simple simulated responses
    responses = {
        'whoami': 'root',
        'id': 'uid=0(root) gid=0(root) groups=0(root)',
        'ls': 'app.py  config.py  logs/  services/  static/  templates/',
        'ls /etc': 'passwd  group  hosts  network  resolv.conf  ssh/',
        'cat /etc/passwd': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin',
        'uname -a': 'Linux staging-srv-04 5.15.0-101-generic #111-Ubuntu SMP Tue Feb 13 19:08:14 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux'
    }
    
    output = responses.get(command, f'bash: {command}: command not found')
    return jsonify({"output": output})

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Fake login panel to capture credentials."""
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        Guard.log_incident('HIGH', f'Authentication attempt: {user}:{pwd}')
        return render_template('login.html', error="Invalid credentials or account locked.")
    return render_template('login.html')

if __name__ == '__main__':
    # Running in debug mode creates a more 'vulnerable' look for hackers
    app.run(host='0.0.0.0', port=5000, debug=True)
