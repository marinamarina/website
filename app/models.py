from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import login_manager

"""Database models representation"""
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

# Models definitions
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # user will log with an email address
    email = db.Column(db.String(120), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # password is stored in this field
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FOOTY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'verify' : self.id})

    def verify(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        try:
            data = s.loads(token)
            if data.get('verify') != self.id:
                return False
        except Exception:
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True


    # using property because I want to protect the password
    @property
    def password(self):
        raise AttributeError('This property cant be accessed!')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        'user representation'
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    'class is assigned to the current user when the user is not logged in'
    def can(self):
        return False

    def is_admin(self):
        return False

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class ReadOnly(AttributeError):
        'custom exception'
        pass

login_manager.anonymous_user = AnonymousUser

# callback function that loads a user from the database
# user ids in flask-login are always unicode strings, needs to be converted to an
# int
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
