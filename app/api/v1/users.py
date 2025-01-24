from app.libs.apiprint import ApiPrint
from app.libs.errors import Success
from app.libs.jwt import generate_token
from app.validators.forms import LoginForm, RegisterForm
from app.models.users import User
from flask import g

api = ApiPrint('users')

@api.route('/login', methods=['POST'])
def user_login():
    form = LoginForm().validate_for_api()
    user = User.verify(email=form.username.data, password=form.password.data)
    token = generate_token(user['uuid'])
    return Success(data={'token': token, **user})

@api.route('/register', methods=['POST'])
def user_register():
    form = RegisterForm().validate_for_api()
    user = User()
    user.email = form.email.data
    user.nickname = form.username.data
    user.password = form.password.data
    user.save()
    return Success(msg='注册成功')

@api.route('/logout', methods=['POST'])
def user_logout():
    # 前端需要清除token
    return Success(msg='退出成功')

