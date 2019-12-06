from datA import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Creating the users table. This table will hold all users in the system."""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    second_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False, unique=True)
    datalists = db.relationship('DataList', backref='datalists', lazy='dynamic',
                                  cascade="all, delete-orphan")

    @property
    def password(self):
        """Show an error message when a user tries to edit the password
        field in the database.
        """
        raise AttributeError('Password field is a write-only field, can not be changed!')

    @password.setter
    def password(self, password):
        """Creates a hashed password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Compare password hashes with that saved in the user table."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return User.query.all()


class DataList(db.Model):
    """creating the datalists table. This table will hold all
    data lists created.
    """
    __tablename__ = 'datalists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.String, db.ForeignKey('Users.email'))
    datalist_items = db.relationship('DataListItem', backref='items', lazy='dynamic',
                                     cascade="all, delete-orphan")

    def __init__(self, name, user_email):
        self.name = name
        self.created_by = user_email

    def __repr__(self):
        return '<DataList {}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return Datalist.query.all()


class DataListItem(db.Model):
    """Creating the Datalist Items table. This table will hold all
    items in all data lists.
    """
    __tablename__ = 'Datalist Items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    data_list_it_belongs_to = db.Column(db.String, db.ForeignKey('datalists.name'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Data_list_Item {}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self):
        return DataListItem.query.all()

