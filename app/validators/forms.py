from flask import request
from wtforms import Form as WTForms, ValidationError, validators

from wtforms.validators import DataRequired, EqualTo, Regexp
from wtforms import PasswordField, StringField


class Form(WTForms):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(Form, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(Form, self).validate()
        if not valid:
            raise ValidationError
        return self


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])


class ChangePasswordForm(Form):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不能为空'),
        Regexp('^[A-Za-z0-9_*$@]{6,22}', message='密码长度在6-22之间,包含字符,字母'),
        EqualTo('confirm_password', message='两次密码输入必须一致')
        ])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(message='请确认密码')])
    old_password = PasswordField('原密码', validators=[DataRequired(message='请输入原密码')])



