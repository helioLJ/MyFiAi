from . import app

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
    pass