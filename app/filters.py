from . import app

@app.template_filter('formatdate')
def format_date(value):
    if value is not None:
        return value.strftime('%a, %d')
    return ''