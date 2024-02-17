# dashboard.py
from flask import render_template
from flask_login import login_required
from ..services.dashboard import get_dashboard_data

def init_dashboard_routes(app):
    @app.route('/dashboards')
    @login_required
    def dashboards():
        images = get_dashboard_data()
        return render_template('dashboard.html', images=images)