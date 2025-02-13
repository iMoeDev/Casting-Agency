from flask_sqlalchemy import SQLAlchemy
import os



db = SQLAlchemy()
migrate = None 


def setup_db(app, database_url=None):
    """Setup the database with Flask app"""
    global migrate 
    try:
        if database_url is None:
            database_url = os.getenv('DB_URL')

        if app.config.get("TESTING", False) or "FLASK_ENV" in os.environ and os.environ["FLASK_ENV"] == "testing":
            database_url = os.getenv('DB_TEST_URL') 
        print(f" Checking DB_URL: {database_url}") 
        #  Ensure Flask recognizes the database before migrations
        if not hasattr(app, 'db_initialized'):
            app.config["SQLALCHEMY_DATABASE_URI"] = database_url
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            db.init_app(app)


            app.db_initialized = True

    except Exception as e:
        print(f" ERROR in setup_db(): {str(e)}")




class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()    

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    