from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    return {}


@view_config(route_name='list_activities', renderer='templates/list_activities.jinja2')
def list_activities_view(request):
    return {}
