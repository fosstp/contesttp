import os
from datetime import datetime
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid_sqlalchemy import Session as DB
from .models import Manager, School, Competition, CompetitionSignUp, CompetitionNews, File
from .security import need_permission


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    account_type = request.session.get('account_type', None)
    if account_type and account_type in ['admin', 'manager']:
        return HTTPFound(location=request.route_url('list_admin_competition'), headers=request.response.headers)
    else:
        return HTTPFound(location=request.route_url('list_guest_competition'), headers=request.response.headers)


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
                manager = DB.query(Manager).filter_by(
                    account=login_form.account.data).one()
                if manager.verify_password(login_form.password.data):
                    request.session['account_type'] = 'admin' if manager.type == 0 else 'manager'
                    request.session['name'] = manager.name
                    request.session['id'] = manager.id
                    request.session['account'] = manager.account
                    return HTTPFound(location=request.route_url('list_admin_competition'), headers=request.response.headers)
                else:
                    request.session.flash('帳密認証錯誤，請重新輸入', 'error')
                    return {'login_form': login_form}
            elif login_form.account_type.data == 'school':
                school = DB.query(School).filter_by(
                    account=login_form.account.data).one()
                if school.verify_password(login_form.password.data):
                    request.session['account_type'] = 'school'
                    request.session['name'] = school.name
                    request.session['id'] = school.id
                    request.session['account'] = school.account
                    if school.status == 0:
                        return HTTPFound(location=request.route_url('change_password'), headers=request.response.headers)
                    else:
                        return HTTPFound(location=request.route_url('list_guest_competition'), headers=request.response.headers)
                else:
                    request.session.flash('帳密認証錯誤，請重新輸入', 'error')
                    return {'login_form': login_form}
        except NoResultFound:
            request.session.flash('帳密認証錯誤，請重新輸入', 'error')
    request.session.flash('帳密認証錯誤，請重新輸入', 'error')
    return {'login_form': login_form}


@view_config(route_name='logout')
def logout_view(request):
    for i in 'account_type', 'name', 'account':
        if i in request.session:
            del request.session[i]
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='list_guest_competition', renderer='templates/list_competition.jinja2')
def list_guest_competition_view(request):
    # 匿名使用者，只能看尚未過期的競賽列表
    now = datetime.now()
    competition = DB.query(Competition).filter(datetime.now()<Competition.end_signup_datetime).all()
    return {'competition': competition, 'now': now}

@view_config(route_name='list_admin_competition', renderer='templates/list_competition.jinja2')
def list_admin_competition_view(request):
    # 最高管理者可看全部列表
    now = datetime.now()
    competition = DB.query(Competition).all()
    return {'competition': competition, 'now': now}

@view_config(route_name='add_competition', renderer='templates/add_competition.jinja2')
def add_competition_view(request):
    from .forms import CompetitionForm

    competition_form = CompetitionForm()
    competition_form.manager.choices = [(str(manager.id), manager.name) for manager in DB.query(Manager).filter_by(type=1).all()]
    return {'competition_form': competition_form}


@view_config(route_name='list_competition_news', renderer='templates/list_competition_news.jinja2')
def list_competition_news_view(request):
    competition_id = int(request.matchdict['competition_id'])
    competition = DB.query(Competition).filter_by(id=competition_id).one()
    competition_news = DB.query(CompetitionNews).filter_by(competition_id=competition_id).order_by(CompetitionNews.status.desc(), CompetitionNews.id)
    return {'competition': competition, 'competition_news': competition_news}

@view_config(route_name='show_competition_news', renderer='templates/show_competition_news.jinja2')
def show_competition_news_view(request):
    competition_news = DB.query(CompetitionNews).get(int(request.matchdict['news_id']))
    return {'competition_news': competition_news}


@view_config(route_name='list_managers', renderer='templates/list_managers.jinja2')
@need_permission('admin')
def list_managers_view(request):
    managers = DB.query(Manager).all()
    return {'managers': managers}


