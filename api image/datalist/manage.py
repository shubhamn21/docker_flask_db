from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from datA import db, app
from datA.database_models import User, DataListItem, DataList

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates database with tables"""
    # db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def drop_db():
    """Deletes database"""
    db.drop_all()

if __name__ == '__main__':
    manager.run()
