from wtforms import Form, StringField, PasswordField, SelectField
from wtforms.validators import InputRequired


class LoginForm(Form):
    account_type = SelectField('帳號類型', [InputRequired('帳號類型為必選欄位')], choices=[
                               ('school', '學校'), ('manager', '管理者')])
    account = StringField('帳號', [InputRequired('帳號為必填欄位')])
    password = PasswordField('密碼', [InputRequired('密碼為必填欄位')])
