from .format_date import format_date_func

def init_utils(app):
    app.template_filter('format_date_func')(format_date_func)