@view_config(route_name='show_manager', renderer='templates/show_manager.jinja2', request_method='GET')
@need_permission('admin')
def show_manager_view(request):
    from .forms import ManagerForm

    manager = DB.query(Manager).filter_by(id=int(request.matchdict['manager_id'])).one()
    manager_form = ManagerForm(obj=manager)
    return {'manager_form': manager_form}

@view_config(route_name='show_manager', renderer='templates/show_manager.jinja2', request_method='POST')
@need_permission('admin')
def show_manager_view(request):
    from .forms import ManagerForm

    manager_form = ManagerForm(request.POST)
    if manager_form.validate():
        manager = DB.query(Manager).filter_by(id=int(request.matchdict['manager_id'])).one()
        manager.password = manager_form.password.data
        DB.add(manager)
        return HTTPFound(location=request.route_url('list_managers'), headers=request.response.headers)
    else:
        request.session.flash('請確認各欄位輸入正確', 'error')
        return {'manager_form': manager_form}

@view_config(route_name='list_signup_per_competition', renderer='templates/list_competition_signup.jinja2')
@need_permission('manager')
def list_signup_per_competition_view(request):
    competition_id = int(request.matchdict['competition_id'])
    competition = DB.query(Competition).get(competition_id)
    signup_list = DB.query(CompetitionSignUp).filter_by(competition_id=competition_id).all()
    signup_limit = DB.query(Competition).filter_by(id=competition_id).one().signup_limit
    return {'competition': competition, 'signup_list': signup_list, 'competition_id': competition_id, 'signup_limit': signup_limit}


@view_config(route_name='list_signup_per_competition_school', renderer='templates/list_competition_signup.jinja2')
@need_permission('school')
def list_signup_per_competition_school_view(request):
    competition_id = int(request.matchdict['competition_id'])
    competition = DB.query(Competition).get(competition_id)
    school_signup_list = DB.query(CompetitionSignUp).filter_by(competition_id=competition_id).filter_by(school_id=request.session['id']).all()
    signup_limit = DB.query(Competition).filter_by(id=competition_id).one().signup_limit
    is_signupable = True if competition.begin_signup_datetime < datetime.now() < competition.end_signup_datetime else False
    return {'competition': competition, 'signup_list': school_signup_list, 'competition_id': competition_id, 'signup_limit': signup_limit, 'is_signupable': is_signupable}


@view_config(route_name='delete_signup')
def delete_signup_view(request):
    competition_id = int(request.matchdict['competition_id'])
    signup_id = int(request.matchdict['signup_id'])

    if 'account_type' not in request.session:
        return HTTPForbidden()

    if request.session['account_type'] == 'school':
        DB.query(CompetitionSignUp).filter_by(id=signup_id).filter_by(school_id=request.session['id']).delete()
        return HTTPFound(location=request.route_url('list_signup_per_competition_school', competition_id=competition_id), headers=request.response.headers)
    else:
        DB.query(CompetitionSignUp).filter_by(id=signup_id).delete()
        return HTTPFound(location=request.route_url('list_signup_per_competition', competition_id=competition_id), headers=request.response.headers)
        

@view_config(route_name='signup_competition', renderer='templates/signup_competition.jinja2', request_method='GET')
def signup_competition_get_view(request):
    from .forms import CompetitionSignUpForm

    competition_signup_form = CompetitionSignUpForm()
    return {'competition_signup_form': competition_signup_form}


@view_config(route_name='signup_competition', renderer='templates/signup_competition.jinja2', request_method='POST')
@need_permission('school')
def signup_competition_post_view(request):
    from .forms import CompetitionSignUpForm

    competition_signup_form = CompetitionSignUpForm(request.POST)
    if competition_signup_form.validate():
        competition_id = int(request.matchdict['competition_id'])
        competition = DB.query(Competition).get(competition_id)
        if competition.begin_signup_datetime < datetime.now() < competition.end_signup_datetime:
            signup = CompetitionSignUp()
            competition_signup_form.populate_obj(signup)
            signup.competition_id = competition_id
            signup.school_id = request.session['id']
            DB.add(signup)
            return HTTPFound(location=request.route_url('list_signup_per_competition_school', competition_id=competition_id), headers=request.response.headers)
        else:
            return HTTPForbidden()
    return {'competition_signup_form': competition_signup_form}


