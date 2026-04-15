import logging
import json
import os
from datetime import datetime
from flask import request

# Configure SOC logging
LOG_DIR = 'logs'
SOC_LOG = os.path.join(LOG_DIR, 'soc_alerts.json')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class Guard:
    """
    Security monitor for identifying and logging malicious activities.
    """
    
    @staticmethod
    def log_incident(threat_level, message):
        """Logs a security incident to the SOC log file."""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "threat_level": threat_level,
            "ip": request.remote_addr,
            "path": request.path,
            "method": request.method,
            "user_agent": request.headers.get('User-Agent'),
            "details": message
        }
        
        with open(SOC_LOG, 'a') as f:
            f.write(json.dumps(incident) + "\n")
            
        print(f"[!] SOC ALERT [{threat_level}]: {message} from {request.remote_addr}")

    @staticmethod
    def analyze_request():
        """Basic analysis of incoming requests for obvious red flags."""
        path = request.path.lower()
        
        # High-risk paths
        honey_paths = {
            '/.env': 'Attempted credential theft',
            '/wp-admin': 'Wordpress scan',
            '/.git': 'Repository exposure discovery',
            '/phpmyadmin': 'Database manager scan',
            '/admin/config.php': 'Admin configuration access',
            '/api/v1/debug': 'Debug endpoint access',
            '/api/config': 'CVE-2026-5842 (9router) sensitive config exposure',
            '/api/auth/status': 'CVE-2026-5842 (9router) auth bypass check',
            '/v1/chat/completions': 'AI Proxy scan (9router bait)'
        }
        
        if path in honey_paths:
            level = 'CRITICAL' if 'CVE-2026-5842' in honey_paths[path] else 'HIGH'
            Guard.log_incident(level, honey_paths[path])
            return True
            
        # SQL Injection detection
        query = request.query_string.decode('utf-8').lower()
        sql_keywords = ["' OR '1'='1", "union select", "drop table", "select * from"]
        if any(key in query for key in sql_keywords):
            Guard.log_incident('HIGH', f'Potential SQL Injection in query: {query}')
            return True
            
        return False
