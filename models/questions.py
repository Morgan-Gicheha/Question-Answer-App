from app import db
class Questions_qa(db.Model):
    '''this class store questions, and expert_id'''
    __tablename__="questions_qa"
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(),nullable=True)
    expert_id= db.Column(db.Integer,nullable=False)
    is_answerd = db.Column(db.Boolean, default=False)

    # function to commit 
    def create(self):
        '''send questios to db'''
        db.session.add(self)
        db.session.commit()