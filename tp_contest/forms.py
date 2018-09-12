from wtforms import Form, StringField, PasswordField, SelectField, DateTimeField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(Form):
    account_type = SelectField('帳號類型', [InputRequired('帳號類型為必選欄位')], choices=[
                               ('school', '學校'), ('manager', '管理者')])
    account = StringField('帳號', [InputRequired('帳號為必填欄位')])
    password = PasswordField('密碼', [InputRequired('密碼為必填欄位')])


class ManagerForm(Form):
    name = StringField('名稱', [InputRequired('名稱為必填欄位')])
    account = StringField('帳號', [InputRequired('帳號為必填欄位')])
    password = PasswordField('密碼')
    password_confirm = PasswordField('再次輸入密碼', [EqualTo('password', '密碼輸入必須一致')])
    email = StringField('Email', [InputRequired('Email 為必填欄位')])
    type = SelectField('帳號類型', [InputRequired('帳號類型為必選欄位')], choices=[
                               ('0', '最高管理者'), ('1', '活動管理者')])


class CompetitionForm(Form):
    name = StringField('競賽活動名稱', [InputRequired('競賽活動名稱為必填欄位')])
    begin_signup_datetime = DateTimeField('開始報名時間', [InputRequired('開始報名時間為必填欄位')])
    end_signup_datetime = DateTimeField('結束報名時間', [InputRequired('結束報名時間為必填欄位')])
    manager = SelectField('管理者', [InputRequired('管理者為必選欄位')])


class CompetitionSignUpForm(Form):
    student_name = StringField('學生名字', [InputRequired('學生名字為必填欄位')])
    student_class = StringField('學生班級', [InputRequired('學生班級為必填欄位')])
    instructor1 = StringField('指導老師1', [InputRequired('指導老師1為必填欄位')])
    instructor2 = StringField('指導老師2', [InputRequired('指導老師2為必填欄位')])