@view_config(route_name='add_competition_news', renderer='templates/add_competition_news.jinja2', request_method='GET')
@need_permission('manager')
def add_competition_news_get_view(request):
    from .forms import CompetitionNewsForm

    competition_news_form = CompetitionNewsForm()
    return {'competition_news_form': competition_news_form}


@view_config(route_name='add_competition_news', renderer='templates/add_competition_news.jinja2', request_method='POST')
@need_permission('manager')
def add_competition_news_post_view(request):
    import random, string, shutil
    import pkg_resources
    from .forms import CompetitionNewsForm

    competition_news_form = CompetitionNewsForm(request.POST)
    if competition_news_form.validate():
        competition_id = int(request.matchdict['competition_id'])
        if DB.query(Competition).get(competition_id).manager_id != request.session['id']:
            return HTTPForbidden()
        competition_news = CompetitionNews()
        competition_news.title = competition_news_form.title.data
        competition_news.content = competition_news_form.content.data 
        competition_news.competition_id = competition_id
        competition_news.manager_id = request.session['id']
        if competition_news_form.is_sticky.data:
            competition_news.status = 1
        # 處理上傳檔案
        if competition_news_form.files.data != [b'']:
            # is FieldStorage
            file_list = request.POST.getall('files')
            dst_base_dir = pkg_resources.resource_filename('tp_contest', 'static/upload_files')
            if not os.path.exists(dst_base_dir):
                os.mkdir(dst_base_dir)
            competition_base_dir = os.path.join(dst_base_dir, str(competition_id))
            if not os.path.exists(competition_base_dir):
                os.mkdir(competition_base_dir)
            for each_file in file_list:
                dst_file_name = '{0}_{1}'.format(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5)), each_file.filename)
                dst_file_path = os.path.join(competition_base_dir, dst_file_name)
                each_file.file.seek(0)
                with open(dst_file_path, 'wb') as dst:
                    shutil.copyfileobj(each_file.file, dst)
                file_model = File()
                file_model.name = dst_file_name
                DB.add(file_model)
                competition_news.files.append(file_model)
        DB.add(competition_news)
        return HTTPFound(location=request.route_url('list_competition_news', competition_id=competition_id), headers=request.response.headers)
    else:    
        return {'competition_news_form': competition_news_form}


@view_config(route_name='delete_competition_news')
@need_permission('manager')
def delete_competition_news_view(request):
    competition_id = int(request.matchdict['competition_id'])
    competition_news_id = int(request.matchdict['news_id'])
    competition = DB.query(Competition).get(competition_id)
    if competition.manager_id != request.session['id']:
        return HTTPForbidden()
    DB.query(File).filter_by(competition_news_id=competition_news_id).delete()
    DB.query(CompetitionNews).filter_by(id=competition_news_id).delete()
    return HTTPFound(location=request.route_url('list_competition_news', competition_id=competition_id), headers=request.response.headers)


@view_config(route_name='change_password', renderer='templates/change_password.jinja2', request_method='GET')
@need_permission('school')
def change_password_get_view(request):
    from .forms import PasswordForm

    return {'password_form': PasswordForm()}


@view_config(route_name='change_password', renderer='templates/change_password.jinja2', request_method='POST')
@need_permission('school')
def change_password_post_view(request):
    from .forms import PasswordForm

    password_form = PasswordForm(request.POST)
    if password_form.validate():
        school = DB.query(School).get(request.session['id'])
        if school.verify_password(password_form.old_password.data):
            school.password = password_form.new_password.data
            school.status = 1
            DB.add(school)
            return HTTPFound(location=request.route_url('list_guest_competition'), headers=request.response.headers)
        else:
            request.session.flash('密碼錯誤，請確認舊密碼正確', 'error')
            return {'password_form': password_form}
    else:
        print('d')
        request.session.flash('密碼錯誤，請確認舊密碼正確，兩次新密碼輸入相同', 'error')
        return {'password_form': password_form}
