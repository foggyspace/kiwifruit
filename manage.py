from flask_script import Manager, Server
#from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models.admin import Admin
from app.extensions import db

app = create_app()

#migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('server', Server())
#manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Admin=Admin)


@manager.option('-u', '--username',default='admin')
@manager.option('-p', '--password', default='admin')
def createadmin(username, password):
    admin = Admin()
    admin.username = username
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print('success!')


if __name__ == '__main__':
    manager.run()
