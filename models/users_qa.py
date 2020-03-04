from app import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User_qa(UserMixin, db.Model):
    '''this class stores users creadentials..eg name, password'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(),unique=False, nullable=False)
    name= db.Column(db.String(20),nullable=False)
    password= db.Column(db.String(),nullable=False)
    is_admin= db.Column(db.Boolean,default=False)
    is_expert = db.Column(db.Boolean,default=False)

    # committing to the database
    def create(self):
        '''sends to the db'''
        db.session.add(self)
        db.session.commit()

    # function to search for name and password
    @classmethod
    def search_name_and_password(cls,name,password):
        '''this fuction checks for te name and password'''
        name_check=cls.query.filter_by(name=name).first()
        if name_check and check_password_hash(name_check.password,password):
            return True
        else:
            return False

    # updating admin role
    @classmethod
    def promote(cls,name):
        user= cls.query.filter_by(name=name).first()
        if user:
            print(user.is_expert)
            user.is_expert = True
            db.session.commit()
            return True


