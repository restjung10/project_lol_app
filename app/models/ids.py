from app import db

class IDs(db.Model):
    __tablename__ = 'ids'

    id = db.Column(db.String(128), nullable=False, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False)
    acc_id = db.Column(db.String(128), nullable=False)

    leagues = db.relationship('League', back_populates='ids')
    comments = db.relationship('Comment', back_populates='nicks')
    wins = db.relationship('Win', back_populates='accs')

    def __repr__(self):
        return f"IDs {self.nickname}"
