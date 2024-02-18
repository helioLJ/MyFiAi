from flask import render_template
from flask_login import login_required
from flask_login import login_required, current_user

def init_profile_routes(app):
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html', name=current_user.name, email=current_user.email, profile_pic_url=current_user.profile_pic_url, is_premium=current_user.is_premium)