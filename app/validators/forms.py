from flask import request
from wtforms import Form as WTForms
from wtforms.validators import DataRequired, EqualTo, Regexp, Email, Length
from wtforms import PasswordField, StringField
from app.libs.errors import ParameterError


class Form(WTForms):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(Form, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(Form, self).validate()
        if not valid:
            raise ParameterError(msg=self.errors)
        return self

    def strip_string_fields(self):
        """去除所有字符串字段的首尾空格"""
        for field in self._fields.values():
            if isinstance(field.data, str):
                field.data = field.data.strip()
        return self

    def sanitize_string(self, field_name):
        """清理特定字段的特殊字符"""
        if hasattr(self, field_name):
            field = getattr(self, field_name)
            if isinstance(field.data, str):
                field.data = ''.join(char for char in field.data if char.isprintable())
        return self


class LoginForm(Form):
    username = StringField('用户名/邮箱', validators=[
        DataRequired(message='用户名不能为空'),
        Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$|^[A-Za-z0-9_]+$', message='请输入有效的用户名或邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=22, message='密码长度必须在6-22位之间')
    ])

    def validate(self):
        self.strip_string_fields()
        self.sanitize_string('username')
        return super(LoginForm, self).validate()


class ChangePasswordForm(Form):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不能为空'),
        Regexp('^[A-Za-z0-9_*$@]{6,22}', message='密码长度在6-22之间,包含字符,字母'),
        EqualTo('confirm_password', message='两次密码输入必须一致')
    ])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(message='请确认密码')])
    old_password = PasswordField('原密码', validators=[DataRequired(message='请输入原密码')])

    def validate(self):
        self.strip_string_fields()
        return super(ChangePasswordForm, self).validate()


class RegisterForm(Form):
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Email(message='请输入有效的邮箱地址')
    ])
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度必须在3-20位之间'),
        Regexp('^[A-Za-z0-9_]+$', message='用户名只能包含字母、数字和下划线')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, max=22, message='密码长度必须在6-22位之间'),
        Regexp('^[A-Za-z0-9_*$@]+$', message='密码只能包含字母、数字和特殊字符(_*$@)')
    ])

    def validate(self):
        self.strip_string_fields()
        self.sanitize_string('username')
        self.sanitize_string('email')
        return super(RegisterForm, self).validate()


class TaskCreateForm(Form):
    name = StringField('任务名称', validators=[
        DataRequired(message='任务名称不能为空'),
        Length(min=1, max=50, message='任务名称长度必须在1-50位之间')
    ])
    target_url = StringField('目标URL', validators=[
        DataRequired(message='目标URL不能为空'),
        Regexp('^https?://[\\w\\-]+(\\.[\\w\\-]+)+([\\w\\-.,@?^=%&:/~+#]*[\\w\\-@?^=%&/~+#])?$', 
               message='请输入有效的URL地址')
    ])
    scan_policy = StringField('扫描策略', validators=[
        DataRequired(message='扫描策略不能为空')
    ])

    def validate(self):
        self.strip_string_fields()
        self.sanitize_string('name')
        self.sanitize_string('target_url')
        return super(TaskCreateForm, self).validate()


