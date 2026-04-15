import logging
import json
import os
from datetime import datetime
from flask import request

LOG_DIR = 'logs'
SOC_LOG = os.path.join(LOG_DIR, 'soc_alerts.json')

class Guard:
    @staticmethod
    def log_incident(threat_level, message):
        incident = {
            "timestamp": datetime.now().isoformat(),
            "threat_level": threat_level,
            "ip": request.remote_addr,
            "path": request.path,
            "details": message
        }
        if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)
        with open(SOC_LOG, 'a') as f:
            f.write(json.dumps(incident) + "\n")
        print(f"[!] SOC ALERT [{threat_level}]: {message}")

    @staticmethod
    def analyze_request():
        path = request.path.lower()
        honey_paths = {
            '/.env': 'Credential theft',
            '/api/config': '9router config probe',
            '/v1/chat/completions': 'AI API probe'
        }
        if path in honey_paths:
            Guard.log_incident('CRITICAL', honey_paths[path])
            return True
            
        if request.is_json and path.startswith('/v1/'):
            content = str(request.get_json()).lower()
            if any(p in content for p in ["id_rsa", "passwd", "config.json"]):
                Guard.log_incident('CRITICAL', f'AI Key/Data Exfiltration Attempt: {content[:50]}')
                return True
        return False
