from flask import Blueprint, render_template, Response, request
from services.guard import Guard
from services.generator import DataGenerator

standard_bp = Blueprint('standard', __name__)

@standard_bp.route('/')
def index():
    return render_template('standard/index.html')

@standard_bp.route('/admin/dashboard')
def dashboard():
    stats = DataGenerator.get_server_stats()
    logs = DataGenerator.generate_logs(8)
    return render_template('standard/dashboard.html', stats=stats, logs=logs)

@standard_bp.route('/admin/terminal')
def terminal():
    Guard.log_incident('CRITICAL', 'Opened internal debug terminal')
    return render_template('standard/terminal.html')
