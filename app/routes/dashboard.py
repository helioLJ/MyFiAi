from .. import app

from flask import render_template

from ..services.dashboard import get_dashboard_data
from flask_login import login_required

@app.route('/dashboards')
@login_required
def dashboards():
    get_dashboard_data()
    return render_template('dashboard.html')