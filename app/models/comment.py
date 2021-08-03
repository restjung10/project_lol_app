from app import db

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128))
    comment = db.Column(db.String(128))
    ids_id = db.Column(db.String(128), db.ForeignKey('ids.id'))

    nicks = db.relationship('IDs', back_populates='comments')

    def __repr__(self):
        return f"{self.comment}"
