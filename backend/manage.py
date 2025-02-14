import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from backend.api import create_app
from backend.models import db

app=create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()