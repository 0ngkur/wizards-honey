from flask import Blueprint, render_template, jsonify, request, Response
from services.guard import Guard
from services.generator import DataGenerator

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/api/auth/status')
def router_auth_status():
    """Vulnerable endpoint for CVE-2026-5842 emulation."""
    return jsonify({
        "authenticated": False,
        "mode": "proxy-only",
        "version": "0.3.89",
        "bypass_allowed": True
    })

@proxy_bp.route('/api/config')
def router_config():
    """Bait configuration file leakage with honey-data."""
    return jsonify({
        "providers": [
            {
                "name": "openai",
                "key": "sk-proj-wizard-decoy-key-" + "51Mz7xXLzq8",
                "models": ["gpt-4o", "gpt-3.5-turbo"]
            },
            {
                "name": "anthropic",
                "key": "sk-ant-wizard-decoy-key-" + "k2L8v6W1nQ",
                "models": ["claude-3-5-sonnet"]
            }
        ],
        "settings": {
            "port": 20128,
            "logLevel": "debug",
            "db_path": "~/.9router/db.json"
        }
    })

@proxy_bp.route('/v1/chat/completions', methods=['POST'])
def proxy_completion():
    """Trap for capturing real API requests and payloads."""
    payload = request.json
    Guard.log_incident('CRITICAL', f'Captured AI Proxy payload: {payload}')
    return jsonify({
        "id": "chatcmpl-wizard",
        "object": "chat.completion",
        "created": 1234567,
        "model": "gpt-4o",
        "choices": [{"message": {"role": "assistant", "content": "Wizard Shield: Access Denied. Your request has been logged by the security monitor."}, "finish_reason": "stop"}]
    })

@proxy_bp.route('/dashboard')
def router_dashboard():
    return render_template('proxy/9router_dash.html')
