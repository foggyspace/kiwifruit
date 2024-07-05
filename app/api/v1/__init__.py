from flask import Blueprint
from app.api.v1 import users


def create_blueprint_v1() -> Blueprint:
    '''创建蓝图对象
    将所有的api蓝图注册进来统一导出出去
    '''
    bp_v1 = Blueprint('v1', __name__)

    users.api.register(bp_v1)
    return bp_v1

