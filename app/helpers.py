from . import app
from functools import wraps
from flask import request, redirect, url_for
from flask_login import current_user

@app.template_filter('formatdate')
def format_date(value):
    if value is not None:
        day_names_english = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_names_portuguese = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        day_name_mapping = dict(zip(day_names_english, day_names_portuguese))
        day_name_english = value.strftime('%a')
        day_name_portuguese = day_name_mapping.get(day_name_english, day_name_english)
        return f'{day_name_portuguese}, {value.strftime("%d")}'
    return ''

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:  # Notice the 'not' here
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function