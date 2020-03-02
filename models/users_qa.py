from app import db

class User_qa(db.Model):
    '''this class stores users creadentials..eg name, password'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(),unique=False, nullable=False)
    name= db.Column(db.String(20),nullable=False)
    password= db.Column(db.String(),nullable=False)

    # committing to the database
    def create(self):
        '''sends to the db'''
        db.session.add(self)
        db.session.commit()