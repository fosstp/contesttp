from wtforms import (Form, StringField, PasswordField, SelectField, DateTimeField,
                     TextAreaField, MultipleFileField, BooleanField)
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
    student1_name = StringField('學生1名字', [InputRequired('學生1名字為必填欄位')])
    student1_class = StringField('學生1班級', [InputRequired('學生1班級為必填欄位')])
    student2_name = StringField('學生2名字')
    student2_class = StringField('學生2班級')
    instructor1 = StringField('指導老師1', [InputRequired('指導老師1為必填欄位')])
    instructor2 = StringField('指導老師2')
    instructor3 = StringField('指導老師3')


class CompetitionNewsForm(Form):
    title = StringField('標題', [InputRequired('標題為必填欄位')])
    content = TextAreaField('內容', [InputRequired('內容為必填欄位')])
    files = MultipleFileField('附件')
    is_sticky = BooleanField('是否置頂')


class PasswordForm(Form):
    old_password = PasswordField('舊密碼', [InputRequired('舊密碼為必填欄位')])
    new_password = PasswordField('新密碼', [InputRequired('新密碼為必填欄位')])
    new_password_confirm = PasswordField('再次輸入新密碼', [EqualTo('new_password', '新密碼輸入必須一致')])
