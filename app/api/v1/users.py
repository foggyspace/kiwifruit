from app.libs.apiprint import ApiPrint

from app.validators.forms import LoginForm
from app.models.users import User


api = ApiPrint('users')


@api.route('/login', methods=['POST'])
def user_login():
    form = LoginForm().validate_for_api()
    user = User.verify(email=form.username.data, password=form.password.data)

