from flask import Blueprint, render_template
from flask_login import login_required


admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/tasks')
@login_required
def tasks():
    return render_template('admin/lists.html')
