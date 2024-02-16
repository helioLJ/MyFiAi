from .. import app

from flask import render_template

from ..services.dashboard import get_dashboard_data
from ..helpers import require_auth

@app.route('/dashboards')
def dashboards():
    get_dashboard_data()
    return render_template('dashboard.html')