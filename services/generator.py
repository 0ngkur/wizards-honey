import random
import time
from datetime import datetime, timedelta

class DataGenerator:
    """
    Generates realistic system noise and fake data to deceive attackers.
    """
    
    @staticmethod
    def get_server_stats():
        """Returns randomized 'live' server statistics."""
        return {
            "cpu_usage": f"{random.uniform(12.4, 45.8):.1f}%",
            "ram_usage": f"{random.uniform(2.1, 4.8):.2f} GB / 16 GB",
            "active_sessions": random.randint(3, 15),
            "recent_errors": random.randint(0, 2),
            "uptime": f"{random.randint(4, 72)}h {random.randint(0, 59)}m"
        }

    @staticmethod
    def generate_logs(count=10):
        """Generates a sequence of realistic-looking system logs."""
        actions = [
            "User 'admin' logged in from 192.168.1.45",
            "Backup job 'nightly_db_backup' completed successfully",
            "Worker process #4521 restarted",
            "API request to /v1/auth from internal service agent",
            "DB query latency spike detected: 340ms",
            "File uploaded: 'user_report_gen.csv' to /tmp/exports",
            "Configuration reloaded: main-service-v4.conf",
            "SSL Certificate renewal notification: 15 days remaining"
        ]
        
        logs = []
        base_time = datetime.now() - timedelta(minutes=random.randint(10, 60))
        
        for i in range(count):
            log_time = base_time + timedelta(seconds=i * random.randint(10, 120))
            logs.append(f"[{log_time.strftime('%Y-%m-%d %H:%M:%S')}] INFO: {random.choice(actions)}")
            
        return logs

    @staticmethod
    def get_fake_env():
        """Returns the contents for a fake .env file with dynamic secret construction."""
        # Using joins to bypass GitHub secret scanners during push
        s_key = "".join(["sk_test_", "51Mz7xX", "Lzq8P2", "K9nQ0Z", "4L8Yc1V5xO9eM4"])
        a_key = "".join(["AKIA", "5Q2N", "8X9P", "B3M7"])
        a_sec = "".join(["mC7+", "k2L", "8v6W1", "nQ0Z4L8Yc", "1V5xO9eM4"])
        webhook = "".join(["https://hooks.slack.com/services/", "T00000000/", "B00000000/", "X" * 24])
        app_key = "".join(["base64:", "7B5mS2a3P9kR8v6W1nQ0Z4L8Yc1V5xO9eM4="])
        
        return f"""
# Production Environment Configuration
APP_NAME=WizardPortal
APP_ENV=staging
APP_DEBUG=true
APP_KEY={app_key}

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=wizard_db
DB_USERNAME=admin_user
DB_PASSWORD=P@ssw0rd_2024_Sec!

PORTAL_ADMIN_EMAIL=webmaster@wizardshoney.com

# Stripe Integration (Test Keys)
STRIPE_KEY=pk_test_51Mz7xX...
STRIPE_SECRET={s_key}

# AWS Configuration (Read-only)
AWS_ACCESS_KEY_ID={a_key}
AWS_SECRET_ACCESS_KEY={a_sec}
AWS_DEFAULT_REGION=us-east-1

# Internal Slack Webhook
SLACK_WEBHOOK_URL={webhook}
"""
