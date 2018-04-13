from application  import db, bcrypt
from application.models import Base

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), unique=True, nullable=False)
    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)

    messages = db.relationship("Message", backref='account', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        print(type(password))
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def check_password(self, plaintext):
        return bcrypt.checkpw(plaintext.encode('utf-8'), self.password.encode('utf-8'))
