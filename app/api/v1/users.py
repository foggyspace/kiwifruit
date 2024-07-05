from app.libs.apiprint import ApiPrint


api = ApiPrint('users')


@api.route('/login', methods=['POST'])
def user_login():
    return {}

