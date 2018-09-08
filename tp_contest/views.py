from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_sqlalchemy import Session as DB
from .models import Manager, School
from .security import need_permission


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2', request_method='GET')
def login_get_view(request):
    from .forms import LoginForm

    return {'login_form': LoginForm()}


@view_config(route_name='login', renderer='templates/login.jinja2', request_method='POST')
def login_post_view(request):
    from sqlalchemy.orm.exc import NoResultFound
    from .forms import LoginForm

    login_form = LoginForm(request.POST)
    if login_form.validate():
        try:
            if login_form.account_type.data == 'manager':
                manager = DB.query(Manager).filter_by(account=login_form.account.data).one()
                if manager.verify_password(login_form.password.data):
                    request.session['account_type'] = 'admin' if manager.type == 0 else 'manager'
                    request.session['name'] = manager.name
                    request.session['account'] = manager.account
            elif login_form.account_type.data == 'school':
                school = DB.query(School).filter_by(account=login_form.account.data).one()
                if school.verify_password(login_form.password.data):
                    request.session['account_type'] = 'school'
                    request.session['name'] = school.name
                    request.session['account'] = school.account
            return HTTPFound(location=request.route_url('home'), headers=request.headers)
        except NoResultFound:
            request.session.flash('帳密認証錯誤，請重新輸入', 'error')
    return {'login_form': login_form}


@view_config(route_name='list_activities', renderer='templates/list_activities.jinja2')
def list_activities_view(request):
    return {}
