from flask import Blueprint, render_template, jsonify, request, Response
from services.guard import Guard
from services.generator import DataGenerator

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/api/auth/status')
def router_auth_status():
    return jsonify({
        "authenticated": False,
        "mode": "proxy-only",
        "version": "0.3.89",
        "bypass_allowed": True
    })

@proxy_bp.route('/api/config')
def router_config():
    env = DataGenerator.get_fake_env().split('\n')
    return jsonify({
        "providers": [
            {"name": "openai", "key": "sk-proj-wizard-" + env[0].split('=')[1], "models": ["gpt-4o"]},
            {"name": "anthropic", "key": "sk-ant-wizard-" + env[1].split('=')[1], "models": ["claude-3-5"]}
        ]
    })

@proxy_bp.route('/v1/chat/completions', methods=['POST'])
def proxy_completion():
    payload = request.json
    Guard.log_incident('CRITICAL', f'Captured AI Proxy payload: {payload}')
    return jsonify({"choices": [{"message": {"content": "Access Denied by Wizard Shield."}}]})

@proxy_bp.route('/dashboard')
def router_dashboard():
    return render_template('proxy/9router_dash.html')
